## 2026/6/6 課程
- 數據整理-Pandas檔案存取		
- 數據整理-資料整理和使用前準備
### 2020/6/6 上課影片
#### 2026_6_6_早上

#### 2026_6_6_下午

### 上課內容 :  

### 上課筆記 :  

### 回家學習心得 :  
### 1. 先行學習 class 的方式.
### 用汽車生產來做比喻:
在 Python 中，class（類別）的概念就像是汽車工廠裡的「汽車設計圖」，而透過設計圖製造出來的每一台「實體汽車」就是實例（Instance）。透過這個汽車工廠的比喻，我們來拆解 class 的核心用法：  
### 🏎️1. 定義類別(設計圖)  
在工廠生產任何車子之前，工程師必須先畫好一張藍圖。這張藍圖規定了車子應該有什麼外觀特徵、什麼功能。  
- ```class Car```：這就是我們的「汽車設計圖」。  
- ```def __init__(self, color, brand)```：這是工廠的「生產線裝配程序」（建構子）。每當有一台新車要下線時，這個程序就會被啟動。  
- ```self```：代表「目前正在生產線上的那台車」。我們要把顏色、品牌等標籤貼在「這台車」上。  

```python
class Car:
    # 汽車生產線的初始化程序（建構子）
    def __init__(self, color, brand):
        self.color = color   # 幫這台車烤漆（實例屬性）
        self.brand = brand   # 幫這台車貼上品牌標籤（實例屬性）
        self.speed = 0       # 每台車剛出廠時，時速預設都是 0
        
    # 汽車的功能按鈕（實例方法）
    def drive(self):
        self.speed += 10
        print(f"這台 {self.color} 的 {self.brand} 踩油門了！目前時速：{self.speed} km/h")
```
### 🏭 2. 建立實例（工廠開始量產）
有了設計圖後，工廠就可以開始量產車子。雖然大家都用同一張設計圖，但生產出來的每一台車都是獨立的實體，可以擁有不同的外觀。
```python
# 依照設計圖，生產第一台「紅色的 Toyota」
my_first_car = Car("紅色", "Toyota")

# 依照同一張設計圖，生產第二台「黑色的 Tesla」
my_second_car = Car("黑色", "Tesla")

# 呼叫第一台車的功能
my_first_car.drive()  # 輸出: 這台 紅色 的 Toyota 踩油門了！目前時速：10 km/h
```

### ***注意：這時候你點擊第一台車的油門，第二台車（my_second_car）並不會前進，因為它們是互相獨立的實體汽車。***

### 例如：所有車都有 4 個輪子。我們不需要在每台車下線時重複設定，而是直接寫在設計圖的最上層。

```python
class Car:
    wheels = 4  # 類別變數（全工廠共享：所有的車都有 4 個輪子）

    def __init__(self, color, brand):
        self.color = color
        self.brand = brand

car1 = Car("白色", "Honda")
print(car1.wheels)  # 輸出: 4
```
### 🛠️ 4. 繼承（衍生車款：電動車設計圖）
幾年後，工廠決定研發新科技，要生產「電動車」。我們不需要重新畫一張包含輪子、油門的全新設計圖，而是直接拿原本的汽車設計圖來進行修改與升級。
```class EV(Car)```：EV（電動車）直接繼承了 Car（傳統汽車）的所有功能。  
***擴充與修改***：我們可以加上電動車專屬的「電池容量」，甚至修改原本的「踩油門（drive）」方式。  
```python
# 電動車設計圖 繼承 傳統汽車設計圖
class EV(Car):
    def __init__(self, color, brand, battery_capacity):
        # 呼叫原本汽車設計圖的裝配程序，處理顏色和品牌
        super().__init__(color, brand)
        # 電動車專屬的裝配項目
        self.battery_capacity = battery_capacity 
        
    # 專屬電動車的功能
    def charge(self):
        print(f"這台 {self.brand} 正在充電中...目前電池容量：{self.battery_capacity} kWh")

# 生產一台電動車
my_ev = EV("藍色", "Tesla", 75)
my_ev.drive()   # 繼承自原本汽車的功能，依然可以使用！
my_ev.charge()  # 電動車專屬的功能
```
透過汽車工廠的比喻，你可以把 ```class`` 理解為「規格與功能的定義」，而物件則是「看得見、摸得著、會動的成品」。  