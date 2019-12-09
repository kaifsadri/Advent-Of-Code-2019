with open("day08input", "r") as f:
    puzzleinput = f.readline().strip()

width = 25
height = 6
layersize = width * height

black = "█"
white = " "

answer = list()

for i in range(layersize):
    pixelstack = puzzleinput[i::layersize]
    for pixel in pixelstack:
        if pixel != "2":
            answer.append(black if "1" == pixel else white)
            break

for i in range(height):
    print("".join(answer[i * width : (i + 1) * width]))
