# 컴프리헨션(Comprehensions)
# 리스트 컴프리헨션
nums = [1, 2, 3, 4, 5]
result = [n + 10 for n in nums]
print(result)
result = [n for n in nums if n % 2 == 0]
print(result)

# 딕셔너리 컴프리헨션
dict = {
    "name": "김일남",
    "age": 99,
    "address": "부산"
}

print(dict)
keys = ["name", "age", "address"]
values = ["김일남", 99, "부산"]

# for k, v in zip(keys, values):
#     print(k, ":",  v)

result = {k: v for k, v in zip(keys, values)}
print(result)