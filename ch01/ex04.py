# 함수
# define, definition
# 명명 규칙
# - 동사형
# - 스네이크 케이스
def greet(name="아무개"):
    print(f"{name}님 안녕하세요!")

greet("김일남")
greet()

print(greet()) # None

def add(a, b):
    return a + b

print(add(1, 2) + 2)