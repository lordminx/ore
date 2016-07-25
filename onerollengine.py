import random
from collections import Counter, namedtuple
from operator import itemgetter


class Match(namedtuple("Match", ["width", "height"])):
    __slots__ = ()

    def __str__(self):
        return "{}x{}".format(self[0], self[1])
    __repr__ = __str__


class Roll:
    def __init__(self, x, penalty=0, over10=False,):
        x -= penalty

        if not over10 and x > 10:
            x = min(x, 10)
            print("Too man dice! Only rolling 10.")

        self.dice = [random.randint(1, 10) for y in range(x)]
        self.dice.sort()

    @property
    def matches(self):
        counter = Counter(self.dice)

        return sorted([Match(y, x) for x, y in counter.items() if y > 1], key=lambda item: item[1]) or []

    @property
    def waste(self):
        if len(self.matches) > 0:
            __waste = list(set(self.dice) - set([x[1] for x in self.matches]))
            return sorted(__waste)
        else:
            return self.dice

    @property
    def highest(self):
        if self.matches:
            return max(self.matches, key=itemgetter(1))
        else:
            return ()

    @property
    def widest(self):
        if self.matches:
            _widest = max(self.matches, key=itemgetter(0))\

            if _widest[0] == self.highest[0]:   # check if sets all have the same width
                _widest = self.highest          # if yes: pick highest as "tiebreaker"
            return _widest
        else:
            return ()


class Contest:

    def __init__(self, roll1, roll2=None, diff=1):
        self.result = ""

        if not roll2:
            if static_contest(roll1, diff):
                self.result = "Success!"
            else:
                self.result = "Failure!"
        else:
            if dynamic_contest(roll1, roll2):
                self.result = "Roll 1 beats Roll 2!"
            else:
                self.result = "Roll 2 beats Roll 1!"


def static_contest(roll, diff=1, penalty=0):
    if type(roll) == int:
        roll = Roll(roll)

    if roll.matches and roll.matches[-1][1] >= diff:

        return True
    else:

        return False


def dynamic_contest(roll1, roll2, width_wins=False):
    if type(roll1) == int:
        roll1 = Roll(roll1)

    if not roll1.matches:

        return False

    if not roll2.matches:

        return True

    if width_wins:
        _width1 = sorted(roll1.matches, key=lambda x:x[0])[-1][0]
        _width2 = sorted(roll2.matches, key=lambda x:x[0])[-1][0]
        return _width1 > _width2
    else:

        return roll1.matches[-1][1] > roll2.matches[-1][1]

def gobble(roll, highest=True):
    if type(roll) == int:
        roll = Roll(roll)

    if roll.matches:
        if highest:
            roll.gobble = []



def roll(dice):
    return Roll(dice)


def roll_with_md(dice):
    pass


def roll_with_ed(dice):
    pass







if __name__ == "__main__":
    print("Rolling...")
    foo = Roll(12)

    print("Matches:", foo.matches)
    print("Waste Dice;", foo.waste)
    print("Dice Roll:", foo.dice)
    print("highest:", foo.highest)
    print("widest:", foo.widest)

    print("Roll against diff 5!")
    print(Contest(foo, diff=5).result)

    print("Dynamic Contest against 5 dice;")
    bar = Roll(5)
    print(bar.matches)
    print(Contest(foo, bar).result)

    Blub = Match(1, 2)
    Blablub = Match(1, 2)
    print(Blub == Blablub)

    testdict = {}
    testdict[Blub] = Blablub
    print(testdict)