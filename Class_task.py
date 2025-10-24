# ask for user input
x = int(float(input("Enter a number: ")))
# check if the number is even or odd
if x % 2 == 0 and x % 3 != 0:
    print("B")
elif x % 3 == 0 and x % 3 != 0:
    print("C")
elif x % 2 == 0:
    print("D")
else:
    print("A")