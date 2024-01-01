#!/usr/bin/env python3
import re
import sys
from pathlib import Path
from typing import Optional

from libcst.metadata import CodeRange
from lsprotocol.types import (
    TEXT_DOCUMENT_COMPLETION,
    TEXT_DOCUMENT_DID_CHANGE,
    TEXT_DOCUMENT_DID_OPEN,
    TEXT_DOCUMENT_DID_SAVE,
    CompletionList,
    CompletionParams,
    DidChangeTextDocumentParams,
    DidOpenTextDocumentParams,
    DidSaveTextDocumentParams,
    TextDocumentContentChangeEvent_Type1,
    Position,
    Range,
    TextDocumentIdentifier,
)
from pygls.server import LanguageServer
from pygls.workspace import Document

from .pool import PoolManager


def log_debug(log):
    print(log, file=sys.stderr)


class TrytonServer(LanguageServer):
    def __init__(self) -> None:
        super().__init__("tryton-ls", "v0.1")
        self._pool_manager: PoolManager | None = None
        self._last_complete_position: tuple[int, int] = (0, 0)
        self._last_completion: Optional[CompletionList] = None

    def get_pool_manager(self):
        if self._pool_manager is None:
            self._pool_manager = PoolManager()
        return self._pool_manager

    def reset_pool_manager(self):
        if self._pool_manager is None:
            return
        self._pool_manager.close()
        self._pool_manager = None

    def generate_diagnostics(
        self, document: TextDocumentIdentifier, ranges: list[Range]
    ) -> None:
        log_debug(f"starting diagnostic generation for {document.uri}")
        text_document = self.workspace.get_document(document.uri)
        source_data = text_document.source
        document_path = Path(text_document.path)
        diagnostics = self.get_pool_manager().generate_diagnostics(
            document_path,
            data=source_data,
            ranges=[
                CodeRange(
                    (range.start.line, range.start.character),
                    (range.end.line, range.end.character),
                )
                for range in ranges
            ],
        )
        self.publish_diagnostics(
            document.uri, [x.to_lsp_diagnostic() for x in diagnostics]
        )
        log_debug(f"Completed diagnostic generation for {document.uri}")

    def generate_completions(
        self, document: TextDocumentIdentifier, position: Position
    ) -> CompletionList:
        text_document = self.workspace.get_document(document.uri)
        completion_data = self._get_completion_data(text_document, position)
        log_debug(
            f"Starting completion for {document.uri}, filter {completion_data['filter']}"
        )
        if completion_data["position"] == self._last_complete_position:
            log_debug(f"Used cached completion for {document.uri}")
        else:
            self._last_completion_position = completion_data["position"]
            document_path = Path(text_document.path)
            completions = self.get_pool_manager().generate_completions(
                document_path,
                data=completion_data["source"],
                line=position.line + 1,
                column=position.character,
            )
            self._last_completion = completions
        completions = self._last_completion
        incomplete = False
        if completion_data["filter"]:
            target_regex = re.compile(
                r".*".join(re.escape(x) for x in completion_data["filter"])
            )
            completions = [
                x for x in completions if re.search(target_regex, x.label)
            ]
        if len(completions) > 100:
            completions = completions[:100]
            incomplete = True
        result = CompletionList(is_incomplete=False, items=completions)
        log_debug(
            f"{'[PARTIAL] ' if incomplete else ''}Completed completion for {document.uri} with {len(completions)} items"
        )
        return result

    def _get_completion_data(
        self, text_document: Document, position: Position
    ) -> dict:
        lines = [x[:-1] for x in text_document.lines]
        line_data = lines[position.line]
        col = position.character - 1
        if line_data[col] == ".":
            lines[position.line] = (
                line_data[: col + 1] + "a" + line_data[col + 1 :]
            )
            col += 1
        for i in range(col):
            if line_data[col - i] == ".":
                col = col - i + 1
                break
        return {
            "source": "\n".join(lines),
            "position": (position.line + 1, col),
            "filter": line_data[col:],
        }


def run() -> None:
    tryton_server = TrytonServer()

    @tryton_server.feature(
        TEXT_DOCUMENT_COMPLETION,
    )
    async def completions(
        params: Optional[CompletionParams] = None,
    ) -> CompletionList:
        """Returns completion items."""
        if not params:
            return
        return tryton_server.generate_completions(
            params.text_document, params.position
        )

    @tryton_server.feature(TEXT_DOCUMENT_DID_OPEN)
    async def did_open(
        ls: LanguageServer, params: DidOpenTextDocumentParams
    ) -> None:
        """Text document did open notification."""
        tryton_server.generate_diagnostics(params.text_document, [])

    @tryton_server.feature(TEXT_DOCUMENT_DID_SAVE)
    async def did_save(
        ls: LanguageServer, params: DidSaveTextDocumentParams
    ) -> None:
        """Text document did change notification."""
        tryton_server.reset_pool_manager()
        tryton_server.generate_diagnostics(params.text_document, [])

    @tryton_server.feature(TEXT_DOCUMENT_DID_CHANGE)
    async def did_change(
        ls: LanguageServer, params: DidChangeTextDocumentParams
    ) -> None:
        """Text document did change notification."""
        ranges = []
        for content_change in params.content_changes:
            if (
                isinstance(content_change,
                           TextDocumentContentChangeEvent_Type1)
                and content_change.range
            ):
                ranges.append(content_change.range)
        if ranges:
            tryton_server.generate_diagnostics(params.text_document, ranges)

    tryton_server.start_io()


if __name__ == "__main__":
    run()
