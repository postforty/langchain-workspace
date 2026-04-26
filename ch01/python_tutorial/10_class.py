class Person:
    def __init__(self, name, age):
        self.name = name # 인스턴스 변수
        self.age = age

person = Person("김일남", 99)
print(person.name)
print(person.age)

class Student(Person):
    def __init__(self, name, age, student_number):
        super().__init__(name, age)
        self.student_number = student_number

    # 인스턴스 메서드
    def study(self):
        print(f"{self.name} 학생이 열공합니다!")

student = Student("김일남", 99, 1)
print(student.name)
print(student.age)
print(student.student_number)
student.study()