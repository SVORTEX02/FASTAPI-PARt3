def find(numbers):
    if len(numbers) < 2:
        return None

    largest = numbers[0]
    for num in numbers:
        if num > largest:
            largest = num

    second_largest = None
    for num in numbers:
        if num != largest:
            if second_largest is None or num > second_largest:
                second_largest = num

    return second_largest


print(find([1, 2, 3, 4, 5]))      
