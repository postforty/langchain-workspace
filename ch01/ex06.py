# 예외 처리
# try, except, else, finally

try:
    result = 10 / 0 # ZeroDivisionError 
except ZeroDivisionError:
    print("입력하신 내용을 계산할 수 없습니다.")
else:
    print(result)
finally:
    print("프로그램 종료!")