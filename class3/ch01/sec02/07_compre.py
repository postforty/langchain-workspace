# 리스트/딕셔너리 컴프리헨션(Comprehensions)

nums = [1, 2, 3, 4, 5]
result = [num*10 for num in nums if num % 2 == 0]
print(result)

keys = ["name", "age", "city"]
values = ["김일남", 99, "부산"]

# print(dict(zip(keys, values)))
person_dict = {k: v for k, v in zip(keys, values)}
print(person_dict)