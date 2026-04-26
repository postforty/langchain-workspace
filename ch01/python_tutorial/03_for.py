# 반복의 횟수 정해져 있을 때
for i in [0, 1, 2, 3, 4]:
    print(i)

for c in "python":
    print(c)

for i in range(5):
    print(i)

for t in enumerate(["사과", "바나나", "딸기"]):
    print(f"{t[0] + 1}번 {t[1]}")

for i, v in enumerate(["사과", "바나나", "딸기"]):
    print(f"{i + 1}번 {v}")