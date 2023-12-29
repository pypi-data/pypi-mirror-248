import statistics
import timeit

# ANSI escape codes for terminal text color
GREEN = "\033[92m"
RESET = "\033[0m"


def apply_color(color, text):
    """Apply the specified color to the given text."""
    return f"{color}{text}{RESET}"


def print_timing_results(func_name, timings, repeat, number):
    """Print timing results for a function."""
    print(apply_color(GREEN, "Function: "), func_name)
    print(
        apply_color(GREEN, "Execution Time for a single run:"),
        f"{min(timings) / number:.6f} seconds",
    )
    print(
        apply_color(
            GREEN,
            f"Avg. Execution Time for {number} iterations (across {repeat} repeats):",
        ),
        f"{statistics.mean(timings):.6f} seconds",
    )
    print(
        apply_color(GREEN, "Median Execution Time: "),
        f"{statistics.median(timings):.6f} seconds",
    )
    print(
        apply_color(GREEN, "Standard Deviation: "),
        f"{statistics.stdev(timings):.6f} seconds",
    )
    print(
        apply_color(GREEN, "Min. Execution Time: "),
        f"{min(timings):.6f} seconds",
    )
    print(
        apply_color(GREEN, "Max. Execution Time: "),
        f"{max(timings):.6f} seconds",
    )
    print(
        apply_color(GREEN, "Total Execution Time: "),
        f"{sum(timings):.6f} seconds",
    )


def timing_decorator(repeat=3, number=5):
    """
    A decorator to measure the execution time of a function.

    Parameters:
        - repeat (int): Number of times to repeat the timing measurement.
        - number (int): Number of times to execute the function for each measurement.

    Returns:
        - decorator function
    """
    if (
        not isinstance(repeat, int)
        or not isinstance(number, int)
        or repeat <= 0
        or number <= 0
    ):
        raise ValueError(
            "Invalid values for repeat and number. Both should be positive integers."
        )

    def decorator(func):
        def wrapper(*args, **kwargs):
            """Wrapper function to measure the execution time."""
            timer = timeit.Timer(lambda: func(*args, **kwargs))
            timings = timer.repeat(repeat=repeat, number=number)

            print_timing_results(func.__name__, timings, repeat, number)

            return func(*args, **kwargs), min(timings) / number

        return wrapper

    return decorator


def timing_function(func, repeat=3, number=5, *args, **kwargs):
    """
    Measure the execution time of a function.

    Parameters:
        - func (function): The function to measure.
        - repeat (int): Number of times to repeat the timing measurement.
        - number (int): Number of times to execute the function for each measurement.

    Returns:
        - Tuple: Result of the function, Minimum execution time per run.
    """
    if (
        not isinstance(repeat, int)
        or not isinstance(number, int)
        or repeat <= 0
        or number <= 0
    ):
        raise ValueError(
            "Invalid values for repeat and number. Both should be positive integers."
        )

    timer = timeit.Timer(lambda: func(*args, **kwargs))
    timings = timer.repeat(repeat=repeat, number=number)

    print_timing_results(func.__name__, timings, repeat, number)

    return func(*args, **kwargs), min(timings) / number
