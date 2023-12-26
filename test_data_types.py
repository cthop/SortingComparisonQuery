import random
from typing import List


class TestDataTypes:
    @staticmethod
    def random_data(size: int) -> List[int]:
        return random.sample(range(size * 3), size)

    @staticmethod
    def sorted_data(size: int) -> List[int]:
        data = list(range(0, size * 2, 2))
        num_swaps = int(size * 0.1)  # 10% of the size

        for _ in range(num_swaps):
            idx1, idx2 = random.sample(range(size), 2)
            data[idx1], data[idx2] = data[idx2], data[idx1]

        return data

    @staticmethod
    def reverse_sorted_data(size: int) -> List[int]:
        return list(reversed(TestDataTypes.sorted_data(size)))

    @staticmethod
    def duplicates_data(size: int) -> List[int]:
        return [random.choice(range(max(1, int(1 / 0.2)))) for _ in range(size)]

    @staticmethod
    def skewed_data(size: int) -> List[int]:
        res = [random.choice(range(size // 3, size + 1)) for _ in range(int(size * 0.2) + 1)] + [
            random.choice(range(0, size // 3 + 1)) for _ in range(int(size * (1 - 0.2)) + 1)]
        random.shuffle(res)
        return res


# import matplotlib.pyplot as plt
#
# size = 500
#
# # Generate test data
# random_data = TestDataTypes.random_data(size)
# sorted_data = TestDataTypes.sorted_data(size)
# reverse_sorted_data = TestDataTypes.reverse_sorted_data(size)
# duplicates_data = TestDataTypes.duplicates_data(size)
# skewed_data = TestDataTypes.skewed_data(size)
#
# # Plot each data type
# fig, axs = plt.subplots(5, 1, figsize=(10, 8))
# # Random Data
# axs[0].bar(range(len(random_data)), random_data, color='skyblue')
# axs[0].set_title('Random Data')
#
# # Sorted Data with Swaps
# axs[1].bar(range(len(sorted_data)), sorted_data, color='lightgreen')
# axs[1].set_title('Sorted Data with Swaps')
#
# # Reverse Sorted Data
# axs[2].bar(range(len(reverse_sorted_data)), reverse_sorted_data, color='salmon')
# axs[2].set_title('Reverse Sorted Data')
#
# # Duplicates Data
# axs[3].bar(range(len(duplicates_data)), duplicates_data, color='violet')
# axs[3].set_title('Duplicates Data')
#
# # Skewed Data
# axs[4].bar(range(len(skewed_data)), skewed_data, color='gold')
# axs[4].set_title('Skewed Data')
#
# # Adjust layout and show the plots
# plt.tight_layout()
# plt.show()
