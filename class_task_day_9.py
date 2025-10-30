odd_numbers = list(range(1, 101))
new_list = []

for num in odd_numbers:
    if not (num % 2 != 0 and num % 3 == 0):
        new_list.append(num)

print("Updated list:", new_list)
print("Count of numbers left:", len(new_list))