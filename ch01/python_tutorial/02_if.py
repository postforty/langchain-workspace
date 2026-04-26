# 실행 할지 말지
if False:
    print(True)

# 둘 중 하나
if True:
    print(True)
else:
    print(False)

# 여럿 중 하나
score = 99

if score >= 90:
    print("A")
elif score >= 80:
    print("B")
elif score >= 70:
    print("C")
elif score >= 60:
    print("D")
else:
    print("F")

# 조건 삼항 연산자
score = 60
if score >= 60:
    print("합격")
else:
    print("불합격")

result = "합격" if score >= 60 else "불합격" # 조건 삼항 연산자
print(result)

print("합격") if score >= 60 else print("불합격")

print(True and True) # 논리곱
print(False and True) # 단축 평가
print(True and False)

is_rain = True
is_rain = False

# if is_rain:
#     print("우산 챙기기")

is_rain and print("우산 챙기기") # 단축 평가

