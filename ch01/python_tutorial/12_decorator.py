def my_decorator(func):
    def wrapper():
        print("함수 실행 전!")
        func() # 콜백 함수
        print("함수 실행 후!")

    return wrapper

# 데코레이터 적용
@my_decorator
def say_hello():
    print("안녕하세요!")

say_hello()