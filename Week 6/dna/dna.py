# Checks if a DNA sequence matches that of any person in a CSV database

from csv import DictReader
from sys import argv


def main():

    # Check for command-line usage
    if len(argv) != 3:
        print("Usage: python dna.py database.csv sequence.txt")
        sys.exit()

    # Read database file into a variable
    data = []
    subsequences = []
    with open(argv[1]) as file1:
        data_reader = DictReader(file1)
        subsequences = data_reader.fieldnames[1:]
        for row in data_reader:
            data.append(row)

    # Read DNA sequence file into a variable
    sequence = ""
    with open(argv[2]) as file2:
        sequence = file2.read()

    # Find longest match of each STR in DNA sequence
    longest_matches = dict()
    for i in subsequences:
        longest_matches[i] = str(longest_match(sequence, i))

    # Check database for matching profiles
    name = "No match"
    for person in data:
        longest_matches["name"] = person["name"]
        if longest_matches == person:
            name = person["name"]

    print(name)

    return


# Returns length of longest run of subsequence in sequence
def longest_match(sequence, subsequence):

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
