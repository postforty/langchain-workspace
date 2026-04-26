# 반복의 횟수를 알 수 없을 때

if False:
    count = 1
    while True: # 무한 루프
        print(f"나무를 {count}번 찍었습니다.")
        count += 1

count = 0
while count < 5:
    count += 1
    print(f"나무를 {count}번 찍었습니다.")

count = 0
while True:
    if count >= 5:
        break # 반복 중단, break 아래 있는 코드 실행 안함
    count += 1
    print(f"나무를 {count}번 찍었습니다.")