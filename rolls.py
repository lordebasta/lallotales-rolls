from collections import Counter
from tabulate import tabulate
import matplotlib.pyplot as plt
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
        res += result
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


class BoxPlotter():
    def __init__(self):
        self.values_lists = []

    def add_values(self, counter: Counter):
        values = []
        for k in counter:
            values += [k] * counter[k]
        self.values_lists.append(values)

    def plot(self):
        plt.boxplot(self.values_lists)


if __name__ == "__main__":

    successes_all = {}
    boxplotter = BoxPlotter()
    for t in tiers:
        cnt = 0
        times = 1_000_000
        maxi = 0
        rolls_c = Counter()
        successes = Counter()
        for i in range(times):
            res = roll_d_with_explosion(t[1], t[2])
            cnt += res
            maxi = max(maxi, res)
            rolls_c[res] += 1

            for i in range(0, MAX_DC, STEP_DC):
                if res >= i:
                    successes[i] += 1

        boxplotter.add_values(rolls_c)
        for k in rolls_c:
            rolls_c[k] = rolls_c[k] / times * 100
        successes_all[t[0]] = successes
        print(t[0].upper(), "avg:", cnt / times, "maxi:", maxi, end="")
        # print("\nRolls:", rolls_c, end="")

        print()

    data = []
    headers = [t[0] for t in tiers]
    for k in range(0, MAX_DC, STEP_DC):
        add = []
        add.append(k)
        for i in range(len(tiers)):
            name = tiers[i][0]
            add.append(f"{round(successes_all[name][k] / times * 100, 3)}%")
        data.append(add)

    print(tabulate(data, headers=["DC"]+headers))
    boxplotter.plot()
