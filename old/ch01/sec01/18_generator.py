import sys

def gen_even_list(n):
    even_nums = []

    for i in range(n):
        if i % 2 == 0:
            even_nums.append(i)
    
    return even_nums

def gen_even_generator(n):
    for i in range(n):
        if i % 2 == 0:
            yield i

N = 1_000_000
lst = gen_even_list(N)
print(f"리스트 짝수 개수: {len(lst)}")
print(f"리스트 짝수 메모리 사용량: {sys.getsizeof(lst)}")

gener = gen_even_generator(N)
print(f"제너레이터 짝수 메모리 사용량: {sys.getsizeof(gener)}")

count = 0
for n in gener:
    count += 1
    if count % 100_000 == 0:
        print(f"{count}개 짝수 처리 중...")

print(f"제너레이터 짝수 개수: {count}")
print(f"제너레이터 짝수 메모리 사용량: {sys.getsizeof(gener)}")

