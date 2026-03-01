# File I/O
f = open("example.txt", "w", encoding="utf8") # write text
f.write("첫 줄\n")
f.write("둘째 줄\n")
f.write("셋째 줄\n")
f.close()

f = open("example.txt", "r", encoding="utf8") # read text
content = f.read()
print(content)
f.close()