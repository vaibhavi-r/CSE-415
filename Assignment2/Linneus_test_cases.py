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
        "That's all I know about \'turtle\'."]),
]

CASE2 = [
    ("A BugsBunny is a cartoon.", None),
    ("A DaffyDuck is a cartoon.", None),
    ("A BugsBunny is a rabbit.", None),
    ("A DaffyDuck is a duck.", None),
    ("A duck is a bird.", None),
    ("A bird is an animal.", None),
    ("A rabbit is a mammal.", None),
    ("A mammal is an animal.", None),
    ("Is a BugsBunny an animal?", ["Yes, it is."]),
    ("Is a DaffyDuck a rabbit?", ["No, as far as I have been informed, it is not."]),
    ("Tell me what you know about \'DaffyDuck\', with justification.", [
        "A DaffyDuck is a cartoon; you told me that directly.",
        "A DaffyDuck is a duck; you told me that directly.",
        "A DaffyDuck is a bird, because a DaffyDuck is a duck and a duck is a bird",
        "A DaffyDuck is an animal, because a DaffyDuck is a duck, a duck is a bird, and a bird is an animal.",
        "That's all I know about \'DaffyDuck\'."]),
    ("Tell me what you know about \'rabbit\', with justification.", [
        "A rabbit is a mammal; you told me that directly.",
        "A rabbit is an animal, because a rabbit is a mammal and a mammal is an animal.",
        "A rabbit is something more general than a BugsBunny, because a BugsBunny is a rabbit.",
        "That's all I know about \'rabbit\'."]),
]
