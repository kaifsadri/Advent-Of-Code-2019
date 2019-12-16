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

ORESPROVIDED = 1e12  # 1 trillion ores on hand.
FUELS = 5000  # a good guss for a point to start
overshot = False
while True:
    lefttomake = defaultdict(int, {"FUEL": FUELS})
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
    if oresneeded < ORESPROVIDED:
        if overshot:
            print(f"{FUELS} FUELs can be made with {ORESPROVIDED:.0f} OREs.")
            break
        else:
            FUELS += round((ORESPROVIDED - oresneeded) / oresneeded * FUELS)
    else:
        overshot = True
        FUELS -= 1
