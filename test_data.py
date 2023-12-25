import random
from typing import List


class TestData:
    @staticmethod
    def random_data(size: int) -> List[int]:
        return random.sample(range(size * 2), size)

    @staticmethod
    def sorted_data(size: int) -> List[int]:
        data = list(range(size))
        num_swaps = int(size * 0.1)  # 10% of the size

        for _ in range(num_swaps):
            idx1, idx2 = random.sample(range(size), 2)
            data[idx1], data[idx2] = data[idx2], data[idx1]

        return data

    @staticmethod
    def reverse_sorted_data(size: int) -> List[int]:
        return list(reversed(TestData.sorted_data(size)))

    @staticmethod
    def many_duplicates_data(size: int) -> List[int]:
        return [random.choice(range(max(1, size // 20))) for _ in range(size)]
