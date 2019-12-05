with open("day02input") as f:
    InputArray = [int(i) for i in f.readline().split(",")]

InputArray[1] = 12
InputArray[2] = 2
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

print(InputArray[0])
