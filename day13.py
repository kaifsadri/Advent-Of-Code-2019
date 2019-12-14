from collections import defaultdict
from os import system

# Tile IDs:
empty = 0
wall = 1
block = 2
paddle = 3
ball = 4

# joystick positions:
neutral = 0
left = -1
right = 1


class ArcadeCabinet(object):
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
        self.outputs = list()
        self.screen = defaultdict(int)
        self.ball = 0
        self.paddle = 0

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
                self.updatescreen()
                self.printscreen()
                print(f"Finished with final score {self.screen[-1,0]}!")
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
                """ The game consists of keeping the paddle under the
                ball, so let's do just that."""
                self.updatescreen()
                self.printscreen()
                if self.ball > self.paddle:
                    self.program[self.outaddress] = 1
                elif self.paddle > self.ball:
                    self.program[self.outaddress] = -1
                else:
                    self.program[self.outaddress] = 0
                self.instructionaddress += 2
                self.outputs = list()
                continue
            elif 4 == self.optcode:  # paint, set  direction, move, continue
                self.outputs.append(self.param1)
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
        return

    def updatescreen(self):
        for i in range(0, len(self.outputs), 3):
            self.screen[(self.outputs[i], self.outputs[i + 1])] = self.outputs[i + 2]
        return

    def printscreen(self):
        system("clear")
        minx = min({coordinate[0] for coordinate in self.screen.keys()})
        maxx = max({coordinate[0] for coordinate in self.screen.keys()})
        miny = min({coordinate[1] for coordinate in self.screen.keys()})
        maxy = max({coordinate[1] for coordinate in self.screen.keys()})
        for y in range(miny, maxy + 1):
            for x in range(minx, maxx + 1):
                # Tile IDs:
                char = " "
                if wall == self.screen[(x, y)]:
                    char = "█"
                elif block == self.screen[(x, y)]:
                    char = "⊡"
                elif paddle == self.screen[(x, y)]:
                    char = "▁"
                    self.paddle = x
                elif ball == self.screen[(x, y)]:
                    char = "⏺"
                    self.ball = x
                # elif empty == self.screen[(x, y)]:
                #     char = " "
                print(char, end="")
            print()
        print(" " + "█" * (maxx + 1))
        print(f'{f"SCORE: {self.screen[-1,0]}":^{maxx+1}}')


# Part 1:
cabinet = ArcadeCabinet("day13input")
cabinet.run()

numblocks = 0
for i in range(0, len(cabinet.outputs), 3):
    if cabinet.outputs[i + 2] == block:
        numblocks += 1

print(f"Part 1: number of blocks on the screen is {numblocks}.")
print(f"{'Press any key to move to part 2':-^50}")
input()

# Part 2:
cabinet = ArcadeCabinet("day13input")
cabinet.program[0] = 2
cabinet.run()
