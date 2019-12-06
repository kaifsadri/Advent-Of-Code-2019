with open("day05input") as f:
    puzzleinput = [int(i.strip()) for i in f.readline().split(",")]


def TEST(instructions):
    instructionpointer = 0
    while True:
        instruction = str(instructions[instructionpointer])
        optcode = int(instruction[-2:])
        param1mode = int(instruction[-3]) if 2 < len(instruction) else 0
        param2mode = int(instruction[-4]) if 3 < len(instruction) else 0

        if 99 == optcode:
            break
        elif 1 == optcode:
            param1 = (
                instructions[instructionpointer + 1]
                if 1 == param1mode
                else instructions[instructions[instructionpointer + 1]]
            )
            param2 = (
                instructions[instructionpointer + 2]
                if 1 == param2mode
                else instructions[instructions[instructionpointer + 2]]
            )
            instructions[instructions[instructionpointer + 3]] = param1 + param2
            instructionpointer += 4
            continue
        elif 2 == optcode:
            param1 = (
                instructions[instructionpointer + 1]
                if 1 == param1mode
                else instructions[instructions[instructionpointer + 1]]
            )
            param2 = (
                instructions[instructionpointer + 2]
                if 1 == param2mode
                else instructions[instructions[instructionpointer + 2]]
            )
            instructions[instructions[instructionpointer + 3]] = param1 * param2
            instructionpointer += 4
            continue
        elif 3 == optcode:
            instructions[instructions[instructionpointer + 1]] = int(
                input("Enter input: ")
            )
            instructionpointer += 2
            continue
        elif 4 == optcode:
            param1 = (
                instructions[instructionpointer + 1]
                if 1 == param1mode
                else instructions[instructions[instructionpointer + 1]]
            )
            print("Output is: ", param1)
            instructionpointer += 2
            continue
        elif 5 == optcode:
            param1 = (
                instructions[instructionpointer + 1]
                if 1 == param1mode
                else instructions[instructions[instructionpointer + 1]]
            )
            param2 = (
                instructions[instructionpointer + 2]
                if 1 == param2mode
                else instructions[instructions[instructionpointer + 2]]
            )
            if 0 != param1:
                instructionpointer = param2
            else:
                instructionpointer += 3
            continue
        elif 6 == optcode:
            param1 = (
                instructions[instructionpointer + 1]
                if 1 == param1mode
                else instructions[instructions[instructionpointer + 1]]
            )
            param2 = (
                instructions[instructionpointer + 2]
                if 1 == param2mode
                else instructions[instructions[instructionpointer + 2]]
            )
            if 0 == param1:
                instructionpointer = param2
            else:
                instructionpointer += 3
            continue
        elif 7 == optcode:
            param1 = (
                instructions[instructionpointer + 1]
                if 1 == param1mode
                else instructions[instructions[instructionpointer + 1]]
            )
            param2 = (
                instructions[instructionpointer + 2]
                if 1 == param2mode
                else instructions[instructions[instructionpointer + 2]]
            )
            if param1 < param2:
                instructions[instructions[instructionpointer + 3]] = 1
            else:
                instructions[instructions[instructionpointer + 3]] = 0
            instructionpointer += 4
            continue
        elif 8 == optcode:
            param1 = (
                instructions[instructionpointer + 1]
                if 1 == param1mode
                else instructions[instructions[instructionpointer + 1]]
            )
            param2 = (
                instructions[instructionpointer + 2]
                if 1 == param2mode
                else instructions[instructions[instructionpointer + 2]]
            )
            if param1 == param2:
                instructions[instructions[instructionpointer + 3]] = 1
            else:
                instructions[instructions[instructionpointer + 3]] = 0
            instructionpointer += 4
            continue
        else:
            print("Invalid instruction: ", optcode)
            break
    return


TEST(puzzleinput)
