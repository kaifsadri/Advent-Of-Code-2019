with open("day08input") as f:
    puzzleinput = f.readline().strip()

wide = 25
tall = 6
layersize = wide * tall

minzeros = layersize
num1bynum2 = 0

# go frame by frame
for f in range(len(puzzleinput) // layersize):
    layer = puzzleinput[f * layersize : (f + 1) * layersize]
    zeros = layer.count("0")
    # print(zeros)
    if zeros < minzeros:
        minzeros = zeros
        num1bynum2 = layer.count("1") * layer.count("2")

print(num1bynum2)
