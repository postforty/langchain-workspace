with open("example_basic.txt", "w", encoding="utf-8") as f:
    f.write("첫줄\n")
    f.write("둘째줄\n")
    f.write("셋째줄\n")

with open("example_basic.txt", "r", encoding="utf-8") as f:
    content_list = f.readlines()
    print(content_list)
