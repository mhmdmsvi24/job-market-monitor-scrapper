import asyncio
import csv
import time
import tracemalloc
from pathlib import Path


def create_dir(path: Path) -> bool:
    """Create a new directory if it does not already exist.

    Args:
        path (Path): The directory path to create.

    Returns:
        bool:
            - True if the directory was successfully created.
            - False if the directory already exists.
    """
    if path.exists(follow_symlinks=False):
        print("This directory already exists")
        return False
    else:
        Path.mkdir(path, exist_ok=False)

    return True


def create_csv(
    base_name: str, create_number: int, rows: list, path: Path | str = None
) -> list[str]:
    """Create one or more CSV files with headers.

    Args:
        base_name (str): Base name for the CSV files.
        create_number (int): Number of CSV files to create.
        rows (list): Column headers for the CSV file(s).
        path (Path | str, optional): Directory in which to create files. Defaults to None.

    Returns:
        list[str]: A list of created file names.
    """
    files_path = []

    for i in range(create_number):
        file_name = f"{base_name}-{i + 1}.csv"

        if Path(path / file_name).exists(follow_symlinks=False):
            file_name = f"{base_name}-{i + 1}-backup.csv"
            print(
                f"The {file_name} already exists, to prevent data loss the file was created as {file_name}"
            )
        else:
            file_name = f"{base_name}-{i + 1}.csv"

        files_path.append(file_name)
        with open(path / file_name, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=rows)
            writer.writeheader()

    return files_path


def write_csv_sync(data: list[dict[str, str]], file: str, rows: list[str]) -> None:
    """Write data synchronously to a CSV file.

    Args:
        data (list[dict[str, str]]): A list of row dictionaries to write.
        file (str): The path to the CSV file.
        rows (list[str]): The field names for the CSV file.

    Returns:
        None
    """
    with open(file, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows)
        writer.writerows(data)


async def write_csv(
    data: list[dict[str, str]], file: Path, rows: list[str], lock: asyncio.Lock
) -> None:
    """Write data asynchronously to a CSV file.

    This function ensures safe concurrent writes by using an asyncio lock.

    Args:
        data (list[dict[str, str]]): A list of row dictionaries to write.
        file (Path): The path to the CSV file.
        rows (list[str]): The field names for the CSV file.
        lock (asyncio.Lock): A lock to prevent race conditions during concurrent writes.

    Returns:
        None
    """
    async with lock:
        write_csv_sync(data, file, rows)


import time


def benchmark(func):
    async def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = await func(*args, **kwargs)
        end = time.perf_counter()
        current, peak = tracemalloc.get_traced_memory()
        print(f"-----> Scraping finished in {end - start:.2f} seconds")
        print(f"-----> Current memory usage: {current / 1024 / 1024:.2f} MB")
        print(f"-----> Peak memory usage: {peak / 1024 / 1024:.2f} MB")

        return result

    return wrapper
