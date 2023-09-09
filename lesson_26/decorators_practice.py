from functools import wraps
import time
import asyncio

def timeit(func):
    if asyncio.iscoroutinefunction(func):
        @wraps(func)
        async def async_timeit_wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = await func(*args, **kwargs)
            end_time = time.perf_counter()
            total_time = end_time - start_time
            print(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')
            return result
        return async_timeit_wrapper
    else:
        @wraps(func)
        def sync_timeit_wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            total_time = end_time - start_time
            print(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')
            return result
        return sync_timeit_wrapper

@timeit
def calculate_something(num):
    """
    Simple function that returns sum of all numbers up to the square of num.
    """
    total = sum(x for x in range(0, num**2))
    return total

@timeit
async def async_calculate_something(num):
    """
    Asynchronous version of the calculate_something function.
    """
    await asyncio.sleep(10)  # Simulating some async operation
    total = sum(x for x in range(0, num**2))
    return total

if __name__ == '__main__':
    calculate_something(10)
    calculate_something(100)
    calculate_something(1000)
    calculate_something(10000)
    
    asyncio.run(async_calculate_something(10))
