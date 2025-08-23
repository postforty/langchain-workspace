# 제너레이터
import sys

def generate_even_nums_generator(n):
    for i in range(n):
        if i % 2 == 0:
            yield i

NUM = 10_000_000

gen_of_evens = generate_even_nums_generator(NUM)
print(f"제너레이터 객체의 메모리 사용량: {sys.getsizeof(gen_of_evens)}")
# print(next(gen_of_evens))

count = 0
for num in gen_of_evens:
    count += 1
    if count % 1000000 == 0:
        print(f"현재까지 {count}개의 짝수 처리")
print(f"제너레이터로 처리된 총 짝수 개수: {count}")
print(f"제너레이터 객체의 최종 메모리 사용량: {sys.getsizeof(gen_of_evens)}")

