from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Symbol:
    index: int
    atom_code: str
    lexeme: str
    full_length: int
    truncated_length: int
    symbol_type: Optional[str]
    lines: List[int] = field(default_factory=list)

class SymbolTable:
    def __init__(self):
        self._symbols: dict[str, Symbol] = {}
        self._index_counter = 0

    def add(self, raw_lexeme: str, line: int, atom_code: str = "ID", symbol_type: Optional[str] = None) -> int:
        normalized = raw_lexeme.lower()
        filtered = ''.join(c for c in normalized if c.isalnum() or c == '_')
        truncated = filtered[:35]

        if normalized not in self._symbols:
            symbol = Symbol(
                index=self._index_counter,
                atom_code=atom_code,
                lexeme=truncated,
                full_length=len(filtered),
                truncated_length=len(truncated),
                symbol_type=symbol_type,
                lines=[line]
            )
            self._symbols[normalized] = symbol
            self._index_counter += 1
        else:
            symbol = self._symbols[normalized]
            if line not in symbol.lines and len(symbol.lines) < 5:
                symbol.lines.append(line)

        return self._symbols[normalized].index

    def get_all(self) -> List[Symbol]:
        return list(self._symbols.values())
