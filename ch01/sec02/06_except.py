try:
    result = 10 / 0
except Exception as e:
    print(e)
    result = 0
finally:
    print("결과는 ", result)