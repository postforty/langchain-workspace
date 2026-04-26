# 기능(function)의 재사용
def greet(name):
    print(f"{name}님, 안녕하세요?")

greet("김일남")
greet("김이남")
greet("김삼남")
greet("김사남")
greet("김오남")

print("---")

# 함수의 형태
# 1. 인수 X, 반환값 X
def func():
    print("인수 X, 반환값 X")

func()

# 2. 인수 O, 반환값 X
def func(param):
    print(param)

func("인수 O, 반환값 X")

# 3. 인수 X, 반환값 O
def func():
    return "인수 X, 반환값 O"

print(func())

# 4. 인수 O, 반환값 O
def func(param):
    return param

print(func("인수 O, 반환값 O"))