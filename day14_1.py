from collections import defaultdict

with open("day14input") as f:
    puzzle = [line.strip() for line in f.readlines()]

reactions = dict()
for line in puzzle:
    left, right = line.split(" => ")
    moq, name = right.split(" ")
    recipe = list()
    for item in left.split(", "):
        qty, what = item.split(" ")
        recipe.append((int(qty), what))
    reactions[name] = [int(moq), recipe]

lefttomake = defaultdict(int, {"FUEL": 1})
onhand = defaultdict(int)
oresneeded = 0
while lefttomake:
    element, leftquantity = lefttomake.popitem()
    moq, recipe = reactions[element]
    moqs, remainder = divmod(leftquantity, moq)
    if remainder:
        onhand[element] = moq - remainder  # keep a record, not to make what we have
        moqs += 1
    for howmany, what in recipe:
        if what == "ORE":
            oresneeded += (
                moqs * howmany - onhand[what]
            )  # not double-count all the ORE currently accounted for
        else:
            lefttomake[what] += (
                moqs * howmany - onhand[what]
            )  # need to make what is missing
            onhand.pop(what)
print(oresneeded)
