import numpy as np
from matplotlib import pyplot as plt
from prettytable import PrettyTable
import random
import gc
import math
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


def benchmark_single_algorithm(algo_data):
    algo, data, data_type, repetitions = algo_data
    total_accesses = 0
    total_comparisons = 0

    for _ in range(repetitions):
        gc.disable()
        test_data = data.copy()
        accesses, comparisons = algo(test_data)
        gc.enable()

        total_accesses += accesses
        total_comparisons += comparisons

    average_accesses = total_accesses // repetitions
    average_comparisons = total_comparisons // repetitions
    return algo.__name__, data_type, average_accesses, average_comparisons


def benchmark_sorting_algorithms(sorting_algorithms: List[Callable],
                                 data_generator: TestData,
                                 sizes: List[int],
                                 repetitions: int = 5) -> dict:
    results = {algo.__name__: {
        'random': {'accesses': [], 'comparisons': []},
        'sorted': {'accesses': [], 'comparisons': []},
        'reverse_sorted': {'accesses': [], 'comparisons': []},
        'many_duplicates': {'accesses': [], 'comparisons': []}
    } for algo in sorting_algorithms}

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

        for name, data_type, average_accesses, average_comparisons in pool.map(benchmark_single_algorithm, tasks):
            results[name][data_type]['accesses'].append(average_accesses)
            results[name][data_type]['comparisons'].append(average_comparisons)

    pool.close()
    pool.join()

    return results


def calculate_integrals(benchmark_results, data_sizes):
    integral_results = {}

    for algo in benchmark_results:
        integral_results[algo] = {'accesses': {}, 'comparisons': {}}
        for data_type in benchmark_results[algo]:
            integral_accesses = simps(benchmark_results[algo][data_type]['accesses'], data_sizes)
            integral_results[algo]['accesses'][data_type] = integral_accesses

            integral_comparisons = simps(benchmark_results[algo][data_type]['comparisons'], data_sizes)
            integral_results[algo]['comparisons'][data_type] = integral_comparisons

    return integral_results


def get_rankings(scores):
    sorted_scores = sorted(list(set(scores)))
    rank_dict = {score: idx + 1 for idx, score in enumerate(sorted_scores)}
    return [rank_dict[score] for score in scores]


def display_terminal_results(integral_results: dict) -> None:
    for data_type in ["random", "sorted", "reverse_sorted", "many_duplicates"]:
        print(f"\nResults for {data_type.replace('_', ' ').title()} Data:")

        table = PrettyTable()
        table.field_names = ["Algorithm", "Accesses Score (Log, Rank)", "Comparisons Score (Log, Rank)",
                             "Combined Score (Log, Rank)"]

        # Gather scores and rankings
        algorithm_data = []
        for algo in integral_results:
            accesses_score = math.log(integral_results[algo]['accesses'][data_type] + 1)  # +1 to avoid log(0)
            comparisons_score = math.log(integral_results[algo]['comparisons'][data_type] + 1)
            combined_score = math.log(
                integral_results[algo]['accesses'][data_type] + integral_results[algo]['comparisons'][data_type] + 1)

            algorithm_data.append((algo, accesses_score, comparisons_score, combined_score))

        # Sort by combined score
        sorted_algorithm_data = sorted(algorithm_data, key=lambda x: x[3])

        # Calculate rankings
        accesses_rankings = get_rankings([data[1] for data in sorted_algorithm_data])
        comparisons_rankings = get_rankings([data[2] for data in sorted_algorithm_data])
        combined_rankings = get_rankings([data[3] for data in sorted_algorithm_data])

        # Add rows to table
        for (algo, accesses_score, comparisons_score, combined_score), acc_rank, comp_rank, comb_rank in zip(
                sorted_algorithm_data, accesses_rankings, comparisons_rankings, combined_rankings):
            table.add_row([algo, f"{accesses_score:.2f} ({acc_rank})", f"{comparisons_score:.2f} ({comp_rank})",
                           f"{combined_score:.2f} ({comb_rank})"])

        print(table)

    print("\nAverage Results Across All Data Types:")
    average_table = PrettyTable()
    average_table.field_names = ["Algorithm", "Average Accesses (Log)", "Average Comparisons (Log)",
                                 "Average Combined Score (Log)"]

    algorithm_data = []
    for algo in integral_results:
        total_accesses_score, total_comparisons_score, total_combined_score = 0, 0, 0
        for data_type in ["random", "sorted", "reverse_sorted", "many_duplicates"]:
            accesses_score = math.log(integral_results[algo]['accesses'][data_type] + 1)
            comparisons_score = math.log(integral_results[algo]['comparisons'][data_type] + 1)

            total_accesses_score += accesses_score
            total_comparisons_score += comparisons_score

        avg_accesses_score = total_accesses_score / 4
        avg_comparisons_score = total_comparisons_score / 4
        avg_combined_score = (avg_accesses_score + avg_comparisons_score) / 2

        algorithm_data.append((algo, avg_accesses_score, avg_comparisons_score, avg_combined_score))

    sorted_algorithm_data = sorted(algorithm_data, key=lambda x: x[3])

    for algo, avg_accesses_score, avg_comparisons_score, avg_combined_score in sorted_algorithm_data:
        average_table.add_row(
            [algo, f"{avg_accesses_score:.2f}", f"{avg_comparisons_score:.2f}", f"{avg_combined_score:.2f}"])

    print(average_table)


def visualize_benchmark_results(results: dict, sizes: List[int], integral_results: dict) -> None:
    def create_total_plot(ax, algo_data, data_type, integral_data):
        plot_data = []
        for algo in algo_data:
            total_operations = np.array(algo_data[algo][data_type]['accesses']) + \
                               np.array(algo_data[algo][data_type]['comparisons'])
            integral_score = integral_data[algo]['accesses'][data_type] + integral_data[algo]['comparisons'][data_type]
            plot_data.append((algo, total_operations, integral_score))

        plot_data.sort(key=lambda x: x[2])

        for algo, total_operations, integral_score in plot_data:
            ax.plot(sizes, total_operations, label=f"{algo} (Total Score: {math.log(integral_score):.2f})")

        ax.set_title(f'Total Operations by Sorting Algorithms on {data_type.replace("_", " ").title()} Data', size=10)
        ax.set_xlabel('Data Size', size=10)
        ax.set_ylabel('Total Operations', size=10)
        ax.set_xscale('log')
        ax.grid(True)
        ax.legend()

    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    axes = axes.flatten()

    for idx, data_type in enumerate(['random', 'sorted', 'reverse_sorted', 'many_duplicates']):
        create_total_plot(axes[idx], results, data_type, integral_results)

    plt.tight_layout()
    plt.show()


def main():
    # Adjustable parameters
    MIN_DATA_SIZE = 1000
    MAX_DATA_SIZE = 100_000
    NUM_DATA_POINTS = 25

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
    integral_results = calculate_integrals(benchmark_results, data_sizes)

    # Displaying results in the terminal
    display_terminal_results(integral_results)

    # Visualise total operations
    visualize_benchmark_results(benchmark_results, data_sizes, integral_results)


if __name__ == "__main__":
    main()
