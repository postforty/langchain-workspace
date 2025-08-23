import sys

def generate_even_nums_list(n):
    even_nums = []

    for i in range(n):
        if i % 2 == 0:
            even_nums.append(i)

    return even_nums

NUM = 10_000_000

list_of_evens = generate_even_nums_list(NUM)
print(f"리스트에 저장된 짝수 개수: {len(list_of_evens)}")
print(f"리스트 객체의 메모리 사용량: {sys.getsizeof(list_of_evens)}")