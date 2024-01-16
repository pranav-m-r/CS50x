# Finds the minimum coins needed to make the given amount of change

from cs50 import get_float
from math import floor

# Prompt the user for change owed, in dollars
while True:
    cents = get_float("Change: ") * 100
    # Try until the user provides a valid input
    if cents > 0:
        break

# Calculate how many quarters you should give customer
quarters = floor(cents / 25)
cents -= quarters * 25

# Calculate how many dimes you should give customer
dimes = floor(cents / 10)
cents -= dimes * 10

# Calculate how many nickels you should give customer
nickels = floor(cents / 5)
cents -= nickels * 5

# Calculate how many pennies you should give customer
pennies = cents
cents -= pennies

# Output the minimum number of coins needed
print(int(quarters + dimes + nickels + pennies))
