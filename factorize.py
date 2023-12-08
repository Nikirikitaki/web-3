from multiprocessing import Pool
import os
import multiprocessing
import logging
import time

# logging.basicConfig(level=logging.INFO)

def factorize(*numbers):
    all_factors = []
    for number in numbers:
        factors = []
        logging.info(f"Factorizing {number} , {os.getpid}")
        for i in range(1, number + 1):
            if number % i == 0:
                factors.append(i)
        # Логируем завершение факторизации числа
        logging.info(f"Factors of {number}: {factors} {os.getpid}")
        all_factors.append(factors)
    return all_factors


a, b, c, d  = factorize(128, 255, 99999, 10651060)

assert a == [1, 2, 4, 8, 16, 32, 64, 128]
assert b == [1, 3, 5, 15, 17, 51, 85, 255]
assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]

if __name__ == "__main__":

    # Вимірюємо час виконання синхронної версії
    start_time = time.time()
    result_sync = factorize(*a, *b, *c, *d)
    end_time = time.time()
    print("Synchronous execution time:", end_time - start_time)
    # print("Result (synchronous):", result_sync)
    
    # Создаем два процесса для обработки директории
    process1 = multiprocessing.Process(target=factorize, args=(*a, *b, *c, *d))
    process2 = multiprocessing.Process(target=factorize, args=(*a, *b, *c, *d))

    # Запускаем процессы + Ожидаем завершения обоих процессов
    num_cpus = multiprocessing.cpu_count()
    start_time = time.time()
    process1.start()
    process1.join()
    end_time = time.time()
    print("Proc-1 execution time:", end_time - start_time,"CPU -",num_cpus)
    
    start_time = time.time()
    process2.start()
    process2.join()
    end_time = time.time()
    print("Proc-2 execution time:", end_time - start_time,"CPU -",num_cpus)
    
   
