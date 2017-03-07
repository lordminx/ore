import random
from collections import Counter, namedtuple
from operator import itemgetter


class Gobble:

    def __init__(self, w, h):
        """
        Represents a Match turned into gobble dice.

        :param w: Width of the Match
        :param h: Height of the Match
        """
        self.width = w
        self.height = h
        self.gobbles = [h] * w

    def use(self):
        return self.gobbles.pop()

    pop = use

    def __str__(self):
        return str(self.gobbles)

    def __bool__(self):
        """
        Test for Truthiness based on remaining gobble dice.

            >>> gobs = Gobble(2,6)
            >>> len(gobs)
            2
            >>> gobs.use()
            6
            >>> bool(gobs)
            True
            >>> gobs.use()
            6
            >>> bool(gobs)
            False

        :return: True, while still gobble dice left.
        """
        return bool(self.gobbles)

    def __len__(self):
        return len(self.gobbles)


class Match(namedtuple("Match", ["width", "height"])):
    """Class representing an ORE match.

        >>> Match(3,7)
        3x7
        >>> match = Match(3,7)
        >>> print(match.height)
        7
        >>> print(match.width)
        3

    :param width: Number of dice in Match
    :param height: Die value of Match
    """
    __slots__ = ()

    def __str__(self):
        return "{}x{}".format(self[0], self[1])

    # Not pythonic, but allows for pretty printing of list of Match objects.
    __repr__ = __str__

    def to_gobble(self):
        """
        Turn a Match object into a Gobble object.

        :return: Gobble object representation of this Match
        """
        return Gobble(self.width, self.height)

    def __bool__(self):
        return self.width > 1


class Roll:
    """
    Class for One Roll Engine dice rolls.

        >>> default = Roll()
        >>> len(default)
        4
        >>> specific = Roll([2, 2, 2, 3, 4, 5, 6, 6, ])
        >>> specific.matches
        [3x2, 2x6]
        >>> specific.highest
        2x6
        >>> specific.widest
        3x2

    :param x: py.int, representing number of dice to roll, or py.list of ints, representing dice values.
    :param penalty: py.int of penalty dice
    :param over10: Allow rolling more than 10 dice.
    :param limit_width: Limit width of oneroll.Match to maximum of 5.
    """

    def __init__(self, x=4, penalty=0, over10=False, limit_width=False):

        if type(x) not in [int, list]:
            raise TypeError("Int or list expected but {} given.".format(type(x)))

        self.over10 = over10
        self.limit_width = limit_width
        self.penalty = penalty

        if type(x) == list:
            self.dice = sorted(x)

        else:
            x -= self.penalty

            if not over10 and x > 10:
                x = min(x, 10)
                print("Too man dice! Only rolling 10.")

            self.dice = [random.randint(1, 10) for y in range(x)]
            self.dice.sort()

            if limit_width and self.widest != ():
                while self.widest.width > 5:
                    print("Set {} too wide, rerolling...".format(self.widest))
                    index = self.dice.index(self.widest[1])
                    self.reroll(index)

    @property
    def matches(self):
        """
        Property method for retrieving a list of Matches in the Roll.

        :return: Sorted list of Match objects, if any. Else an empty list.
        """
        counter = Counter(self.dice)

        return sorted([Match(y, x) for x, y in counter.items() if y > 1], key=lambda item: item[1]) or []

    @property
    def waste(self):
        """
        Property function for retrieving waste dice, ie. die values that did not result in a Match.
        :return: Sorted list of waste die values or an empty list.
        """
        if len(self.matches) > 0:
            __waste = list(set(self.dice) - set([x[1] for x in self.matches]))
            return sorted(__waste)
        else:
            return self.dice

    @property
    def highest(self):
        """
        Retrieve Match with largest Height.
        :return: Match object of max Height; empty tuple of no Match in Roll.
        """
        if self.matches:
            return max(self.matches, key=itemgetter(1))
        else:
            return ()

    @property
    def widest(self):
        """
        Retrieve Match with max Width.
        :return: Match object with most Width; empty tuple if no Match in Roll.
        """
        if self.matches:
            _widest = max(self.matches, key=itemgetter(0))

            if _widest[0] == self.highest[0]:   # check if sets all have the same width
                _widest = self.highest          # if yes: pick highest as "tiebreaker"
            return _widest
        else:
            return ()

    def reroll(self, index):
        """
        Reroll the die at index.

        :param index: Index of the die to be replaced by a new value.
        :return: None
        """
        try:
            self.dice[index] = random.randint(1, 10)
        except IndexError as e:
            print("No die at index")
            raise e

    def reroll_all(self):
        """
        Reroll all dice in Roll.
        :return:
        """
        number = len(self.dice)
        self.dice = Roll(number,
                         over10=self.over10,
                         limit_width=self.limit_width
                         ).dice

    def __eq__(self, other):
        """
        Overridden builtin method. Rolls are equal if their dice have the same value.

        :param other: Roll object
        :return: Bool
        """
        return set(self.dice) == set(other.dice)

    def __ne__(self, other):
        return not self == other

    def __add__(self, other):
        """
        Add one dice Roll to this.
        :param other: Roll object to be added to this Roll.
        :return: A new Roll object consisting of the dice results on self and other.
        """
        try:
            new_dice = self.dice + other.dice
            over_10 = len(new_dice) > 10
            limit_width = self.limit_width or other.limit_width

            return Roll(new_dice, over10=over_10, limit_width=limit_width)
        except AttributeError:
            raise TypeError("Addition not possible between Types Roll and {}.".format(type(other)))

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)

    __iadd__ = __add__

    def __len__(self):
        return self.dice.__len__()

    def __repr__(self):
        """

            >>> roll = Roll(6)
            >>> roll == eval(roll.__repr__())
            True

        :return: Str representation of this Roll object.
        """

        rep = list()

        rep.append("x={}".format(self.dice))

        if self.penalty:
            rep.append("penalty={}".format(self.penalty))

        if self.over10:
            rep.append("over10=True")

        if self.limit_width:
            rep.append("limit_width=True")

        return "Roll(" + ", ".join(rep) + ")"

    def __str__(self):
        return str(self.matches + self.waste)


