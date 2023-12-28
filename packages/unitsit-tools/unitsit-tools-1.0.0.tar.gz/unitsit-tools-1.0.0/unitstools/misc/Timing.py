import statistics
import timeit

GREEN = '\033[92m'
RESET = '\033[0m'


def apply_color(color, text):
    return f"{color}{text}{RESET}"


def print_timing_results(func_name, timings, repeat, number):
    print(apply_color(GREEN, f"Function: "), func_name)
    print(apply_color(GREEN, f"Execution Time for a single run:"), f"{min(timings) / number:.6f} seconds")
    print(apply_color(GREEN, f"Avg. Execution Time for {number} iterations "
                             f"(across {repeat} repeats):"), f"{statistics.mean(timings):.6f} seconds")
    print(apply_color(GREEN, f"Median Execution Time: "), f"{statistics.median(timings):.6f} seconds")
    print(apply_color(GREEN, f"Standard Deviation: "), f"{statistics.stdev(timings):.6f} seconds")
    print(apply_color(GREEN, f"Min. Execution Time: "), f"{min(timings):.6f} seconds")
    print(apply_color(GREEN, f"Max. Execution Time: "), f"{max(timings):.6f} seconds")
    print(apply_color(GREEN, f"Total Execution Time: "), f"{sum(timings):.6f} seconds")


def timing_decorator(repeat=3, number=5):
    if not isinstance(repeat, int) or not isinstance(number, int) or repeat <= 0 or number <= 0:
        raise ValueError("Invalid values for repeat and number. Both should be positive integers.")

    def decorator(func):
        def wrapper(*args, **kwargs):
            timer = timeit.Timer(lambda: func(*args, **kwargs))
            timings = timer.repeat(repeat=repeat, number=number)

            print_timing_results(func.__name__, timings, repeat, number)

            return func(*args, **kwargs), min(timings) / number

        return wrapper

    return decorator


def timing_function(func, repeat=3, number=5, *args, **kwargs):
    if not isinstance(repeat, int) or not isinstance(number, int) or repeat <= 0 or number <= 0:
        raise ValueError("Invalid values for repeat and number. Both should be positive integers.")

    timer = timeit.Timer(lambda: func(*args, **kwargs))
    timings = timer.repeat(repeat=repeat, number=number)

    print_timing_results(func.__name__, timings, repeat, number)

    return func(*args, **kwargs), min(timings) / number
