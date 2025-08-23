# 변수, 기본 자료형
int_var = 10 # 정수
int_var = 20 # 코드 복사 단축키 : alt + shift + 방향키 아래로
print(int_var)

float_var = 3.14 # 실수
print(float_var)

bool_var = True # 논리형
bool_var = False
print(bool_var)

str_var = "a" # 문자열: 파이썬에서는 문자 없음(모든 문자는 문자열)
print(str_var)

# 컬렉션 자료형(자료 구조)

# 리스트
list_var = [1, 2, 3]
print(list_var)

# [1, 2, 3]
#  0  1  2
# -3 -2 -1 

# 인덱싱
print(list_var[1]) 
print(list_var[2])
print(list_var[-1])

# 슬라이싱
print(list_var[1:3])
print(list_var[1:])

# ---

# 튜플
tup_var = (1, 2, 3)
tup_var = 1, 2, 3
print(tup_var)

# ---

# 딕셔너리
dic_var = {"a": 1, "b": 2}
print(dic_var["a"])

# ---

# 세트(집합)
# - 중복 허용 안됨
# - 순서 없음
set_var = {"a", "a", "b", "c"}
print(set_var) # {'c', 'a', 'b'}
# print(set_var[0]) # 인덱스가 없기 때문에 오류

# 문자열 포맷(f-string)
print(f"정수: {int_var}, 실수: {float_var}")

float_var = 3.141592

print(f"정수: {int_var}, 실수: {float_var}")