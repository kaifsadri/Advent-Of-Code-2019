from collections import defaultdict


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
        self.coordinates = list()
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
                if not self.coordinates:
                    # need to wait for input
                    return False
                else:
                    self.program[self.outaddress] = self.coordinates.pop(0)
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


n = 0
for x in range(50):
    for y in range(50):
        drone = IntCodeComputer("day19input")
        drone.coordinates = [x, y]
        drone.run()
        if drone.outputs == [1]:
            n += 1

print(n)

