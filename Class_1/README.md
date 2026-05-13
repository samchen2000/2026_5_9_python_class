## 2026/5/9 課程
- Python程式設計基礎 1.Python基本語法 2.Python條件分析和迴圈		
- Python內建資料結構 1.Python內建資料結構 2.Python函式和匿名函式		
### 2020/5/9 上課影片
#### 2026_5_9_早上
https://www.youtube.com/watch?v=fhcxceKl8Vw
#### 2026_5_9_下午
https://www.youtube.com/watch?v=mTJSFgaFc40
### 上課內容 :  
1. 使用 colab 進行 python 學習
2. 申請 GitHub 帳號(目前已申請)
3. 使用 colab 設定附檔名為``` ipynb```
4. 學習使用 markdown語法 進行文字說明.
5. 目前學習 ```print()```, 
``` python
str()
int()
float()
bool()
import math
```
### 上課筆記 :  
### 1. python list
針對 例如 x[1,2,3,4,5,6,7,8,9,10]
 #### 添加元素 
 - (Add)append(x): 在列表末尾添加一个元素 x。
 - extend(iterable): 将一个可迭代对象（如列表、元组）中的所有元素添加到列表末尾。
 - insert(i, x): 在指定索引 i 处插入元素 x。
 #### 删除元素 (Remove)
  - pop([i]): 移除并返回列表中索引为 i 的元素（默认是最后一个）。
  - remove(x): 移除列表中第一个值为 x 的元素。如果元素不存在，会抛出 ValueError。
  - clear(): 清空列表中的所有元素。
  - del list[i]: 使用关键字删除指定位置的元素。
#### 查询与搜索 (Search)
  - index(x[, start[, end]]): 返回第一个值为 x 的元素的索引。
  - count(x): 返回元素 x 在列表中出现的次数。
  - in: 判断元素是否在列表中（例如：if x in my_list:）。
#### 排序与翻转 (Order)
 - sort(key=None, reverse=False): 对列表进行原地排序（改变原列表）。
- reverse(): 将列表中的元素原地翻转。
- sorted(list): 内置函数，返回一个排序后的新列表，不改变原列表。
#### 其他常用操作
 - copy(): 返回列表的浅拷贝。
 - len(list): 返回列表长度（元素个数）。
 - list[i] = x: 通过索引修改特定位置的元素值。
 - 列表推导式 (List Comprehension): 使用 [x for x in iterable] 这种简洁的方式创建新列表。
### 回家學習心得 :  
