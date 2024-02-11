class MyClass:
    a: int
    b: int

    def __init__(self):
        MyClass.a = 100
        MyClass.b = 200
        self.a = 0
        self.b = 0

    def sum(self):
        return self.a + self.b

    def set(self, a, b):
        self.a = a
        self.b = b

    def sum_class_val(self):
        return MyClass.a + MyClass.b


def main():
    c1 = MyClass()
    c2 = MyClass()
    c1.set(1,2)
    print(f"c1 = {c1.sum()}")
    c2.set(10,20)
    print(f"c2 = {c2.sum()}")
    print(f"c1 = {c1.sum()}")
    print(f"c1_sum_class_val = {c1.sum_class_val()}")
    print(f"c2_sum_class_val = {c2.sum_class_val()}")



if __name__ == '__main__':
    main()