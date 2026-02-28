def my_decorator(func):
    def wrapper():
        print("함수 실행 전!")
        func()
        print("함수 실행 후!")
    return wrapper

@my_decorator
def say_hello():
    print("안녕하세요!")

say_hello()