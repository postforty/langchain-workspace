# File I/O
with open("example.txt", "w", encoding="utf8") as f:
    f.write("첫 줄\n")
    f.write("둘째 줄\n")
    f.write("셋째 줄\n")

with open("example.txt", "r", encoding="utf8") as f:
    content = f.read()
    print(content)