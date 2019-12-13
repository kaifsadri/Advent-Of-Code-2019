from collections import defaultdict


class Robot(object):
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
        self.grid = defaultdict(int)  # 0 unless a coordinate is set to 1
        self.location = (0, 0)
        self.outputwhat = 0  # 0 for paint, 1 for turn+move
        self.direction = "^"

    def turn(self, whichway):
        if 0 == whichway:  # LEFT
            if "^" == self.direction:
                self.direction = "<"
            elif "<" == self.direction:
                self.direction = "v"
            elif "v" == self.direction:
                self.direction = ">"
            elif ">" == self.direction:
                self.direction = "^"
            else:
                print("INVALID DIRECTION IN TURN!")
        elif 1 == whichway:  # RIGHT
            if "^" == self.direction:
                self.direction = ">"
            elif ">" == self.direction:
                self.direction = "v"
            elif "v" == self.direction:
                self.direction = "<"
            elif "<" == self.direction:
                self.direction = "^"
            else:
                print("INVALID DIRECTION IN TURN!")
        else:
            print("INVALID TURN IN TURN!")

    def move(self):
        if "^" == self.direction:
            self.location = (self.location[0], self.location[1] + 1)
        elif ">" == self.direction:
            self.location = (self.location[0] + 1, self.location[1])
        elif "v" == self.direction:
            self.location = (self.location[0], self.location[1] - 1)
        elif "<" == self.direction:
            self.location = (self.location[0] - 1, self.location[1])
        else:
            print("INVALID DIRECTION IN ROBOT!")

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
        if 1 != self.running:
            return
        while True:
            self.parseinstruction(str(self.program[self.instructionaddress]))
            if 99 == self.optcode:
                self.running = 0
                return
            elif 1 == self.optcode:
                self.program[self.outaddress] = self.param1 + self.param2
                self.instructionaddress += 4
                continue
            elif 2 == self.optcode:
                self.program[self.outaddress] = self.param1 * self.param2
                self.instructionaddress += 4
                continue
            elif 3 == self.optcode:
                self.program[self.outaddress] = self.grid[self.location]
                self.instructionaddress += 2
                continue
            elif 4 == self.optcode:  # paint, set  direction, move, continue
                if 0 == self.outputwhat:
                    self.outputwhat = 1
                    self.grid[self.location] = self.param1  # paint
                elif 1 == self.outputwhat:
                    self.outputwhat = 0
                    self.turn(self.param1)
                    self.move()
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


print("Part 1:")
robot = Robot("day11input")
robot.run()
print(len(robot.grid))

print("\nPart 2:")
robot = Robot("day11input")
robot.grid[robot.location] = 1
robot.run()
minx = min({coordinate[0] for coordinate in robot.grid.keys()})  # 0
maxx = max({coordinate[0] for coordinate in robot.grid.keys()})  # 42
miny = min({coordinate[1] for coordinate in robot.grid.keys()})  # -5
maxy = max({coordinate[1] for coordinate in robot.grid.keys()})  #
black = "█"
white = " "
for y in range(maxy, miny - 1, -1):  # becuse y goes from 0 to -5
    for x in range(minx, maxx + 1):
        print(white if 1 == robot.grid[x, y] else black, end="")
    print()
print()
