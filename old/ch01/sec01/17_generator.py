def test_gen():
    yield 1
    yield 2
    yield 3

gen = test_gen()

print(next(gen))
print(next(gen))
print(next(gen))
# print(next(gen))