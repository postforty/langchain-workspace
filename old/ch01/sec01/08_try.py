try:
    num1 = int(input("피제수: "))
    num2 = int(input("제수: "))

    result = num1 / num2

    print("결과:", result)
except ZeroDivisionError as e:
    print(e)
    print("0으로는 나눌 수 없습니다.")
finally:
    print("프로그램 종료")