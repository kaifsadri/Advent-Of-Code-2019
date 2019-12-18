with open("day16input") as f:
    puzzle = f.readline().strip()

msg = [
    int(puzzle[i % len(puzzle)]) for i in range(int(puzzle[0:7]), len(puzzle) * 10000)
]

for phase in range(100):
    s = sum(msg) % 10
    for i in range(len(msg)):
        buf = s
        s -= msg[i]
        msg[i] = buf % 10

print("".join(str(i) for i in msg[0:8]))
