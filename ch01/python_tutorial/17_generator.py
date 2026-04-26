import sys

NUMBER = 10_000_000

def get_even_numbers_list(n):
    even_nums = []
    for i in range(n):
        if i % 2 == 0:
            even_nums.append(i)
    
    return even_nums

list_of_evens = get_even_numbers_list(NUMBER)
print(f"{len(list_of_evens)} 개")
print(f"{sys.getsizeof(list_of_evens)} 바이트")

def get_evem_numbers_generator(n):
    for i in range(n):
        if i % 2 == 0:
            yield i

generator_of_evens = get_evem_numbers_generator(NUMBER)
print(f"{sys.getsizeof(generator_of_evens)} 바이트")

count = 0
for num in generator_of_evens:
    count += 1
    if count % 1000000 == 0:
        print(f"현재까지 {count}개의 짝수 처리 중...")
print(f"제너레이터로 처리된 총 짝수 개수: {count}")

print(f"{sys.getsizeof(generator_of_evens)} 바이트")
