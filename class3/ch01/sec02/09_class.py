class Dog:
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed

    def bark(self):
        return f"{self.name} ({self.breed})가 멍멍 짖습니다."
    
my_dog = Dog("흰둥이", "진돗개")
print(my_dog.bark())