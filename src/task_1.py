#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# С использованием многопоточности для заданного значения найти сумму ряда с
# точностью члена ряда S по абсолютному значению ε=10-7 и произвести сравнение
# полученной суммы с контрольным значением функции для двух бесконечных рядов.


import math
import threading
from queue import Queue


# Функция для вычисления одного члена ряда
def calculate_term(x: float, n: int) -> float:
    return (x ** (2 * n + 1)) / math.factorial(2 * n + 1)


# Функция для вычисления суммы ряда с заданной точностью
def calculate_series(x: float, epsilon: float, queue: Queue[float]) -> None:
    n: int = 0
    term = calculate_term(x, n)
    total_sum: float = 0
    while abs(term) > epsilon:
        total_sum += term
        n += 1
        term = calculate_term(x, n)
    queue.put(total_sum)
    queue.task_done()


def main() -> None:
    queue: Queue[float] = Queue()

    # Значения x, epsilon, и расчет y
    x: float = 2.0
    epsilon: float = 1e-7
    y: float = (math.exp(x) - math.exp(-x)) / 2  # Контрольное значение

    # Создаем и запускаем поток
    thread = threading.Thread(target=calculate_series, args=(x, epsilon, queue))
    thread.start()

    # Ожидаем завершения потоков
    thread.join()
    queue.join()

    # Получаем результат
    s: float = queue.get()

    # Вывод результатов
    print(f"Рассчитанная сумма ряда S: {s}")
    print(f"Контрольное значение функции y: {y}")
    print(f"Разница между S и y: {abs(s - y)}")


if __name__ == "__main__":
    main()
