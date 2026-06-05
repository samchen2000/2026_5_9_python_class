import csv

rows = [
    ["name", "Chinese score", "English score", "math score"],
    ["samchen", "85", "88", "77"],
    ["joytu", "95", "97", "88"],
    ["kenlin", "75", "82", "99"]
]

addrows = [["peterlu", "65", "70", "100"]]

try:
    with open("score.csv", mode="w", newline="", encoding="utf-8") as student:
        writer = csv.writer(student)
        writer.writerows(rows + addrows)

except Exception as e:
    print(e)    
    

#使用 DictReader / DictWriter
#DictReader 會自動把第一列當成「欄位名稱」，每一列變成一個字典。
try:
    with open("score.csv", mode="r", newline="", encoding="utf-8") as student_1:
        reader = csv.DictReader(student_1)
        for row in reader:
            print(row["name"], "國語的分數是", row["Chinese score"], "英文的分數是", row["English score"], "數學的分數是", row["math score"])
except Exception as e:
    print(e)
    

with open("score.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)  # 先把標題那一列讀掉
    for row in reader:
        name = row[0]
        chinese_score = int(row[1])
        english_score = int(row[2])
        math_score = int(row[3])
        avg = float((chinese_score + english_score + math_score) / 3 )
        print(name, " 國語分數是 :", chinese_score, " 英文分數是 :", english_score , "平均分數 : ", (round(avg, 2)))

class score:
    # 建構子:初始化物件屬性
    shcool_class = "三年五班"  # 類別變數（全共享：這個班級）
    def __init__(self,name, bread):
        self.name = name
        self.bread = bread
    
    #定義物件的方法 (函式)
    def bark(self):
        print(f"{self.name} says Woof!, my score : {self.bread}, {score.shcool_class}")
my_score_1 = score("sam", "55")
my_score_2 = score("ian", "75")
my_score_1.bark()