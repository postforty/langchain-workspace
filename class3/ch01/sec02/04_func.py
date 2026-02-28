# 함수
def greet(name="아무개"):
    return f"안녕하세요, {name}님!"

message = greet("김일남")
print(message)

message = greet("김이남")
print(message)

message = greet()
print(message)

