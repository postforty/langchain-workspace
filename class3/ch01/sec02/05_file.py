# File I/O

# wt, rt, at(w, r, a)
# wb, rb, ab
# 윈도우: cp949, 웹: utf8
# f = open("example.txt", "w", encoding="utf8")
# f.write("1번줄 작성")
# f.close()

# f = open("example.txt", "a", encoding="utf8")
# f.write("\n2번줄 작성")
# f.close()

# f = open("example.txt", "r", encoding="utf8")
# content = f.read()
# print(content)
# f.close()

with open("example.txt", "r", encoding="utf8") as f:
    content = f.read()
    print(content)