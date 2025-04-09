from collections import Counter
from tabulate import tabulate
import matplotlib.pyplot as plt
from roller_d6s import RollerD6s

MAX_DC = 40
STEP_DC = 1


class BoxPlotter():
    def __init__(self):
        self.values_lists = []

    def add_values(self, counter: Counter):
        values = []
        for k in counter:
            values += [k] * counter[k]
        self.values_lists.append(values)

    def plot(self):
        fig, ax = plt.subplots()
        ax.boxplot(self.values_lists)
        plt.show()


if __name__ == "__main__":
    successes_all = {}
    boxplotter = BoxPlotter()
    roller = RollerD6s()
    print(roller.tiers)
    print(type(roller.tiers))
    for tier_index, tier in enumerate(roller.tiers):
        cnt = 0
        times = 1_000_000
        maxi = 0
        rolls_c = Counter()
        successes = Counter()
        for i in range(times):
            res = roller.roll_d_with_advantage(tier_index)
            cnt += res
            maxi = max(maxi, res)
            rolls_c[res] += 1

            for i in range(0, MAX_DC, STEP_DC):
                if res >= i:
                    successes[i] += 1

        boxplotter.add_values(rolls_c)
        for k in rolls_c:
            rolls_c[k] = rolls_c[k] / times * 100
        successes_all[tier] = successes
        print(tier.upper(), "avg:", cnt / times, "maxi:", maxi, end="")
        # print("\nRolls:", rolls_c, end="")

        print()

    data = []
    boxplotter.plot()
    headers = [t[0] for t in roller.tiers]
    for k in range(0, MAX_DC, STEP_DC):
        add = []
        add.append(k)
        for i in range(len(headers)):
            name = roller.tiers[i]
            add.append(f"{round(successes_all[name][k] / times * 100, 3)}%")
        data.append(add)

    print(tabulate(data, headers=["DC"]+headers))
