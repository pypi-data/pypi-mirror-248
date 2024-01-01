from __future__ import annotations

import os
from collections.abc import Generator
from pathlib import Path
from typing import Any

from libcst.metadata import CodeRange

from .analyzer import CompletionTargetFoundError, PythonCompletioner
from .parsing import (
    Module,
    ParsedFile,
    ParsedPythonFile,
    ParsedViewFile,
    ParsedXMLFile,
    ParsingError,
)
from .pool_companion import Companion
from .tools import CompletionItem, Diagnostic, generate_completions_from_model


class UnknownModelException(KeyError):
    pass


class PoolManager:
    def __init__(self) -> None:
        super().__init__()
        self._parsed: dict[Path, ParsedFile | None] = {}
        self._modules: dict[str, Module] = {}
        self._pools: dict[tuple[str, ...], Pool] = {}
        self._companion: Companion = Companion()

    def close(self) -> None:
        self._companion.close()

    def get_companion(self) -> Companion:
        if self._companion.is_alive():
            return self._companion
        new_companion = Companion()
        dead_companion = self._companion
        self._companion = new_companion
        self._pools.clear()
        dead_companion.close()
        return new_companion

    def is_alive(self) -> bool:
        return self._companion.is_alive()

    def get_pool(self, module_names: list[str]) -> Pool:
        key = tuple(sorted(module_names))
        if key in self._pools:
            return self._pools[key]

        companion = self.get_companion()
        result = companion.init_pool(key)
        pool = Pool(self, key, result["models"], result["wizards"])
        self._pools[key] = pool
        return self._pools[key]

    def fetch_model(self, key: list[str], name: str, kind: str) -> dict:
        return self.get_companion().fetch_model(key, name, kind)

    def fetch_super_information(
        self, key: list[str], kind: str, name: str, function_name: str
    ) -> Any:
        return self.get_companion().fetch_super_information(
            key, kind, name, function_name
        )

    def fetch_completions(
        self, key: list[str], name: str, kind: str
    ) -> list[Any]:
        return self.get_companion().fetch_completions(key, name, kind)

    def _get_module(self, module_name: str) -> Module:
        if module_name in self._modules:
            return self._modules[module_name]
        module = Module(module_name)
        self._modules[module_name] = module
        return module

    def generate_diagnostics(
        self,
        path: Path,
        ranges: list[CodeRange] | None = None,
        data: str | None = None,
    ) -> list[Diagnostic]:
        parsed = self.get_parsed(path, data=data)
        if parsed:
            return self._get_diagnostics(parsed, ranges=ranges)
        return []

    def generate_completions(
        self, path: Path, line: int, column: int, data: str | None = None
    ) -> list[CompletionItem]:
        parsed = self.get_parsed(path, data=data)
        if parsed and isinstance(parsed, ParsedPythonFile):
            return self._get_completions(parsed, line, column)
        return []

    def get_parsed(
        self, path: Path, data: str | None = None
    ) -> ParsedFile | None:
        Parser: type[ParsedFile] | None = self._parser_from_path(path)
        if Parser is None:
            return None
        can_fallback = data is not None
        if not can_fallback:
            with open(path) as f:
                data = f.read()

        parsed: ParsedFile | None = None
        try:
            parsed = Parser(path, data=data)
        except ParsingError:
            if path in self._parsed:
                parsed = self._parsed[path]
            if parsed is None and can_fallback:
                try:
                    parsed = Parser(path)
                except ParsingError:
                    parsed = None
            else:
                parsed = None

        if parsed is not None and parsed.get_module_name():
            parsed.set_module(self._get_module(parsed.get_module_name()))
        self._parsed[path] = parsed
        return parsed

    def _parser_from_path(self, path: Path) -> type[ParsedFile] | None:
        if path.match("*.py"):
            return ParsedPythonFile
        elif path.match("view/*.xml"):
            return ParsedViewFile
        elif path.match("*.xml"):
            return ParsedXMLFile
        else:
            return None

    def _get_diagnostics(
        self, parsed: ParsedFile, ranges: list[CodeRange] | None = None
    ) -> list[Diagnostic]:
        return parsed.get_analyzer(self).analyze(ranges=ranges or [])

    def _get_completions(
        self, parsed: ParsedFile, line: int, column: int
    ) -> list[Diagnostic]:
        completioner = PythonCompletioner(parsed, self, line, column)
        try:
            completioner.analyze()
        except CompletionTargetFoundError:
            return generate_completions_from_model(completioner._target_model)
        else:
            return []

    def generate_module_diagnostics(
        self, module_name: str
    ) -> list[Diagnostic]:
        module = self._get_module(module_name)
        module_path = module.get_directory()
        diagnostics = []

        def to_analyze() -> Generator[Path, None, None]:
            for file_path in os.listdir(module_path):
                yield Path(file_path)
            if os.path.isdir(module_path / "tests"):
                for file_path in os.listdir(module_path / "tests"):
                    yield Path("tests") / file_path
            if os.path.isdir(module_path / "view"):
                for file_path in os.listdir(module_path / "view"):
                    if file_path.endswith(".xml"):
                        yield Path("view") / file_path

        for file_path in to_analyze():
            diagnostics += self.generate_diagnostics(module_path / file_path)

        return diagnostics


class Pool:
    supported_keys = {"model", "wizard"}

    def __init__(
        self,
        manager: PoolManager,
        key: tuple[str, ...],
        models: list[str],
        wizards: list[str],
    ) -> None:
        super().__init__()
        self._key: tuple[str, ...] = key
        self._manager: PoolManager = manager
        self.models: dict[str, PoolModel | None] = {x: None for x in models}
        self.wizards: dict[str, PoolModel | None] = {x: None for x in wizards}

    def get(self, name: str, kind: str = "model") -> PoolModel:
        referential = self.models if kind == "model" else self.wizards
        if name not in referential:
            raise UnknownModelException
        if referential[name] is not None:
            return referential[name]
        result = self._manager.fetch_model(self._key, name, kind)
        model = PoolModel(name, kind, result, self)
        referential[name] = model
        return model

    def fetch_super_information(
        self, model: PoolModel, function_name: str
    ) -> Any:
        return self._manager.fetch_super_information(
            self._key, model.type, model.name, function_name
        )

    def fetch_completions(self, model: PoolModel) -> list[Any]:
        return self._manager.fetch_completions(
            self._key, model.type, model.name
        )


class PoolModel:
    def __init__(
        self, name: str, type: str, data: dict[str, Any], pool: Pool
    ) -> None:
        super().__init__()
        self.name: str = name
        self._dir: set[str] = data["attrs"]
        self.fields: dict[str, Any] = data.get("fields", {})
        self.states: dict[str, Any] = data.get("states", {})
        self._completion_cache: dict[str, Any] | None = None
        self.type: str = type
        self._pool: Pool = pool

    def get_super_information(self, function_name: str):
        return self._pool.fetch_super_information(self, function_name)

    def has_attribute(self, name):
        return name in self._dir

    def get_completions(self):
        if self._completion_cache is not None:
            return self._completion_cache
        self._completion_cache = self._pool.fetch_completions(self)
        return self._completion_cache
