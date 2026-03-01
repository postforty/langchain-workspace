class Dog:
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed
    
    def bark(self):
        return f"{self.breed} {self.name} 멍멍"

dog = Dog("흰둥이", "진돗개")
print(dog.name)
print(dog.breed)
print(dog.bark())