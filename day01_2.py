def calc_fuel(mass):
    if 9 > mass:
        fuel = 0
    else:
        fuel = (mass // 3) - 2
        fuel += calc_fuel(fuel)
    return fuel


with open("day01input") as f:
    inputarray = f.readlines()

totalfuel = 0

for i in inputarray:
    totalfuel += calc_fuel(int(i))

print(totalfuel)
