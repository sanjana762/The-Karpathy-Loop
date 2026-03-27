from generated_code import two_sum
import time

def test_basic_case():
    assert two_sum([2, 7, 11, 15], 9) == [0, 1]

def test_another_case():
    assert two_sum([3, 2, 4], 6) == [1, 2]

def test_performance():
    nums = list(range(10000))
    target = 19997

    start = time.time()
    result = two_sum(nums, target)
    end = time.time()

    assert result == [9998, 9999]
    assert (end - start) < 0.5