import random

name = input("Enter your name: ")
question = input("Ask the Magic 8-Ball a question: ")

answer = ""
random_number = random.randint(1, 9)

# Assign an answer based on random number
if random_number == 1:
    answer = "Yes - definitely."
elif random_number == 2:
    answer = "It is decidedly so."
elif random_number == 3:
    answer = "Without a doubt."
elif random_number == 4:
    answer = "Reply hazy, try again."
elif random_number == 5:
    answer = "Ask again later."
elif random_number == 6:
    answer = "Better not tell you now."
elif random_number == 7:
    answer = "My sources say no."
elif random_number == 8:
    answer = "Outlook not so good."
elif random_number == 9:
    answer = "Very doubtful."
else:
    answer = "Error."

# Check if user actually asked a question
if question == "":
    print("You must ask a question to receive a fortune! The fabric of reality depends on it!")
# If name is empty, print only question and answer
elif name == "":
    print("Question:", question)
    print("Magic 8-Ball's answer:", answer)
# If both name and question are provided, print both
else:
    print(f"{name} asks: {question}")
    print("Magic 8-Ball's answer:", answer)
