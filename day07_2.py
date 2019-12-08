from itertools import permutations


class Amplifier:
    def __init__(self, phase):
        self.program = puzzle_program.copy()
        self.instructionaddress = 0
        self.running = 1
        self.output = 0
        self.run(phase)

    def run(self, inputs) -> int:
        if 1 != self.running:
            return
        new_input = True
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
                if new_input:
                    self.program[self.program[self.instructionaddress + 1]] = inputs
                    self.instructionaddress += 2
                    new_input = False
                    continue
                else:
                    return
            elif 4 == optcode:
                param1 = (
                    self.program[self.instructionaddress + 1]
                    if 1 == param1mode
                    else self.program[self.program[self.instructionaddress + 1]]
                )
                self.output = param1
                self.new_output = True
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
for sequence in permutations("56789", 5):
    ampchain = [Amplifier(int(phase)) for phase in sequence]
    thrust = 0
    while 0 != sum([a.running for a in ampchain]):
        for amp in ampchain:
            amp.run(thrust)
            thrust = amp.output
        if max_thrust < thrust:
            max_thrust = thrust

print(max_thrust)
