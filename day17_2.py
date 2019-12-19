from collections import defaultdict
from itertools import combinations


class IntCodeComputer(object):
    def __init__(self, inputfile: str):
        with open(inputfile) as f:
            self.program = defaultdict(
                int,
                {
                    address: int(instruction)
                    for address, instruction in enumerate(
                        f.readline().strip().split(",")
                    )
                },
            )
        self.instructionaddress = 0
        self.running = 1
        self.relativebase = 0
        self.optcode = 99
        self.param1 = 0
        self.param2 = 0
        self.outaddress = 0
        self.commands = list()
        self.outputs = list()

    def parseinstruction(self, instruction: str):  # returns (optcode, param1, param2)
        self.optcode = int(instruction[-2:])
        self.param1 = 0
        self.param2 = 0
        self.outaddress = 0
        if self.optcode in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            param1mode = int(instruction[-3]) if 2 < len(instruction) else 0
            if 0 == param1mode:  # position mode
                self.param1 = self.program[self.program[self.instructionaddress + 1]]
            elif 1 == param1mode:  # parameter mode
                self.param1 = self.program[self.instructionaddress + 1]
            elif 2 == param1mode:  # relative mode
                self.param1 = self.program[
                    self.relativebase + self.program[self.instructionaddress + 1]
                ]
            if self.optcode in [1, 2, 5, 6, 7, 8]:
                param2mode = int(instruction[-4]) if 3 < len(instruction) else 0
                if 0 == param2mode:  # position mode
                    self.param2 = self.program[
                        self.program[self.instructionaddress + 2]
                    ]
                elif 1 == param2mode:  # parameter mode
                    self.param2 = self.program[self.instructionaddress + 2]
                elif 2 == param2mode:  # relative mode
                    self.param2 = self.program[
                        self.relativebase + self.program[self.instructionaddress + 2]
                    ]
        if self.optcode in [1, 2, 7, 8]:
            outputmode = int(instruction[-5]) if 4 < len(instruction) else 0
            if 0 == outputmode:  # position mode
                self.outaddress = self.program[self.instructionaddress + 3]
            elif 2 == outputmode:  # relative mode
                self.outaddress = (
                    self.relativebase + self.program[self.instructionaddress + 3]
                )
        elif self.optcode in [3]:
            outputmode = int(instruction[-3]) if 2 < len(instruction) else 0
            if 0 == outputmode:  # position mode
                self.outaddress = self.program[self.instructionaddress + 1]
            elif 2 == outputmode:  # relative mode
                self.outaddress = (
                    self.relativebase + self.program[self.instructionaddress + 1]
                )
        return

    def run(self):
        while True:
            self.parseinstruction(str(self.program[self.instructionaddress]))
            if 99 == self.optcode:
                return False
            elif 1 == self.optcode:
                self.program[self.outaddress] = self.param1 + self.param2
                self.instructionaddress += 4
                continue
            elif 2 == self.optcode:
                self.program[self.outaddress] = self.param1 * self.param2
                self.instructionaddress += 4
                continue
            elif 3 == self.optcode:
                self.program[self.outaddress] = ord(self.commands.pop(0))
                self.instructionaddress += 2
                continue
            elif 4 == self.optcode:  # paint, set  direction, move, continue
                self.outputs.append(self.param1)
                # print(chr(self.param1), end="")
                self.instructionaddress += 2
                continue
            elif 5 == self.optcode:
                if 0 != self.param1:
                    self.instructionaddress = self.param2
                else:
                    self.instructionaddress += 3
                continue
            elif 6 == self.optcode:
                if 0 == self.param1:
                    self.instructionaddress = self.param2
                else:
                    self.instructionaddress += 3
                continue
            elif 7 == self.optcode:
                if self.param1 < self.param2:
                    self.program[self.outaddress] = 1
                else:
                    self.program[self.outaddress] = 0
                self.instructionaddress += 4
                continue
            elif 8 == self.optcode:
                if self.param1 == self.param2:
                    self.program[self.outaddress] = 1
                else:
                    self.program[self.outaddress] = 0
                self.instructionaddress += 4
                continue
            elif 9 == self.optcode:
                self.relativebase += self.param1
                self.instructionaddress += 2
                continue
            else:
                print("Invalid instruction: ", self.soptcode)
                break
        return True

    def display(self):
        for i in self.outputs:
            print(chr(i), end="")


