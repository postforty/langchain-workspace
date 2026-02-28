# 제어문
# 조건문(분기문)

score = 85

# score가 90 이상이면 "A", 80 이상이면 "B", 70 이상이면 "C"
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
else:
    grade = "C"

print(f"점수는 {score}점이고, 등급은 {grade}입니다.")