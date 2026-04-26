f = open("example_basic.txt", "w", encoding="utf-8")
f.write("첫줄\n")
f.write("둘째줄\n")
f.write("셋째줄\n")
f.close()

f = open("example_basic.txt", "r", encoding="utf-8")
# content = f.read()

# content = f.readline()
# print(content, end="")
# content = f.readline()
# print(content, end="")
# content = f.readline()
# print(content, end="")

content_list = f.readlines()
print(content_list)

f.close()
