#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
from queue import Queue
from threading import Thread

from src.task_1 import calculate_series, calculate_term


# Тест для функции calculate_term
def test_calculate_term():
    x = 2
    # Проверяем первые несколько членов ряда
    assert math.isclose(calculate_term(x, 0), x, rel_tol=1e-9)
    assert math.isclose(
        calculate_term(x, 1), x**3 / math.factorial(3), rel_tol=1e-9
    )
    assert math.isclose(
        calculate_term(x, 2), x**5 / math.factorial(5), rel_tol=1e-9
    )


# Тест для функции calculate_series
def test_calculate_series():
    x = 2
    epsilon = 1e-7
    queue = Queue()

    # Запускаем поток для расчета суммы ряда
    thread = Thread(target=calculate_series, args=(x, epsilon, queue))
    thread.start()
    thread.join()

    # Извлекаем результат из очереди
    s = queue.get()

    # Контрольное значение функции y
    y = (math.exp(x) - math.exp(-x)) / 2

    # Проверяем, что рассчитанная сумма близка к аналитическому значению
    assert math.isclose(s, y, rel_tol=1e-7), f"Ожидал {y}, но получил {s}"


# Тест для граничных случаев
def test_calculate_series_boundary():
    epsilon = 1e-7
    queue = Queue()

    # Проверяем для x = 0 (результат должен быть 0, так как все члены ряда равны 0)
    x = 0
    thread = Thread(target=calculate_series, args=(x, epsilon, queue))
    thread.start()
    thread.join()
    result = queue.get()
    assert result == 0.0, f"Ожидал 0.0, но получил {result}"

    # Проверяем для очень маленького x (пример x = 1e-3, сумма близка к x)
    x = 1e-3
    thread = Thread(target=calculate_series, args=(x, epsilon, queue))
    thread.start()
    thread.join()
    result = queue.get()
    assert math.isclose(
        result, x, rel_tol=1e-7
    ), f"Ожидал приблизительно {x}, но получил {result}"
