with open("day06input") as f:
    puzzleinput = [i.strip().split(")") for i in f.readlines()]

planets = dict()
pathstocom = dict()

for planet, moon in puzzleinput:
    planets[moon] = planet


def scansystem(moon):
    if "COM" == planets[moon]:
        return ["COM"]
    else:
        return [planets[moon]] + scansystem(planets[moon])


for moon in planets.keys():
    pathstocom[moon] = scansystem(moon)

for planet in pathstocom["YOU"]:
    if planet in pathstocom["SAN"]:
        print(pathstocom["YOU"].index(planet) + pathstocom["SAN"].index(planet))
        break
