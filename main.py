import matplotlib.pyplot as plt
import random
import time
import gc
from typing import Callable, List
from scipy.integrate import simps
from multiprocessing import Pool, cpu_count

from merge_sort import merge_sort
from quick_sort import quick_sort
from shell_sort import shell_sort
from tim_sort import tim_sort
from heap_sort import heap_sort
from my_sort_not_in_place import my_sort_not_in_place
from my_sort_in_place import my_sort_in_place


class TestData:
    @staticmethod
    def random_data(size: int) -> List[int]:
        return random.sample(range(size * 2), size)

    @staticmethod
    def sorted_data(size: int) -> List[int]:
        return list(range(size))

    @staticmethod
    def reverse_sorted_data(size: int) -> List[int]:
        return list(range(size, 0, -1))

    @staticmethod
    def many_duplicates_data(size: int) -> List[int]:
        return [random.choice(range(max(1, size // 10))) for _ in range(size)]


def benchmark_single_algorithm(algo_data):
    algo, data, data_type, repetitions = algo_data
    times = []

    for _ in range(repetitions):
        gc.disable()
        test_data = data.copy()
        start_time = time.perf_counter()
        algo(test_data)
        end_time = time.perf_counter()
        gc.enable()

        times.append(end_time - start_time)

    average_time = sum(times) / repetitions
    return algo.__name__, data_type, average_time


def benchmark_sorting_algorithms(sorting_algorithms: List[Callable],
                                 data_generator: TestData,
                                 sizes: List[int],
                                 repetitions: int = 5) -> dict:
    results = {algo.__name__: {'random': [], 'sorted': [], 'reverse_sorted': [], 'many_duplicates': []}
               for algo in sorting_algorithms}

    pool = Pool(max(1, cpu_count() - 2))

    for size in sizes:
        print(f"Testing size: {size}")

        datasets = {
            'random': data_generator.random_data(size),
            'sorted': data_generator.sorted_data(size),
            'reverse_sorted': data_generator.reverse_sorted_data(size),
            'many_duplicates': data_generator.many_duplicates_data(size)
        }

        tasks = [(algo, datasets[data_type], data_type, repetitions)
                 for algo in sorting_algorithms for data_type in datasets]

        for name, data_type, average_time in pool.map(benchmark_single_algorithm, tasks):
            results[name][data_type].append(average_time)

    pool.close()
    pool.join()

    return results


def calculate_integrals(benchmark_results, data_sizes):
    # Calculating the integral for each algorithm and data type
    integral_results = {}

    for algo in benchmark_results:
        integral_results[algo] = {}
        for data_type in benchmark_results[algo]:
            # Calculating the integral using Simpson's rule
            integral = simps(benchmark_results[algo][data_type], data_sizes)
            integral_results[algo][data_type] = integral

    return integral_results


def visualize_benchmark_results(results: dict,
                                sizes: List[int],
                                integral_results: dict) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    axes = axes.flatten()

    for idx, data_type in enumerate(['random', 'sorted', 'reverse_sorted', 'many_duplicates']):
        ax = axes[idx]
        line_label_pairs = []

        for algo in results:
            integral_score = integral_results[algo][data_type]
            line, = ax.plot(sizes, results[algo][data_type])
            label = f"{algo} (Score: {integral_score:.2f})"
            line_label_pairs.append((line, label, integral_score))

        # Sort the pairs by integral score
        line_label_pairs.sort(key=lambda x: x[2])

        # Unpack the sorted pairs
        lines, sorted_labels, *_ = zip(*line_label_pairs)

        ax.set_title(f'Time taken by Sorting Algorithms on {data_type.replace("_", " ").title()} Data')
        ax.set_xlabel('Data Size')
        ax.set_ylabel('Time (seconds)')
        ax.grid(True)

        # Create legend with sorted labels and corresponding lines
        ax.legend(lines, sorted_labels)

    plt.tight_layout()
    plt.show()


def main():
    # Adjustable parameters
    MIN_DATA_SIZE = 0
    MAX_DATA_SIZE = 250_000
    NUM_DATA_POINTS = 50

    # List of sorting algorithms to benchmark
    sorting_algorithms = [merge_sort,
                          quick_sort, shell_sort,
                          tim_sort, heap_sort,
                          my_sort_not_in_place,
                          my_sort_in_place]

    # Generating data sizes for benchmarking
    data_sizes = list(range(MIN_DATA_SIZE, MAX_DATA_SIZE + 1, MAX_DATA_SIZE // NUM_DATA_POINTS))

    # Creating a TestData instance
    test_data_generator = TestData()

    # Running the benchmark
    benchmark_results = benchmark_sorting_algorithms(sorting_algorithms, test_data_generator, data_sizes)

    # Calculating integrals
    results = calculate_integrals(benchmark_results, data_sizes)

    # Visualizing the results with rankings
    visualize_benchmark_results(benchmark_results, data_sizes, results)


if __name__ == "__main__":
    main()
