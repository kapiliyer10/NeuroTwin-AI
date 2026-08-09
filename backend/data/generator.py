import csv
import random
from pathlib import Path


def generate(n: int = 1000) -> list[list[float]]:
    data = []
    for _ in range(n):
        typing_speed = random.uniform(20, 100)
        pause_variance = random.uniform(0.1, 4)
        sentiment = random.uniform(-1, 1)
        screen_time = random.uniform(1, 12)
        stress = min(1.0, max(0.0, (1 - sentiment) * 0.35 + pause_variance * 0.12 + screen_time * 0.025))
        data.append([typing_speed, pause_variance, sentiment, screen_time, stress])
    return data


def write_csv(path: str | Path, n: int = 1000) -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["typing_speed", "pause_variance", "sentiment", "screen_time", "stress"])
        writer.writerows(generate(n))
    return output_path


if __name__ == "__main__":
    write_csv(Path(__file__).with_name("dataset.csv"))
