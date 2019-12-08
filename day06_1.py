from collections import defaultdict

with open("day06input") as f:
    puzzleinput = [i.strip().split(")") for i in f.readlines()]

planetarysystem = defaultdict(set)
orbitcounts = defaultdict(int)

for planet, moon in puzzleinput:
    planetarysystem[planet].add(moon)


def scansystem(planet):
    for moon in planetarysystem[planet]:
        orbitcounts[moon] = orbitcounts[planet] + 1
        scansystem(moon)


scansystem("COM")
print(sum(orbitcounts.values()))
