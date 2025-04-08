from collections import Counter
from tabulate import tabulate
import random

MAX_DC = 40
STEP_DC = 1

tiers = [
    ("1d6",         1, 6),
    ("3d6",         3, 6),
    ("5d6",         5, 6),
    ("7d6",         7, 6),
    ("9d6",         9, 6),
]


def roll_d(rolls: int, size: int) -> int:
    res = 0
    for _ in range(rolls):
        result = random.randint(1, size)
        if result > 3:
            res += 1
    return res


def roll_d_with_explosion(rolls, size: int) -> int:
    res = 0
    for _ in range(rolls):
        result = random.randint(1, size)
        res += result
        while result == size:
            result = random.randint(1, size)
            res += result
    return res


def get_success_chance_roll_vs(i_a, i_b) -> float:
    wins = 0
    times = 2_000_000
    rolls_a = tiers[i_a][1]
    size_a = tiers[i_a][2]
    rolls_b = tiers[i_b][1]
    size_b = tiers[i_b][2]

    for i in range(times):
        if roll_d_with_explosion(rolls_a, size_a) >= roll_d_with_explosion(rolls_b, size_b):
            wins += 1

    return wins/times


if __name__ == "__main__":
    add = []
    for i1, t1 in enumerate(tiers):
        new = [t1[0]]
        for i2, t2 in enumerate(tiers):
            chance = get_success_chance_roll_vs(i1, i2)
            chance *= 100
            chance = round(chance)
            chance = f"{chance}%"
            new.append(chance)
        add.append(new)

    headers = [""] + [t[0] for t in tiers]

    print(tabulate(add, headers=headers))
