# 변수, 자료형

# 기본 자료형
int_var = 1
print(int_var)
print(type(int_var)) # 자료형 확인

float_var = 1.234
print(float_var)
print(type(float_var))

bool_var = True
print(bool_var)
print(type(bool_var))

print(int_var + int_var)
print(int_var + float_var)
print(int_var + bool_var)
print(float_var + bool_var)

print(bool_var)
print(int(bool_var))
print(int(False))

# 컬렉션(여러개 데이터)
list_var = [1, "이", 3.0, [4, 5, 6]]
print(list_var)
print(type(list_var))

print(list_var[0])
print(list_var[-1][0])
print(list_var[-1][1:])

# tuple_var = (1, 2, 3, 4, 5)
tuple_var = 1, 2, 3, 4, 5 # 소괄호 생략 가능
print(tuple_var)
print(tuple_var[0])
print(tuple_var[-1])
print(tuple_var[1:4])
print(type(tuple_var))

dict_var = {
    "name": "김일남", 
    "age": 99
}

print(dict_var)
print(type(dict_var))
print(dict_var["name"])
print(dict_var["age"])
# print(dict_var["address"])
print(dict_var.get("address", "부산"))

# set_var = {} # 딕셔너리
set_var = set()
set_var = {1, 2, 3}
set_var = set("apple") # 순서(인덱스) 없음, 중복 허용 안함
set_var = {1, 1, 1, 1, 1, 2, 2, 2, 3}
print(set_var)
print(type(set_var))

list_var = [] # mutable
list_var.append(1)
print(list_var)

tuple_var = () # immutable
# tuple_var.append(1) # 불가
print(tuple_var)

list_var = [1, 2, 3, 4, 5]
a, b, c, d, e = list_var # unpacking
print(a, b, c, d, e)

a, b, *c = list_var
print(a)
print(b)
print(c)

a, b, c = 1, 2, 3 # tuple unpacking
print(a, b, c)