vacrobot = IntCodeComputer("day17input")
vacrobot.run()
# vacrobot.display()

U, D, L, R = (-1, 0), (1, 0), (0, -1), (0, 1)
char = {R: "R", L: "L"}


def neighbor(point, direction):
    return (point[0] + direction[0], point[1] + direction[1])


def turn(now, new):
    if (
        (now == R and new == U)
        or (now == U and new == L)
        or (now == L and new == D)
        or (now == D and new == R)
    ):
        return L
    if (
        (now == R and new == D)
        or (now == D and new == L)
        or (now == L and new == U)
        or (now == U and new == R)
    ):
        return R


# now pack the output
# line width:
width = vacrobot.outputs.index(10) + 1
grid = []
row = 0
for row in range(len(vacrobot.outputs) // width):
    grid.append(vacrobot.outputs[row * width : (row + 1) * width])
    grid[row].pop()  # trims the "10" in the end
    for i, o in enumerate(grid[row]):
        grid[row][i] = chr(o)


def indexgrid(grid, point):
    if point[1] < 0 or point[1] >= 41:
        return " "
    if point[0] < 0 or point[0] >= 39:
        return " "
    return grid[point[0]][point[1]]


vacstart = (0, 0)
for row in range(len(grid)):
    for column in range(width - 1):
        if "^" == grid[row][column]:
            vacstart = (row, column)
            break
location = vacstart
turn_steps = [[R, 0]]
direction = R
covered = [vacstart]
leg = 0
while True:
    EOL = True
    if indexgrid(grid, neighbor(location, direction)) == "#":
        turn_steps[leg][1] += 1
        location = neighbor(location, direction)
        covered.append(location)
    else:
        for newdir in {U, D, L, R}:
            if (
                indexgrid(grid, neighbor(location, newdir)) == "#"
                and neighbor(location, newdir) not in covered
                and direction != newdir
            ):
                turn_steps.append([turn(direction, newdir), 0])
                direction = newdir
                leg += 1
                EOL = False
                break
        if EOL:
            break

path = ",".join([char[x[0]] + str(x[1]) for x in turn_steps])
# This comes to R6,L6,L10,L8,L6,L10,L6,R6,L6,L10,L8,L6,L10,L6,R6,L8,L10,R6,R6,L6,L10,L8,L6,L10,L6,R6,L8,L10,R6,R6,L6,L10,R6,L8,L10,R6
# now start finding the longest elements
# since ther is a limit of 20 chars, it will stop there.
finalprogs = set()
substrings = set()
shift = 0
while shift < len(path) - 5:
    p = (path + ",")[shift:]
    for i in range(1, 19):
        ss = p[:i]
        if ss[0] not in "RL":
            continue
        if ss[-1] != ",":
            continue
        if ss not in substrings:
            substrings.add(ss.strip(","))
    p = p.replace(ss, " ")
    shift += 1

# now find a 3-pack of functions that works
progs = list()
for i in combinations(substrings, 3):
    p = path
    for _ in range(3):
        p = p.replace(i[_], " ")
    if p.replace(",", "").strip() == "":
        progs = i

progdefs = list(zip(["A", "B", "C"], progs))
progsequence = path
for i in progdefs:
    progsequence = progsequence.replace(i[1], i[0])


# now run the vac robot properly:
vacrobot = IntCodeComputer("day17input")
vacrobot.program[0] = 2
vacrobot.commands = list(
    progsequence
    + "\n"
    + progdefs[0][1].replace("R","R,").replace("L", "L,")
    + "\n"
    + progdefs[1][1].replace("R","R,").replace("L", "L,")
    + "\n"
    + progdefs[2][1].replace("R","R,").replace("L", "L,")
    + "\n"
    + "n"
    + "\n"
)
vacrobot.run()
# vacrobot.display()
print(f"The vac robot collecteed {vacrobot.outputs[-1]} units of dust.")
