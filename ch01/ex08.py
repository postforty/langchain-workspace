# 클래스와 객체(OOP)

class Dog:
    def __init__(self, name): # 매직 메서드
        self.name = name # 인스턴스 변수 정의

    def bark(self): # 인스턴스 메서드
        print("멍멍")

my_dog = Dog("흰둥이")

print(my_dog)  # <__main__.Dog object at 0x000001BC79C66900>
print(my_dog.name)
my_dog.bark()

your_dog = Dog("검둥이")
print(your_dog.name)
your_dog.bark()