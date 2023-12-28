"""A segment containing all of the original relocations."""
from __future__ import annotations

from ..bytearray import ByteArray
from ..relocation import SymbolRelocation
from ..section.relocation_table import RelocationTable
from ..symbol import Symbol
from .common import Flags


class RelocationsSegment:
    """The segment containing all of the original relocations."""

    def __init__(self, section_to_wrap: RelocationTable) -> None:
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
