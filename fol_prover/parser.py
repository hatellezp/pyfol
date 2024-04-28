from lark import Transformer
from lark.tree import Tree

from .formulae import *


class TPTPParser(Transformer):
    def _to_formula(self, s, ftype: FormulaType):
        content: List[Formula | Tree] = [self._go_down_fof(si) for si in s]
        content = [c.children[0] if self._is_tree(c) else c for c in content]
        formula = Formula(ftype=ftype, content=content)
        return formula

    def _is_tree(self, s):
        return type(s) is Tree

    def _go_down_fof(self, s) -> Union[Tree, Formula]:
        # if is tree and s.data == fof
        if self._is_tree(s) and s.data == "fof_f":
            s = s.children[0]
            return self._go_down_fof(s)
        return s

    def single_quoted_word(self, s):
        return s[0].value[1:-1]

    def lowercase_word(self, s):
        res = "".join([str(si) for si in s])
        return res

    def number(self, n):
        (n,) = n
        return int(n)

    def variable(self, s):
        res = "".join([str(si[0]) for si in s])
        return Term(ttype=TermType.VAR, content=res)

    def literal(self, s):
        return Term(ttype=TermType.CONST, content=s[0])

    def name(self, s):
        return s[0]

    def predicate(self, s):
        name, terms = s[0].children[0], s[1:]
        terms = [t.children[0] for t in terms]
        predicate = Predicate(name=name, content=terms)
        formula = Formula(ftype=FormulaType.PRED, content=[predicate])
        return formula

    def fun_appl(self, s):
        name, terms = s[0].children[0], s[1:]
        terms = [t.children[0] for t in terms]
        fun_appl = FunApp(name=name, content=terms)
        return fun_appl

    def fof_equality(self, s):
        return self._to_formula(s, FormulaType.EQUA)

    def fof_inequality(self, s):
        return self._to_formula(s, FormulaType.INEQ)

    def fof_not_f(self, s):
        res = self._go_down_fof(s[0])
        return Formula(ftype=FormulaType.NOTF, content=[res])

    def fof_and_f(self, s):
        return self._to_formula(s, FormulaType.ANDF)

    def fof_or_f(self, s):
        return self._to_formula(s, FormulaType.ORF)

    def fof_equivalent_f(self, s):
        return self._to_formula(s, FormulaType.EQUIF)

    def fof_implies_f(self, s):
        return self._to_formula(s, FormulaType.IMPF)

    def fof_implies_backward_f(self, s):
        formula = self._to_formula(s, FormulaType.IMPF)
        formula.content.reverse()
        return formula

    def fof_all_f(self, s):
        index = s.index(":")
        vars, rest = s[:index], s[(index + 1) :]
        formula = [self._go_down_fof(si) for si in rest]
        formula = Formula(ftype=FormulaType.ALLF, content=formula, bounded=vars)
        return formula

    def fof_exists_f(self, s):
        index = s.index(":")
        vars, rest = s[:index], s[(index + 1) :]
        formula = [self._go_down_fof(si) for si in rest]
        formula = Formula(ftype=FormulaType.EXISF, content=formula, bounded=vars)
        return formula

    fof = lambda self, _: "fof"
    thf = lambda self, _: "thf"
    tff = lambda self, _: "tff"
    cnf = lambda self, _: "cnf"
    axiom = lambda self, _: "axiom"
    conjecture = lambda self, _: "conjecture"

    def formula(self, s):
        return s[0].children[0]

    def declaration(self, s):
        language, name, role, formula = s[0], s[1], s[2], s[3]
        return Declaration(language=language, name=name, role=role, formula=formula)

    def valid_start(self, s):
        return s
