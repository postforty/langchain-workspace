# 제너레이터
# 이터레이터(iterator)를 만드는 함수

def test_generator():
    yield 1
    yield 2
    yield 3

gen = test_generator()

print(next(gen))
print(next(gen))
print(next(gen))
# print(next(gen))