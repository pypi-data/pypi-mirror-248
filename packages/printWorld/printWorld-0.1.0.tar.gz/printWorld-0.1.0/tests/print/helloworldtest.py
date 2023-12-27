import random


def multiply(first_number, second_number):
    return first_number * second_number


def test_multiply():
    first_number = random.randint(1, 9)
    second_number = random.randint(1, 9)
    total_sum = first_number
    for x in range(1, second_number):
        total_sum = total_sum + first_number
    assert multiply(first_number, second_number) == total_sum
