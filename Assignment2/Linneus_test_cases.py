import pprint as pp
from Linneaus3b import *

def test_insect():
    A = "insect"
    B = "organism"
    C = "creature"
    D = "living-thing"
    reset()

    store_article("insect", "an")
    store_article("organism", "an")
    store_article("creature", 'a')
    store_article("living-thing", 'a')

    print("\nSYNONYM Insect")
    store_synonym(A,A)
    print("\nSYNONYM Organism")
    store_synonym(B,B)
    print("\nSYNONYM Creature")
    store_synonym(C,C)
    print("\nSYNONYM Living Thing")
    store_synonym(D,D)


    print("\nFACT: A, B")
    store_isa_fact("insect", "organism")
    print("\nFACT: A, C")
    store_isa_fact("insect", "creature")
    print("\nFACT: C, D")
    store_isa_fact("creature","living-thing")
    print("\nFACT: B, C")
    store_isa_fact("organism","creature")
    print("\nFACT: D, B")
    store_isa_fact("living-thing","organism", True)


    pp.pprint(ISA[A])
    pp.pprint(SYNONYMS)

test_insect()