# 비정상적인 종료 발생 -> 예외 처리
while True:
    try:
        num1 = int(input("피제수? "))
        num2 = int(input("제수? "))

        print(f"결과는 [{num1/num2}]입니다.")
    except ValueError as e:
        print(f"숫자만 입력 가능합니다. ({e})")
    except ArithmeticError as e:
        print(f"0으로는 나눌 수 없습니다. ({e})")