class Contest:

    def __init__(self,
                 roll1,
                 roll2=None,
                 diff=1,
                 desc="A ORE Contest"):

        self.desc = desc
        self.result = ""
        self.winner = None

        if not roll2:
            if static_contest(roll1, diff):
                self.result = "Success!"
            else:
                self.result = "Failure!"
        else:
            self._res = dynamic_contest(roll1, roll2)

            if self._res == None:

                self.result = "Neither roll achieved a match."
                self.winner = None

            elif self._res:

                self.result = "Roll 1 beats Roll 2!"
                self.winner = roll1

            else:
                self.result = "Roll 2 beats Roll 1!"
                self.winner = roll2

    @property
    def winning_roll(self):
        return self.winner





def static_contest(roll, diff=1, penalty=0):
    if type(roll) == int:
        roll = Roll(roll)

    if roll.matches and roll.matches[-1][1] >= diff:

        return True
    else:

        return False


def dynamic_contest(roll1, roll2, width_wins=False):

    assert type(roll1) in (int, Roll), "Roll object or integer expected"
    assert type(roll2) in (int, Roll), "Roll object or integer expected"

    if type(roll1) == int:
        roll1 = Roll(roll1)

    if type(roll2) == int:
        roll2 = Roll(roll2)

    if not (roll1.matches or roll2.matches):
        return None

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


def gobble_match(match, gobble):
    """Ruin a Match using Gobble dice.

    :param match: Match object to be gobbled.
    :param gobble: Gobble object to be used against match.
    :return: Tuple of (Boolean, Match, Gobble):
        Boolean: True if Gobble was both fast and high enough to know dice out of Match.
        Match: Resulting Match after applying gobble dice, None if ruined completely.
        Gobble: Gobble object with remaining Gobble dice, None if all used up."""

    assert type(match) == Match, "Match object expected"
    assert type(gobble) == Gobble, "Gobble object expected."

    if match.width > gobble.width or match.height > gobble.height:
        return False, match, gobble

    while gobble and match:
        match = Match(match.width -1, match.height)
        gobble.pop()

    if match.width <= 1:
        match = None

    if len(gobble) == 0:
        gobble = None

    return True, match, gobble


def roll(dice):
    """
    Roll <dice> # of dice and return a Roll object.

    :param dice: Number of Dice to be rolled.
    :type: int
    :return: Roll object.
    """
    assert type(dice) == int, "Argument must be an integer."

    return Roll(dice)


def roll_with_md(dice):
    """Roll <dice> # of dice and interactively add one Master Die. Returns Roll object."""

    _roll = Roll(dice)
    print("You rolled:", _roll.dice)

    if _roll.matches:
        print("Matches:", _roll.matches)

    md = int(input("What number do you want to set your Master Die to? "))

    _roll.dice.append(md)
    _roll.dice.sort()

    return _roll


def roll_with_ed(dice, ed=None):
    """Roll <dice> # of dice and add a chosen Expert Die, returning a Roll object."""

    if not ed:
        ed = int(input("What number do you want to set your Expert Die to? "))

    _roll = Roll(dice)
    _roll.dice.append(ed)
    _roll.dice.sort()

    return _roll


if __name__ == "__main__":
    match = Match(3, 6)
    gobble = Gobble(3, 7)
    gobble.width = 3

    res, match, gobble = gobble_match(match, gobble)

    print(res, match, gobble)
