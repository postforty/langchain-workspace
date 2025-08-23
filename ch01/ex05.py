# 파일 입출력
# - 파일 입력: 파일의 내용 읽어 오기
# - 파일 출력: 파일을 저장하기

# mode
# 텍스트
# - r : 읽기
# - w : 쓰기
# - a : 수정(추가)
# 바이너리
# - rb : 읽기
# - wb : 쓰기
# - ab : 수정(추가)

# 텍스트 파일 생성
file = open("ch01/example_basic.txt", "w", encoding="utf8")
file.write("python")
file.write("\n") # 줄바꿈

# 인코딩 방식
# - UTF-8 : 웹
# - CP949 : 윈도우
file.write("파이썬")
file.close() # file 객체를 메모리에서 제거(메모리 누수 방지)

# 텍스트 파일 읽기
file = open("ch01/example_basic.txt", "r", encoding="utf8")
content = file.read()
file.close()
print(content)

print("---")

with open("ch01/example_basic.txt", "r", encoding="utf8") as file:
    content = file.read()

print(content)
