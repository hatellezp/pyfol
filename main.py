#!/home/horacio/anaconda3/bin/python

import sys
from typing import List, Tuple

from lark import Lark

from fol_prover.parser import Declaration, Formula, Language, Role, TPTPParser

GRAMMAR_DIR = "grammars"


def load_basic_parser():
    grammar_file = GRAMMAR_DIR + "/" + "grammar.lark"

    with open(grammar_file, "r") as f:
        grammar_text = f.read()
    parser = Lark(grammar_text, lexer="basic", start="valid_start")
    return parser


def extract_formulae(lod: List[Declaration]) -> Tuple[List[Formula], List[Formula]]:
    accepted = [
        d.formula
        for d in lod
        if d.role not in [Role.Conjecture, Role.Negated_conjecture]
    ]
    to_prove = [
        d.formula for d in lod if d.role in [Role.Conjecture, Role.Negated_conjecture]
    ]

    return accepted, to_prove


if __name__ == "__main__":
    filename = sys.argv[1]
    filename = "sentences/" + filename

    with open(filename, "r") as f:
        file_content = f.read()

    parser = load_basic_parser()
    r = parser.parse(file_content)
    rr = TPTPParser().transform(r)

    formulae, to_prove = extract_formulae(rr)

    for f in formulae:
        print(f)
    print("========================")
    for f in to_prove:
        print(f)
