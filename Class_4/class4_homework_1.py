import csv
import os


teacher = ['SamChen', 'AllanLu', 'IanKu']
print(teacher)
# append() - 在末尾添加單一元素
teacher.append('JasonWu')
print(teacher)
# extend() - 擴展多個元素
teacher.extend(['TomLi', 'JoyChang'])
print(teacher)
# insert() - 在指定位置插入元素
teacher.insert(3, 'ChrisShih')
print(teacher)
# 獲取腳本所在目錄，然後找 student_data.csv
# 取得目前這支 .py 檔的所在資料夾
script_dir = os.path.dirname(os.path.abspath(__file__))
# 組成 student_data.csv 的完整路徑
#csv_file = os.path.join(script_dir, "student_data.csv")
txt_file = os.path.join(script_dir, "note2.txt")
print(script_dir)
#print(csv_file)
print(txt_file)
try:
    #with open(csv_file, mode="r", encoding="utf-8") as student:
    with open(txt_file, mode="r", encoding="utf-8") as student:
        for list in student:
            print(list.strip())
except Exception as e:
    print(e)