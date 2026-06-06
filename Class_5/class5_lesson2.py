n = 10
def main():
    print("這裡是main function 的命名空間")
    print(__name__)
    o = 12
    print(o)

def function_1():
    with open("note.txt", "r", encoding="utf-8") as fun_1:
        con = fun_1.read
        print("這是function_1")

def function_2():
    n= 100
    m = 50

if __name__ == "__main__":
    print(n)
    main()
    function_1()


