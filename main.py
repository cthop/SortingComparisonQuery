import numpy as np
from matplotlib import pyplot as plt
from prettytable import PrettyTable
import gc
import statistics
from typing import Callable, List
from scipy.integrate import simps
from multiprocessing import Pool, cpu_count
import time
from test_data import TestData

from merge_sort import merge_sort
from quick_sort import quick_sort
from shell_sort import shell_sort
from tim_sort import tim_sort
from heap_sort import heap_sort
from my_sort_not_in_place import my_sort_not_in_place
from my_sort_in_place import my_sort_in_place


def benchmark_single_algorithm(algo_data):
    algo, data, data_type, repetitions = algo_data
    times = []

    # Warm-up runs
    for _ in range(3):
        test_data = data.copy()
        gc.disable()
        algo(test_data)
        gc.enable()

    # Timing runs
    for _ in range(repetitions):
        test_data = data.copy()
        gc.disable()
        start_time = time.perf_counter()
        algo(test_data)
        end_time = time.perf_counter()
        gc.enable()

        times.append(end_time - start_time)

    median_time = statistics.median(times)
    min_time = min(times)
    max_time = max(times)
    std_dev = statistics.stdev(times)

    return algo.__name__, data_type, median_time, min_time, max_time, std_dev


def benchmark_sorting_algorithms(sorting_algorithms: List[Callable],
                                 data_generator: TestData,
                                 sizes: List[int],
                                 repetitions: int = 5) -> dict:
    results = {algo.__name__: {
        'random': [],
        'sorted': [],
        'reverse_sorted': [],
        'many_duplicates': []
    }
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
                 for algo in sorting_algorithms
                 for data_type in datasets]

        for name, data_type, median_time, min_time, max_time, std_dev in pool.map(benchmark_single_algorithm, tasks):
            results[name][data_type].append((median_time, min_time, max_time, std_dev))

    pool.close()
    pool.join()

    return results


def calculate_score(benchmark_results, data_sizes):
    scores = {}

    for algo in benchmark_results:
        scores[algo] = {}
        for data_type in benchmark_results[algo]:
            median_times = [data[0] for data in benchmark_results[algo][data_type]]
            score = simps(median_times, data_sizes)
            scores[algo][data_type] = np.log(score)

    return scores


def visualize_benchmark_results(results: dict,
                                sizes: List[int],
                                scores: dict) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    axes = axes.flatten()

    for idx, data_type in enumerate(['random', 'sorted', 'reverse_sorted', 'many_duplicates']):
        plot_data = []
        for algo in results:
            median_times, *_ = zip(*results[algo][data_type])
            median_times = np.array(median_times)
            score = scores[algo][data_type]
            plot_data.append((algo, median_times, score))

        plot_data.sort(key=lambda x: x[2])  # Sort by score

        for algo, median_times, score in plot_data:
            axes[idx].plot(sizes, median_times, label=f"{algo} (Score: {score:.2f})")

        axes[idx].set_title(f'Execution Time by Sorting Algorithms on {data_type.replace("_", " ").title()} Data',
                            size=10)
        axes[idx].set_xlabel('Data Size', size=10)
        axes[idx].set_ylabel('Execution Time (seconds)', size=10)
        # axes[idx].set_xscale('log')
        # axes[idx].set_yscale('log')
        axes[idx].grid(True)
        axes[idx].legend(loc='upper left', prop={'size': 8})

    plt.tight_layout()
    plt.show()


def print_and_save_results(results: dict, scores: dict) -> None:
    output_str = ""

    for data_type in ['random', 'sorted', 'reverse_sorted', 'many_duplicates']:
        table_data = []
        for algo in results:
            median_times, min_times, max_times, std_devs = zip(*results[algo][data_type])
            score = scores[algo][data_type]
            table_data.append((algo, statistics.median(median_times), min(min_times), max(max_times),
                               statistics.mean(std_devs), score))

        # Sort by score (6th element in the tuple)
        table_data.sort(key=lambda x: x[5])

        table = PrettyTable()
        table.field_names = ["Algorithm", "Median Time", "Min Time", "Max Time", "Average Std Dev", "Score"]

        for row in table_data:
            adjusted_row = [f"{ele:.6f}" if isinstance(ele, (float, int)) else ele for ele in row]
            table.add_row(adjusted_row)

        print(f"\nResults for {data_type.replace('_', ' ').title()} Data:")
        print(table)

        output_str += f"Results for {data_type.replace('_', ' ').title()} Data:\n"
        output_str += str(table)
        output_str += "\n\n"

    with open("results.txt", "w") as file:
        file.write(output_str)


def pre_benchmark_check(sorting_algorithms: List[Callable],
                        test_data_generator: TestData,
                        test_size: int = 1000,
                        repetitions: int = 5) -> bool:
    for _ in range(repetitions):
        test_data = test_data_generator.random_data(test_size)
        expected_result = sorted(test_data)

        for algo in sorting_algorithms:
            if algo.__name__ in ['my_sort_not_in_place', 'merge_sort']:
                if algo(test_data.copy()) != expected_result:
                    print(f"Algorithm {algo.__name__} failed the pre-benchmark check.")
                    return False
            else:
                data_copy = test_data.copy()
                algo(data_copy)
                if data_copy != expected_result:
                    print(f"Algorithm {algo.__name__} failed the pre-benchmark check.")
                    return False

    print("All algorithms passed the pre-benchmark check.")
    return True


def main():
    # Adjustable parameters
    min_data_size = 0
    max_data_size = 6
    num_data_points = (max_data_size - min_data_size) * 20 + 1

    # List of sorting algorithms to benchmark
    sorting_algorithms = [merge_sort,
                          quick_sort, shell_sort,
                          tim_sort, heap_sort,
                          my_sort_not_in_place,
                          my_sort_in_place]

    # Generating data sizes for benchmarking
    data_sizes = sorted(set(np.logspace(min_data_size, max_data_size, num_data_points, dtype=int)))

    # Creating a TestData instance
    test_data_generator = TestData()

    # Pre-benchmark check
    if not pre_benchmark_check(sorting_algorithms, test_data_generator):
        print("Pre-benchmark check failed. Please check the sorting algorithms.")
        return

    # Running the benchmark
    benchmark_results = benchmark_sorting_algorithms(sorting_algorithms, test_data_generator, data_sizes)

    # Calculating scores
    scores = calculate_score(benchmark_results, data_sizes)

    # Get raw results
    print_and_save_results(benchmark_results, scores)

    # Visualise total operations
    visualize_benchmark_results(benchmark_results, data_sizes, scores)


if __name__ == "__main__":
    main()
