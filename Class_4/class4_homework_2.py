import csv

rows = [
    ["name", "Chinese score", "English score"],
    ["samchen", "85", "88"],
    ["joytu", "95", "97"],
    ["kenlin", "75", "82"]
]

addrows = [["peterlu", "65", "70"]]

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
            print(row["name"], "國語的分數是", row["Chinese score"], "英文的分數是", row["English score"])
except Exception as e:
    print(e)
    

with open("score.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)  # 先把標題那一列讀掉
    for row in reader:
        name = row[0]
        chinese_score = int(row[1])
        english_score = int(row[2])
        avg = float((chinese_score + english_score) / 2)
        print(name, " 國語分數是 :", chinese_score, " 英文分數是 :", english_score , "平均分數 : ", avg)
