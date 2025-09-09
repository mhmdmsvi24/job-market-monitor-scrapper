import asyncio
import csv
from pathlib import Path

def create_dir(path: Path) -> bool:
    """

    Args:
      path: Path:

    Returns:

    """
    if (path.exists(follow_symlinks=False)):
        print(f"This directory already exists")
        return False
    else:
        Path.mkdir(path, exist_ok=False)

    return True


def create_csv(base_name: str, create_number: int, rows: list, path: Path | str = None) -> None:
    """

    Args:
      base_name: str:
      create_number: int:
      rows: list:
      path: Path | str:  (Default value = None)

    Returns:

    """
    files_path = []

    for i in range(create_number):
        file_name = f"{base_name}-{i + 1}.csv"

        if (Path(path / file_name).exists(follow_symlinks=False)):
            file_name = f"{base_name}-{i + 1}-backup.csv"
            print(f"The {file_name} already exists, to prevent damage the data is created in {file_name}")
        else:
            file_name = f"{base_name}-{i + 1}.csv"

        files_path.append(file_name)
        with open(path / file_name, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=rows)
            writer.writeheader()

    return files_path


def write_csv(data: list[dict[str, str]], file: str, rows: list[str]) -> None:
    """

    Args:
      data:
      file:
      rows:

    Returns:

    """
    with open(file, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows)
        writer.writerows(data)


async def write_csv_async(data: list[dict[str, str]], file: Path, rows: list[str], lock: asyncio.Lock) -> None:
    async with lock:
        write_csv(data, file, rows)
