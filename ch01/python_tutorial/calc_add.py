# 클로저
def calc_add():
    result = 0

    def inner_func(num):
        nonlocal result
        result += num
        return result
    
    return inner_func

# print(__name__)

if __name__ == "__main__":
    result = calc_add(1, 2)
    print(result)
