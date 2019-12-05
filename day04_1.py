puzzle_input_range = range(264793, 803935 + 1)
passwords = 0

for number in puzzle_input_range:
    number_string = str(number)
    # check for repeating characters
    result = False

    for c in number_string:
        if c * 2 in number_string:
            result = True
    if not result:
        continue

    # check for decreasing numbers
    result = False
    for i in range(5):
        if int(number_string[i + 1]) < int(number_string[i]):
            result = True
    if result:
        continue

    # if we're here, then the number is a potential password
    passwords += 1

print(passwords)
