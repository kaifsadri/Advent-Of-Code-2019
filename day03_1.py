Directions = [[], []]

with open("day03input") as f:
    Directions[0] = [section.strip() for section in f.readline().split(",")]
    Directions[1] = [section.strip() for section in f.readline().split(",")]


def directions2pointset(steps):
    points = set()
    location = [0, 0]
    for s in steps:
        direction = s[0]
        numsteps = int(s[1:])
        for i in range(numsteps):
            if "U" == direction:
                location[1] += 1
            elif "D" == direction:
                location[1] -= 1
            elif "L" == direction:
                location[0] -= 1
            elif "R" == direction:
                location[0] += 1
            points.add(tuple(location.copy()))
    return points


wire0 = directions2pointset(Directions[0])
wire1 = directions2pointset(Directions[1])

intersections = list(wire0.intersection(wire1))
distances = [abs(i[0]) + abs(i[1]) for i in intersections]

print(min(distances))
