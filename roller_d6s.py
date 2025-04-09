from typing import List
import random


class RollerD6s():
    def __init__(self):
        self.__tiers = [
            ("1d6",         1, 6),
            ("3d6",         3, 6),
            ("5d6",         5, 6),
            ("7d6",         7, 6),
            ("9d6",         9, 6),
        ]

    def roll_d(self, rolls: int, size: int) -> int:
        res = 0
        for _ in range(rolls):
            result = random.randint(1, size)
            res += result
        return res

    @property
    def tiers(self) -> List[str]:
        return [t[0] for t in self.__tiers]

    def roll_d_with_explosion(self, tier_index: int) -> int:
        rolls, size = self.__tiers[tier_index][1:3]
        res = 0
        for _ in range(rolls):
            result = random.randint(1, size)
            res += result
            while result == size:
                result = random.randint(1, size)
                res += result
        return res

    def roll_d_with_one_explosion(self, tier_index: int) -> int:
        rolls, size = self.__tiers[tier_index][1:3]
        res = 0
        for _ in range(rolls):
            result = random.randint(1, size)
            res += result
            if result == size:
                res += random.randint(1, size)
        return res

    def roll_d_with_advantage(self, tier_index: int) -> int:
        n_rolls, size = self.__tiers[tier_index][1:3]
        rolls = []
        for _ in range(n_rolls):
            result = random.randint(1, size)
            rolls.append(result)
        n_sixs = rolls.count(6)
        if n_sixs == size:
            return sum(rolls)
        for i in range(n_sixs):
            mini = min(rolls)
            rolls.remove(mini)
            result = random.randint(1, size)
            rolls.append(max(result, mini))
        return sum(rolls)


if __name__ == '__main__':
    roller = RollerD6s()
    for i, t in enumerate(roller.tiers):
        roller.roll_d_with_advantage(i)
