from itertools import combinations
from math import gcd

# puzzle input
"""
input:
<x=-4, y=-14, z=8>
<x=1, y=-8, z=10>
<x=-15, y=2, z=1>
<x=-17, y=-17, z=16>
"""


class Moon:
    def __init__(self, location: list):
        self.location = location
        self.velocity = [0, 0, 0]
        return


# Part 1
Io = Moon([-4, -14, 8])
Europa = Moon([1, -8, 10])
Ganymede = Moon([-15, 2, 1])
Callisto = Moon([-17, -17, 16])
moons = [Io, Europa, Ganymede, Callisto]

steps = 1000
for step in range(steps):
    # apply gravity:
    for pair in combinations(moons, 2):
        for dimension in range(3):
            # there is no condition for equality, so it will not change velocities in that case
            if pair[0].location[dimension] > pair[1].location[dimension]:
                pair[0].velocity[dimension] -= 1
                pair[1].velocity[dimension] += 1
            elif pair[0].location[dimension] < pair[1].location[dimension]:
                pair[0].velocity[dimension] += 1
                pair[1].velocity[dimension] -= 1
    # apply velocity:
    for moon in moons:
        for dimension in range(3):
            moon.location[dimension] += moon.velocity[dimension]

total_energy = 0
for moon in moons:
    total_energy += sum([abs(moon.location[i]) for i in range(3)]) * sum(
        [abs(moon.velocity[i]) for i in range(3)]
    )

print(f"Part 1: Total energy after 1000 steps is {total_energy}.")


# Part 2
Io = Moon([-4, -14, 8])
Europa = Moon([1, -8, 10])
Ganymede = Moon([-15, 2, 1])
Callisto = Moon([-17, -17, 16])
moons = [Io, Europa, Ganymede, Callisto]

# gravity and speed changes happen independently for each dimension,
# so one can find the repeating steps fr each dimension,
# then find the smallest common multiplier of the 3 dimensions.
stepstorepeating_position = [0, 0, 0]
for dimension in range(3):
    positions = set()
    steps = 0
    while True:
        # apply gravity:
        for pair in combinations(moons, 2):
            # there is no condition for equality, so it will not change velocities in that case
            if pair[0].location[dimension] > pair[1].location[dimension]:
                pair[0].velocity[dimension] -= 1
                pair[1].velocity[dimension] += 1
            elif pair[0].location[dimension] < pair[1].location[dimension]:
                pair[0].velocity[dimension] += 1
                pair[1].velocity[dimension] -= 1
        # apply velocity:
        for moon in moons:
            moon.location[dimension] += moon.velocity[dimension]
        hash_id = hash(tuple([tuple(moon.location + moon.velocity) for moon in moons]))
        if hash_id in positions:
            stepstorepeating_position[dimension] = steps
            break
        else:
            positions.add(hash_id)
            steps += 1

# now find the least common multiple of the steps
solution = int(
    stepstorepeating_position[0]
    * stepstorepeating_position[1]
    / gcd(stepstorepeating_position[0], stepstorepeating_position[1])
)
solution = int(
    stepstorepeating_position[2]
    * solution
    / gcd(solution, stepstorepeating_position[2])
)
print(f"Part 2: The system reaches a previous state after {solution} steps.")
