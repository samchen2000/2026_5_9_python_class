## Python 說明

### python 標準指令庫
- https://docs.python.org/zh-tw/3/library/index.html

### 內建函式
#### Python 直譯器有內建多個可隨時使用的函式和型別。以下按照英文字母排序列出。
### A :  
```python
abs() , aiter() , all() , anext() , any() , ascii()
```
- abs(x)：**回傳數字 x 的絕對值。支援整數、浮點與複數。**
- aiter(async_iterable)：**返回異步可迭代物件的異步迭代器，等同於 async_iterable.__aiter__()。**
- all(iterable)：**當 iterable 中所有元素都為真值時回傳 True，否則回傳 False。空序列回傳 True。**
- anext(async_iterator[, default])：**從異步迭代器取得下一個元素；若已結束且提供 default，則回傳 default，否則丟出StopAsyncIteration。**
- any(iterable)：**只要 iterable 中有任一元素為真值即回傳 True，否則回傳 False。空序列回傳 False。**
- ascii(object)：**回傳物件的 ASCII 字串表示，會把非 ASCII 字元轉換為 \x、\u 或 \U 逃脫序列。**
### B :  
```python
bin() , bool() , breakpoint() , bytearray() , bytes()
```
- bin(x)：將整數 x 轉換為二進位表示的字串，前綴 0b。
- bool([x])：將值轉為布林值。預設 False，若提供 x，會依照物件的真值判斷。
- breakpoint(*args, **kws)：啟動除錯器。預設呼叫 sys.breakpointhook()，常用於插入中斷點。
- bytearray([source[, encoding[, errors]]])：建立可變位元組陣列。來源可為整數、可迭代物件、字串或資料視圖。
- bytes([source[, encoding[, errors]]])：建立不可變位元組物件。用法類似 bytearray()，但結果不可變。
### C :
```  python
callable() , chr() , classmethod() , compile() , complex()
```
- callable(object)：檢查物件是否可呼叫，如函式、方法、實作 __call__ 的物件。
- chr(i)：回傳對應 Unicode 代碼點 i 的字元。
- classmethod(function)：將函式包裝成類別方法。呼叫時第一個參數為類別本身，而非實例。
- compile(source, filename, mode, flags=0, dont_inherit=False, optimize=-1)：將程式碼字串編譯成可執行的程式碼物件，mode 可為 exec、eval、single。
- complex([real[, imag]])：建立複數。若只給一個參數則視為實部；兩個參數表示實部與虛部。
### D :
```   python
delattr() , dict() , dir() , divmod()
```
- delattr(object, name)：刪除物件屬性 name，等同 del object.name。
- dict([mapping_or_iterable], **kwargs)：建立字典。參數可為映射、鍵值對序列或關鍵字引數。
- dir([object])：回傳物件的屬性名稱列表；若無參數，回傳當前本機作用域名稱列表。
- divmod(a, b)：同時回傳 a // b 和 a % b，結果為二元組 (quotient, remainder)。
### E :
```  python
enumerate() , eval() , exec()
```
- enumerate(iterable, start=0)：對可迭代物件加上索引，回傳 (index, value) 的可迭代物件，預設索引從 0 開始。
- eval(expression, globals=None, locals=None)：評估字串形式的 Python 表達式並回傳結果。注意安全性，不應對不受信任的輸入使用。
- exec(object, globals=None, locals=None)：執行字串或程式碼物件中的 Python 程式碼，通常用於動態執行。
### F :  
```  python
filter() , float() , format() , frozenset()
```
- filter(function, iterable)：過濾 iterable，只保留 function(item) 為真的元素；若 function 為 None，則過濾掉假值元素。
- float([x])：將值轉為浮點數。接受字串或數值。
- format(value, format_spec='')：依指定的格式字串回傳值的格式化表示，等同於 value.__format__(format_spec)。
- frozenset([iterable])：建立不可變集合。可用於作為字典鍵或集合的元素。
### G :  
```python
getattr() , globals()
```
- getattr(object, name[, default])：取得物件屬性 name 的值；若屬性不存在且提供 default，回傳 default，否則丟出 AttributeError。
- globals()：回傳當前全域符號表的字典，通常用於動態檢視或修改全域變數。
### H :  
```python
hasattr() , hash() , help() , hex()
```
- hasattr(object, name)：檢查物件是否具有屬性 name。
- hash(object)：回傳物件的雜湊值。可用於可雜湊物件（如不可變型別）作為集合或字典鍵。
- help([object])：顯示物件的說明文件。互動模式下常用於查詢函式、類別與模組說明。
- hex(x)：將整數 x 轉換為十六進位表示的字串，前綴 0x。
### I :  
```python
id() , input() , int() , isinstance() , issubclass() , iter()
```
- id(object)：回傳物件的唯一識別號（記憶體地址的實作層表示），用於比較物件是否為同一實例。
- input([prompt])：從標準輸入讀取一行字串，並回傳。不會自動移除前後空白。
- int([x[, base]])：將值轉為整數。若提供字串，base 可指定進位（預設 10）。
- isinstance(object, classinfo)：檢查物件是否為指定類型或類型元組中的成員。
- issubclass(cls, classinfo)：檢查類別是否為指定類型或類型元組中某個類別的子類。
- iter(object[, sentinel])：若 object 是可迭代物件，回傳迭代器；若提供 sentinel，則 object 必須是可呼叫的，直到回傳 sentinel 為止。
### L :  
```python
len() , list() , locals()
```
- len(s)：回傳序列或容器 s 的長度或元素數量。
- list([iterable])：建立可變列表。若有 iterable，則將其元素轉為列表。
- locals()：回傳當前區域變數的字典視圖，可用於檢查當前區域的變數名稱和值。
### M :  
```python
map() , max() , memoryview() , min()
```
- map(function, iterable, ...)：對每個可迭代物件中的元素呼叫 function，回傳結果的迭代器。可同時處理多個可迭代物件。
- max(iterable, *[, default, key]) / max(arg1, arg2, *args, *[, key])：回傳最大值，支援 key 函式比較；若序列為空且提供 default，回傳 default。
- memoryview(obj)：建立資料物件的記憶體視圖，可直接存取位元組資料而不複製，常用於 bytes、bytearray 等。
- min(...)：回傳最小值，語法與 max() 類似。
### N :  
```python
next()
```
- next(iterator[, default])：從迭代器取得下一個元素。若已耗盡且提供 default，回傳 default，否則丟出 StopIteration。
### O :  
```python
object() , oct() , open() , ord()

```
- object()：建立最基本的空物件。通常用於作為佔位或基底類別。
- oct(x)：將整數 x 轉換為八進位表示的字串，前綴 0o。
- open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None)：開啟檔案，回傳檔案物件。常見模式有 r、w、a、b、t 等。
- ord(c)：回傳字符 c 的 Unicode 代碼點整數值。
### P :  
```python
pow() , print() , property()
```
- pow(x, y[, z])：回傳 x**y，若提供 z 則回傳 x**y % z。
- print(*objects, sep=' ', end='\n', file=sys.stdout, flush=False)：將物件轉為字串並寫入輸出流。可自訂分隔符、結尾字元與是否立即刷新。
- property(fget=None, fset=None, fdel=None, doc=None)：定義屬性描述符，用於類別中建立可控取值、設定與刪除行為。
### R :  
```python
range() , repr() , reversed() , round()
```
- range(stop) / range(start, stop[, step])：建立一個不可變數列序列物件，用於迭代整數。
- repr(object)：回傳物件的正式字串表示，通常用於除錯，應盡量是可重新建立物件的形式。
- reversed(seq)：回傳序列的反向迭代器。支援具有 __reversed__ 或 __len__ / __getitem__ 的物件。
- round(number[, ndigits])：把數字四捨五入到指定小數位。若 ndigits 省略，回傳整數類型。
### S :  
```python
set() , setattr() , slice() , sorted() , staticmethod() , str() , sum() , super()
```
- set([iterable])：建立可變集合，去除重複元素並支援集合運算。
- setattr(object, name, value)：設定物件屬性 name 的值，等同 object.name = value。
- slice(stop) / slice(start, stop[, step])：建立切片物件，可用於序列索引。
- sorted(iterable, *, key=None, reverse=False)：回傳排序後的列表，不改變原始可迭代物件。
- staticmethod(function)：把函式包裝成靜態方法，呼叫時不會自動傳入類別或實例。
- str(object='')：將物件轉為字串表示。
- sum(iterable, start=0)：計算可迭代物件中元素的總和，可指定起始值。
- super([type[, object-or-type]])：取得上一層方法解析順序中的父類別，常用於呼叫父類別方法。
### T :  
```python
tuple() , type()
```
- tuple([iterable])：建立不可變的元組。若給定可迭代物件，將其元素轉為元組。
- type(object)：回傳物件的類別；如果給定三個引數，type(name, bases, dict) 可動態建立新類別。
### V :  
```python
vars()
```
- vars([object])：回傳物件的 __dict__ 屬性字典；若無參數，回傳當前作用域的本機變數字典。
### Z :  
```python
zip()
```
- zip(*iterables)：將多個可迭代物件「壓縮」成元組序列，傳回一個可迭代物件。迭代長度以最短的輸入為準。
### _ :  
```python
__import__()
```
- __import__(name, globals=None, locals=None, fromlist=(), level=0)：內部匯入函式，用於動態匯入模組。通常直接使用 import 語句即可。
