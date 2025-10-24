# ask for user input
x = int(input("Enter number: "))
# check if the number is even or odd
if x % 2 == 0:
    print("A")
if x % 2 == 0 and x % 3 != 0:
    print("B")
elif x % 2 == 0 and x // 3:
    print("C")
elif x % 2 != 0:
    print("D")