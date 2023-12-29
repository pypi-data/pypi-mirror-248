from __future__ import annotations

from contextvars import ContextVar

from .spec import FormattedPath, PathSpec, SourceSpec


class _SuffixNode:
    bound: tuple[SourceSpec, PathSpec] | None

    def __init__(self) -> None:
        self.bound = None
        self.nxt: dict[str, _SuffixNode] = {}

    def insert(self, frags: list[str], index: int = 0) -> _SuffixNode:
        if index == len(frags):
            return self
        nxt = self.nxt.setdefault(frags[index], _SuffixNode())
        return nxt.insert(frags, index + 1)

    def lookup(
        self, frags: list[str], index: int = 0
    ) -> tuple[int, tuple[SourceSpec, PathSpec] | None]:
        res = index, self.bound
        if index < len(frags):
            if nxt_nd := self.nxt.get(frags[index], None):
                if (lookup_res := nxt_nd.lookup(frags, index + 1)) and lookup_res[1]:
                    return lookup_res
        return res


class _PrefixNode:
    suffix: _SuffixNode | None

    def __init__(self) -> None:
        self.suffix = None
        self.nxt: dict[str, _PrefixNode] = {}

    def insert(self, frags: list[str], index: int = 0) -> _SuffixNode:
        if index == len(frags):
            if not self.suffix:
                self.suffix = _SuffixNode()
            return self.suffix
        nxt = self.nxt.setdefault(frags[index], _PrefixNode())
        return nxt.insert(frags, index + 1)

    def lookup(
        self, frags: list[str], index: int = 0
    ) -> tuple[tuple[SourceSpec, PathSpec], FormattedPath] | None:
        if index < len(frags) and (nxt_nd := self.nxt.get(frags[index], None)):
            if lookup_res := nxt_nd.lookup(frags, index + 1):
                return lookup_res
        if self.suffix:
            suffix_ind, spec = self.suffix.lookup(list(reversed(frags[index:])))
            if spec:
                src_spec, path_spec = spec
                parts = (
                    src_spec.section.prefix
                    + frags[index : -suffix_ind or None]
                    + src_spec.section.suffix
                )
                if formatted := path_spec.format(parts):
                    return spec, formatted


def insert(src: SourceSpec, path: PathSpec) -> None:
    prefix, suffix = src.prefix, src.suffix
    target_nd = _root.get().insert(prefix).insert(list(reversed(suffix)))
    if target_nd.bound:
        raise ValueError(
            f"{'.'.join(prefix + ['*'] + suffix)} is already bound to {target_nd.bound}"
        )
    target_nd.bound = (src, path)


def lookup(domains: list[str]) -> FormattedPath:
    if res := _root.get().lookup(domains):
        return res[1]
    raise ValueError(f"Unable to lookup {'.'.join(domains)}")


_root: ContextVar[_PrefixNode] = ContextVar("kayaku.__root__", default=_PrefixNode())
