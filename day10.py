from math import atan, pi


def intermediatepoints(a: tuple, b: tuple) -> set:
    result = set()
    minx = min(a[0], b[0])
    maxx = max(a[0], b[0])
    miny = min(a[1], b[1])
    maxy = max(a[1], b[1])
    if a[0] == b[0]:
        return set([(a[0], y) for y in range(miny + 1, maxy)])
    if a[1] == b[1]:
        return set([(x, a[1]) for x in range(minx + 1, maxx)])
    for x in range(minx + 1, maxx):
        for y in range(miny + 1, maxy):
            try:
                if (x - a[0]) / (y - a[1]) == (b[0] - a[0]) / (b[1] - a[1]):
                    result.add((x, y))
            except ZeroDivisionError:
                pass
    return result


def findvisibleasteroids(monitorstationlocation, belt) -> set:
    asteroidsvisible = set()
    for thing in belt:
        if 0 == len(
            asteroidbelt.intersection(intermediatepoints(monitorstationlocation, thing))
        ):
            asteroidsvisible.add(thing)
    return asteroidsvisible - {monitorstationlocation}


asteroidbelt = set()
with open("day10input") as f:
    for y, line in enumerate(f.readlines()):
        for x, what in enumerate(line):
            if "#" == what:
                asteroidbelt.add((x, y))

monitorstation = tuple()
maxtargets = 0
maxvisibleasteroids = set()
for asteroid in asteroidbelt:
    visibleasteroids = findvisibleasteroids(asteroid, asteroidbelt)
    targets = len(visibleasteroids)
    if targets > maxtargets:
        maxvisibleasteroids = visibleasteroids
        maxtargets = targets
        monitorstation = asteroid


print("\nPart 1: ")
print(f"Monitor station to be at {monitorstation}.")
print(f"{maxtargets} directly visible asteroids from this location.")

# Start of part 2
monitorstation = monitorstation
vaporizedasteroids = list()

maxvisibleasteroids = findvisibleasteroids(monitorstation, asteroidbelt)
while len(maxvisibleasteroids) != 0:
    # find one round's worth of asteroids
    processedtargets = dict()
    for target in maxvisibleasteroids:
        distance = (
            (
                (target[1] - monitorstation[1]) ** 2
                + (target[0] - monitorstation[0]) ** 2
            )
            ** 0.5,
            3,
        )
        if target[0] == monitorstation[0]:
            if target[1] > monitorstation[1]:
                angle = 180
            else:
                angle = 0
        elif target[0] > monitorstation[0]:
            angle = (
                90
                - atan(
                    (monitorstation[1] - target[1]) / (target[0] - monitorstation[0])
                )
                * 180
                / pi
            )
        elif target[0] < monitorstation[0]:
            angle = (
                270
                - atan(
                    (monitorstation[1] - target[1]) / (target[0] - monitorstation[0])
                )
                * 180
                / pi
            )
        else:
            print("ERROR IN THIS CODE")
        processedtargets[target] = angle

    # now vaporize this round, keeping score
    processedtargets = sorted(
        processedtargets.keys(), key=lambda x: processedtargets[x]
    )
    for target in processedtargets:
        vaporizedasteroids.append(target)
        asteroidbelt.remove(target)
    # Get ready for the next round
    maxvisibleasteroids = findvisibleasteroids(monitorstation, asteroidbelt)

print("\nPart 2: ")
print(f"The 200th asteroid to be vaporized is at {vaporizedasteroids[199]}.\n")

