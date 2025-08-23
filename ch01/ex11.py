# 동기 프로그램
import time

def fetch_data_sync(delay):
    print(f"시작! 딜레이 {delay}초")
    time.sleep(delay)
    print(f"끝! 딜레이 {delay}초")
    return f"동기 딜레이 {delay}초"

def main_sync():
    result1 = fetch_data_sync(2)
    result2 = fetch_data_sync(1)
    print(f"결과: {result1}, {result2}")

main_sync()