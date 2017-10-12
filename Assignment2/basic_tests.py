import Linneaus3b as lin
CASE1 = [
        ("A turtle is a reptile.", None),
        ("A turtle is a shelled-creature.", None),
        ("A reptile is an animal.", None),
        ("An animal is a thing.", None),
        ("Is a turtle a reptile.", ["Yes, it is."]),
        ("Is a turtle an animal.", ["Yes, it is."]),
        ("What is a turtle?", ["A turtle is a reptile."]),
        ("Why is a turtle an animal?", ["Because a turtle is a reptile, and a reptile is an animal."]),
        ("Why is an animal a reptile?", ["But that's not true, as far as I know!"]),
        ("Tell me what you know about \'turtle\', with justification.", [
            "A turtle is a reptile; you told me that directly.",
            "A turtle is a shelled-creature; you told me that directly.",
            "A turtle is an animal, because a turtle is a reptile and a reptile is an animal.",
            "A turtle is a thing, because a turtle is a reptile, a reptile is an animal, and an animal is a thing.",
            "That's all I know about \'turtle\'."])
        ]


def initialize_case():
    statements = ["A turtle is a reptile.",
                  "A turtle is a shelled-creature.",
                  "A reptile is an animal.",
                  "An animal is a thing."
                  ]
    lin.reset()
    for st in statements:
        lin.process(st)

    x= "rabbit"
    #lin.isa_bfs("thing")
    lin.includes_bfs("thing")
    print("That's all I know about \'%s\'."%x)

initialize_case()


