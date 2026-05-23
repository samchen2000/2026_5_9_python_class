import random

answer = random.randint(1,100)

count = 0

print("===猜數字遊戲===")
print("請猜一個數字1到100的數字")

while True:
    guess = int(input("請輸入數字"))

    count += 1
    if guess > answer:
        print("太大了")
    elif guess < answer:
        print("太小了")
    else:
        print("猜對了")
        break