from abc import ABC, abstractmethod
from typing import List, Optional

from .formulae import *

RuleType = Enum("RuleType", ["E", "I"])


class AbcRule(ABC):
    @abstractmethod
    def apply(
        self, premises: Optional[List[Formula | Predicate]]
    ) -> Optional[List[Formula | Predicate]]:
        ...

    @abstractmethod
    def t(self) -> RuleType:
        ...


class AndI(AbcRule):
    def apply(
        self, premises: Optional[List[Formula | Predicate]]
    ) -> Optional[List[Formula | Predicate]]:
        if premises is None or len(premises) == 1:
            return None
        return [Formula(ftype=FormulaType.ANDF, content=premises, bounded=None)]

    def t(self) -> RuleType:
        return RuleType.I


class AndEL(AbcRule):
    def apply(
        self, premises: Optional[List[Formula | Predicate]]
    ) -> Optional[List[Formula | Predicate]]:
        if premises is None or len(premises) != 1:
            return None
        premise = premises[0]
        if premise.t() != FormulaType.ANDF:
            return None
        left = premise.content[0]
        return [left]

    def t(self) -> RuleType:
        return RuleType.E


class AndER(AbcRule):
    def apply(self, premises: Optional[List[Formula]]) -> Optional[List[Formula]]:
        if premises is None or len(premises) != 1:
            return None
        premise = premises[0]
        if premise.t() != FormulaType.ANDF:
            return None
        right = premise.content[1]
        return [right]

    def t(self) -> RuleType:
        return RuleType.E


class AndEGeneral(AbcRule):
    def apply(
        self, premises: Optional[List[Formula]], index: int = 0
    ) -> Optional[List[Formula]]:
        if premises is None or len(premises) != 1:
            return None
        premise = premises[0]
        if premise.t() != FormulaType.ANDF:
            return None
        right = premise.content[index]
        return [right]

    def t(self) -> RuleType:
        return RuleType.E
