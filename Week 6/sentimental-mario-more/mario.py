# Recreates the pyramid of blocks from Super Mario Brothers

from cs50 import get_int

# Get the height of the pyramid as an input from the user
while True:
    height = get_int("Height: ")
    if height > 0 and height < 9:
        break

for i in range(1, height + 1):
    print((" " * (height - i)) + ("#" * i) + "  " + ("#" * i))
