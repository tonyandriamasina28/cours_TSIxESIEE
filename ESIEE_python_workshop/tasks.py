#Task 1: Create a function to cook your favorite dish. It should contain parameters, methods and conditions.
def cook_pasta(servings, ingredients, sauce="tomato"):
    """Return the cooking steps, or a list of what is missing."""
    required = {"pasta", "salt", sauce}
    available = {ingredient.lower() for ingredient in ingredients}
    missing = required - available

    if servings <= 0:
        return ["Nothing to cook."]
    if missing:
        return ["Missing: " + ", ".join(sorted(missing))]

    grams = servings * 100
    return [
        "Boil a large pot of salted water.",
        f"Cook {grams} g of pasta for 10 minutes.",
        f"Mix with the {sauce} sauce and serve.",
    ]


#Task 2: Conditional Statements
#Write a Python program that checks if a given number is positive, negative, or zero. Print an appropriate message for each case.
def describe_number(number):
    if number > 0:
        return f"{number} is positive."
    elif number < 0:
        return f"{number} is negative."
    else:
        return f"{number} is zero."


#Task 3:
#Write a program that prints all even numbers between 1 and 20 using both a for loop and a while loop.
def even_numbers_for():
    numbers = []
    for number in range(2, 21, 2):
        numbers.append(number)
    return numbers


def even_numbers_while():
    numbers = []
    number = 2
    while number <= 20:
        numbers.append(number)
        number += 2
    return numbers


if __name__ == "__main__":
    print("Task 1:")
    for step in cook_pasta(2, ["Pasta", "Salt", "Tomato"]):
        print("-", step)
    print("-", cook_pasta(2, ["Pasta"])[0])

    print("\nTask 2:")
    for value in (5, -3, 0):
        print(describe_number(value))

    print("\nTask 3:")
    print("for:  ", *even_numbers_for())
    print("while:", *even_numbers_while())
