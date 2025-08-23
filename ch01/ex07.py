num = [1, 2, 3, 4, 5]
new_num = []

for n in num:
    new_num.append(n * 10)

print(new_num)

# List Comprehensions
lst_comp = [n * 10 for n in num]
print(lst_comp)

lst_comp = [n * 10 for n in num if n % 2 == 0]
print(lst_comp)