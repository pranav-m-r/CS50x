# Assigns a readability grade to the text provided

from cs50 import get_string


def main():
    # Prompt the user for some text
    text = get_string("Text: ")
    words = count_words(text)

    # Compute the Coleman-Liau index
    L = count_letters(text) * 100 / words
    S = count_sentences(text) * 100 / words
    index = round(0.0588 * L - 0.296 * S - 15.8)

    # Print the grade level
    if (index < 1):
        print("Before Grade 1")

    elif (index > 16):
        print("Grade 16+")

    else:
        print(f"Grade {index}")


# Return the number of letters in text
def count_letters(text):
    letters = 0

    for i in text:
        if i.isalpha():
            letters += 1

    return letters


# Return the number of words in text
def count_words(text):
    return len(text.split())


# Return the number of sentences in text
def count_sentences(text):
    sentences = 0

    for i in text:
        if i in [".", "!", "?"]:
            sentences += 1

    return sentences


if __name__ == "__main__":
    main()
