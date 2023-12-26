import random
import statistics
import time
from test_data_types import TestDataTypes

import numpy as np
from matplotlib import pyplot as plt
from scipy.integrate import simps

from bucket_sort import bucket_sort
from heap_sort import heap_sort
from merge_sort import merge_sort
from my_sort_2 import my_sort_2
from my_sort_1_in_place import my_sort_1_in_place
from my_sort_1_not_in_place import my_sort_1_not_in_place
from quick_sort import quick_sort
from shell_sort import shell_sort
from tim_sort import tim_sort
from my_sort_3 import my_sort_3


def run_algorithm(algo, data, repetitions=5):
    times = []
    for _ in range(repetitions):
        data_copy = data.copy()
        start = time.perf_counter()
        algo(data_copy)
        end = time.perf_counter()
        times.append(end - start)
    return times


def benchmark_algorithms(sorting_algorithms, data_types, data_sizes, repetitions=5):
    benchmark_info = {
        algo.__name__: {
            data_type: {'times': [], 'stats': []}
            for data_type in data_types.keys()
        }
        for algo in sorting_algorithms
    }

    for algo in sorting_algorithms:
        algo_name = algo.__name__
        print(algo_name)
        for data_name, data_func in data_types.items():
            for size in data_sizes:
                test_data = data_func(size)
                times = run_algorithm(algo, test_data, repetitions)
                stats = {
                    'median': statistics.median(times),
                    'min': min(times),
                    'max': max(times),
                    'mean': statistics.mean(times),
                    'stdev': statistics.stdev(times)
                }

                benchmark_info[algo_name][data_name]['times'].append(times)
                benchmark_info[algo_name][data_name]['stats'].append(stats)

    return benchmark_info


def calculate_scores(benchmark_results, data_sizes, scoring_metric='median'):
    scores = {}
    for algo in benchmark_results:
        scores[algo] = dict()
        for data_type in benchmark_results[algo]:
            stat_times = [stats[scoring_metric] for stats in benchmark_results[algo][data_type]['stats']]
            score = simps(stat_times, data_sizes)
            scores[algo][data_type] = np.log(score)

    return scores


def visualise_benchmark(benchmark_info, data_sizes, data_types, scores, scoring_metric='median'):
    fig, axes = plt.subplots(3, 2, figsize=(15, 10))
    axes = axes.flatten()

    for idx, data_type in enumerate(data_types.keys()):
        plot_data = []
        for algo in benchmark_info:
            stat_times = [stats[scoring_metric] for stats in benchmark_info[algo][data_type]['stats']]
            stat_times = np.array(stat_times)
            score = scores[algo][data_type]
            plot_data.append((algo, stat_times, score))

        plot_data.sort(key=lambda x: x[2])  # Sort by score

        for algo, stat_times, score in plot_data:
            axes[idx].plot(data_sizes, stat_times, label=f"{algo} (Score: {score:.2f})")

        axes[idx].set_title(f'Execution Time by Sorting Algorithms on {data_type.replace("_", " ").title()} Data',
                            size=10)
        axes[idx].set_xlabel('Data Size', size=10)
        axes[idx].set_ylabel('Execution Time (seconds)', size=10)
        axes[idx].grid(True)
        axes[idx].legend(loc='upper left', prop={'size': 8})

    plt.tight_layout()
    plt.show()


def pre_check(sorting_algorithms, data_types, test_size=1000, repetitions=5):
    for _ in range(repetitions):
        test_data = data_types['random'](test_size)
        expected_result = sorted(test_data)

        for algo in sorting_algorithms:
            if algo.__name__ in ['my_sort_1_not_in_place', 'merge_sort',
                                 'my_sort_2', 'bucket_sort', 'my_sort_3']:
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
    max_data_size = 5
    num_data_points = (max_data_size - min_data_size) * 5 + 1

    # Sorting algorithms
    sorting_algorithms = [
        quick_sort,
        bucket_sort,
        my_sort_2,
        heap_sort,
        my_sort_1_not_in_place,
        shell_sort,
        tim_sort,
        my_sort_1_in_place,
        merge_sort,
        my_sort_3
    ]
    random.shuffle(sorting_algorithms)

    data_types = {
        "random": TestDataTypes.random_data,
        "sorted": TestDataTypes.sorted_data,
        "reverse_sorted": TestDataTypes.reverse_sorted_data,
        "duplicates": TestDataTypes.duplicates_data,
        "skewed": TestDataTypes.skewed_data,
    }

    # Generating data sizes for benchmarking
    data_sizes = sorted(set(np.logspace(min_data_size, max_data_size, num_data_points, dtype=int)))

    # Check algorithms sort correctly
    pre_check(sorting_algorithms, data_types)

    # Benchmark the algorithms
    benchmark_info = benchmark_algorithms(sorting_algorithms, data_types, data_sizes)

    # Score the results
    scores = calculate_scores(benchmark_info, data_sizes)

    # Visualise the benchmark
    visualise_benchmark(benchmark_info, data_sizes, data_types, scores)


if __name__ == "__main__":
    main()
