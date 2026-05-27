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
    
    # 驅車二輪轉,路長紅燈多.
    # 東行西進,南衝北轉.
    # 一時雲捲天色濃,清風挽長風.
    # 我欲加緊催油門,雷鳴掩蓋引擎聲.
    # 聲聲響,心心驚.
    # 風嘯肆意穿街,
    # 悶雷深擊雲門,
    # 萬千雨箭蓄發,
    # 雨急落,風狂笑,
    # 急雨狂風天難留,
    # 暫停避雨著雨衣.
    # 迎面風協雨襲身,
    # 雨穿沁衣繪河山,