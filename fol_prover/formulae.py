from enum import Enum
from typing import List, Optional, Union

TermType = Enum("TermType", ["VAR", "CONST", "FUN"])


class FunApp:
    name: str
    content: List["Term"]

    def __init__(self, name: str, content: List[Union[str, "FunApp"]]) -> None:
        self.name = name
        self.content = content

    def __str__(self) -> str:
        values = ", ".join([str(v) for v in self.content])
        return f"{self.name}({values})"

    def t(self) -> TermType:
        return TermType.FUN


class Term:
    def __init__(self, ttype: TermType, content: Union[str, FunApp]) -> None:
        self.ttype = ttype
        self.content = content

    def type(self):
        return self.ttype

    def __str__(self):
        return str(self.content)

    def t(self) -> TermType:
        return self.ttype


FormulaType = Enum(
    "FormulaType",
    [
        "PRED",
        "EQUA",
        "INEQ",
        "NOTF",
        "ANDF",
        "ORF",
        "IMPF",
        "IMPBF",
        "EQUIF",
        "ALLF",
        "EXISF",
        "BOT",
        "TOP",
    ],
)


class Predicate:
    def __init__(self, name: str, content: List[Term]) -> None:
        self.name = name
        self.content = content

    def __str__(self) -> str:
        if not len(self.content):
            return f"<{self.name}>"
        values = ", ".join([str(v) for v in self.content])
        return f"{self.name}({values})"

    def t(self) -> FormulaType:
        return FormulaType.PRED


class Formula:
    def __init__(
        self,
        ftype: FormulaType,
        content: List[Union[Predicate, "Formula"]],
        bounded: Optional[List[Term]] = None,
    ) -> None:
        self.ftype = ftype
        self.content = content
        self.bounded = bounded

    def t(self) -> FormulaType:
        return self.ftype

    def var_is_bound(self, var: Union[Term, FunApp]):
        if var.t() != TermType.VAR:
            return False
        if self.t() not in (FormulaType.ALLF, FormulaType.EXISF):
            return False
        if self.bounded is None:
            return False
        return var in self.bounded

    def __str__(self) -> str:
        match self.ftype:
            case FormulaType.BOT:
                return "⊥"
            case FormulaType.TOP:
                return "T"
            case FormulaType.PRED:
                return str(self.content[0])
            case FormulaType.INEQ:
                return f"{self.content[0]} != {self.content[1]}"
            case FormulaType.EQUA:
                return f"{self.content[0]} = {self.content[1]}"
            case FormulaType.ANDF:
                res = " & ".join([str(c) for c in self.content])
                return f"({res})"
            case FormulaType.ORF:
                res = " | ".join([str(c) for c in self.content])
                return f"({res})"
            case FormulaType.IMPF:
                return f"{self.content[0]} ⇒ {self.content[1]}"
            case FormulaType.EQUIF:
                return f"{self.content[0]} ⇔ {self.content[1]}"
            case FormulaType.ALLF:
                bounded = ", ".join([str(v) for v in self.bounded])
                return f"∀ [{bounded}]: {self.content[0]}"
            case FormulaType.EXISF:
                bounded = ", ".join([str(v) for v in self.bounded])
                return f"∃ [{bounded}]: {self.content[0]}"
            case FormulaType.NOTF:
                return f"~ ({self.content[0]})"
            case _:
                print(self.ftype)
                raise NotImplementedError


Role = Enum(
    "Role",
    [
        "Conjecture",
        "Axiom",
        "Theorem",
        "Lemma",
        "Hypothesis",
        "Definition",
        "Assumption",
        "Corollary",
        "Negated_conjecture",
        "Plain",
        "Type",
        "Interpretation",
    ],
)
Language = Enum("Language", ["FOF", "CNF", "THF", "TFF", "TCF", "TPI"])


class Declaration:
    def __init__(self, language: str, name: str, role: str, formula: Formula) -> None:
        language = language.upper()
        try:
            self.language = Language[language]
        except KeyError as e:
            raise Exception(f"The language is not known: {e}")

        role = role.capitalize()
        try:
            self.role = Role[role]
        except KeyError as e:
            raise Exception(f"The role is not known: {e}")

        self.name = name
        self.formula = formula

    def __str__(self) -> str:
        res = f"""
{self.language}({self.name}, {self.role},
{self.formula}
)
"""
        return res
