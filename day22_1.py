with open("day22input", "r") as f:
    puzzle = [line.strip() for line in f.readlines()]


def deal_new(d: list):
    return list(reversed(d))


def cut(d: list, n: int):
    if n > 0:
        return d[n:] + d[:n]
    else:
        return d[n:] + d[0:n]


def deal_inc(d: list, n: int):
    new = d.copy()
    old = d.copy()
    i = 0
    while old:
        new[i % len(new)] = old.pop(0)
        i += n
    return new


# now the main part:
deck = list(range(10007))
for step in puzzle:
    if "cut" in step:
        n = int(step.split(" ")[-1])
        deck = cut(deck, n)
    elif "deal with increment" in step:
        n = int(step.split(" ")[-1])
        deck = deal_inc(deck, n)
    elif "deal into new stack" in step:
        deck = deal_new(deck)
    else:
        print(f"ERROR IN LINE {step}.")

print(deck.index(2019))
