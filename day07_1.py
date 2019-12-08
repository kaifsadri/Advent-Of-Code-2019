from itertools import permutations


class Amplifier:
    def __init__(self, inputs: list):
        self.inputs = inputs
        self.output = 0
        self.program = puzzle_program.copy()
        self.instructionaddress = 0
        self.running = 1

    def run(self):
        if 1 != self.running:
            return
        while True:
            instruction = str(self.program[self.instructionaddress])
            optcode = int(instruction[-2:])
            param1mode = int(instruction[-3]) if 2 < len(instruction) else 0
            param2mode = int(instruction[-4]) if 3 < len(instruction) else 0
            if 99 == optcode:
                self.running = 0
                return
            elif 1 == optcode:
                param1 = (
                    self.program[self.instructionaddress + 1]
                    if 1 == param1mode
                    else self.program[self.program[self.instructionaddress + 1]]
                )
                param2 = (
                    self.program[self.instructionaddress + 2]
                    if 1 == param2mode
                    else self.program[self.program[self.instructionaddress + 2]]
                )
                self.program[self.program[self.instructionaddress + 3]] = (
                    param1 + param2
                )
                self.instructionaddress += 4
                continue
            elif 2 == optcode:
                param1 = (
                    self.program[self.instructionaddress + 1]
                    if 1 == param1mode
                    else self.program[self.program[self.instructionaddress + 1]]
                )
                param2 = (
                    self.program[self.instructionaddress + 2]
                    if 1 == param2mode
                    else self.program[self.program[self.instructionaddress + 2]]
                )
                self.program[self.program[self.instructionaddress + 3]] = (
                    param1 * param2
                )
                self.instructionaddress += 4
                continue
            elif 3 == optcode:
                self.program[
                    self.program[self.instructionaddress + 1]
                ] = self.inputs.pop()
                self.instructionaddress += 2
                continue
            elif 4 == optcode:
                param1 = (
                    self.program[self.instructionaddress + 1]
                    if 1 == param1mode
                    else self.program[self.program[self.instructionaddress + 1]]
                )
                self.output = param1
                self.instructionaddress += 2
                return
            elif 5 == optcode:
                param1 = (
                    self.program[self.instructionaddress + 1]
                    if 1 == param1mode
                    else self.program[self.program[self.instructionaddress + 1]]
                )
                param2 = (
                    self.program[self.instructionaddress + 2]
                    if 1 == param2mode
                    else self.program[self.program[self.instructionaddress + 2]]
                )
                if 0 != param1:
                    self.instructionaddress = param2
                else:
                    self.instructionaddress += 3
                continue
            elif 6 == optcode:
                param1 = (
                    self.program[self.instructionaddress + 1]
                    if 1 == param1mode
                    else self.program[self.program[self.instructionaddress + 1]]
                )
                param2 = (
                    self.program[self.instructionaddress + 2]
                    if 1 == param2mode
                    else self.program[self.program[self.instructionaddress + 2]]
                )
                if 0 == param1:
                    self.self.instructionaddress = param2
                else:
                    self.instructionaddress += 3
                continue
            elif 7 == optcode:
                param1 = (
                    self.program[self.instructionaddress + 1]
                    if 1 == param1mode
                    else self.program[self.program[self.instructionaddress + 1]]
                )
                param2 = (
                    self.program[self.instructionaddress + 2]
                    if 1 == param2mode
                    else self.program[self.program[self.instructionaddress + 2]]
                )
                if param1 < param2:
                    self.program[self.program[self.instructionaddress + 3]] = 1
                else:
                    self.program[self.program[self.instructionaddress + 3]] = 0
                self.instructionaddress += 4
                continue
            elif 8 == optcode:
                param1 = (
                    self.program[self.instructionaddress + 1]
                    if 1 == param1mode
                    else self.program[self.program[self.instructionaddress + 1]]
                )
                param2 = (
                    self.program[self.instructionaddress + 2]
                    if 1 == param2mode
                    else self.program[self.program[self.instructionaddress + 2]]
                )
                if param1 == param2:
                    self.program[self.program[self.instructionaddress + 3]] = 1
                else:
                    self.program[self.program[self.instructionaddress + 3]] = 0
                self.instructionaddress += 4
                continue
            else:
                print("Invalid instruction: ", optcode)
                break


with open("day07input") as f:
    puzzle_program = [int(i.strip()) for i in f.readline().split(",")]

max_thrust = 0
for sequence in permutations("01234", 5):
    thrust = 0
    for phase in sequence:
        amp = Amplifier([thrust, int(phase)])
        amp.run()
        thrust = amp.output
    if max_thrust < thrust:
        max_thrust = thrust

print(max_thrust)
