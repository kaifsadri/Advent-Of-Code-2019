with open("day02input") as f:
    Input = [int(i.strip()) for i in f.readline().split(",")]


def RunProgram(InA, Noun, Verb):
    InputArray = InA.copy()
    InputArray[1] = Noun
    InputArray[2] = Verb
    PositionCode = 0
    while True:
        OptCode = InputArray[PositionCode]
        if 99 == OptCode:
            break
        elif 1 == OptCode:
            InputArray[InputArray[PositionCode + 3]] = (
                InputArray[InputArray[PositionCode + 1]]
                + InputArray[InputArray[PositionCode + 2]]
            )
        elif 2 == OptCode:
            InputArray[InputArray[PositionCode + 3]] = (
                InputArray[InputArray[PositionCode + 1]]
                * InputArray[InputArray[PositionCode + 2]]
            )
        PositionCode += 4
    return InputArray[0]


for i in range(100):
    for j in range(100):
        if 19690720 == RunProgram(Input, i, j):
            print(100 * i + j)
