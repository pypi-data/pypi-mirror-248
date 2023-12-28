"""A segment containing all of the original symbols."""
from __future__ import annotations
from typing import Iterable

from ..bytearray import ByteArray
from ..relocation import SymbolRelocation
from ..section.symbol_table import SymbolTable
from ..symbol import Symbol
from .common import Flags, Segment


class SymbolsSegment:
    """The segment containing all of the original symbols."""

    def __init__(self, section_to_wrap: SymbolTable) -> None:
        self._section = section_to_wrap

    def data(self) -> ByteArray | None:
        """The data contained in the segment, or None if the
        segment should be zero-initialized.
        """
        return None

    def symbols(self, offset: int) -> tuple[Symbol, ...]:
        """All symbols in the segment."""
        return tuple()

    @property
    def byte_size(self) -> int:
        """The size of a single byte in the segment."""
        return 0

    @property
    def size(self) -> int:
        """The size of the segment in its own bytes."""
        return 0

    @property
    def flags(self) -> Flags:
        """The flags of the segment."""
        return Flags(executable=False, readable=True, writable=False, special=True)

    @property
    def relocations(self) -> list[SymbolRelocation]:
        """A list of relocations in the segment."""
        return []

    def symbols_from(self, segment: Segment, offset: int) -> Iterable[Symbol]:
        """Return all symbols from the given segment and offset.

        Args:
            segment (Segment): The segment to return the symbols to.
            offset (int): The offset to return the symbols to.

        Returns:
            tuple[Symbol, ...]: The symbols from the given segment and offset.
        """
        for symbol in self._section._symbols:
            if offset <= symbol.location.offset < offset + segment.size:
                yield symbol
