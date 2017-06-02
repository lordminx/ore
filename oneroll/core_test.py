from oneroll.core import *
import pytest


class TestGobble:
    """Tests for the Gobble class"""

class TestRoll:
    """Tests for the Roll class."""

    def test_construction(self):
        """Rolls can be constructed from an integer or a list of integers, otherwise it should throw TypeError."""

        with pytest.raises(TypeError) as exinfo:
            Roll("string")
        with pytest.raises(TypeError) as exinfo:
            Roll(("Tuple", 12))

        assert "Int or list expected" in str(exinfo.value)

    def test_construction_dice_sorted(self):
        """When constructed from a list of values, the list should be sorted and saved under Roll().dice."""
        dice = [2, 3, 1, 4, 5]

        assert Roll(dice).dice == sorted(dice)
        assert set(Roll(dice).dice) == set(dice)

    def test_construction_over10(self):
        """A Roll constructed from an int larger than 10 without over10=True should only include 10 dice."""
        assert len(Roll(25)) == 10
        assert len(Roll(25, over10=True)) == 25

    def test_construction_penalty(self):
        """The penalty argument of a Roll must be subtracted from the number of dice before rolling."""
        assert len(Roll(10, penalty=3)) == 7
        assert len(Roll(20, penalty=13)) == 7
        assert len(Roll(20, penalty=3)) == 10   # Penalties subtract before limiting the pool to 10 dice
        assert len(Roll(20, penalty=3, over10=True)) == 17

    def test_construction_limit_width(self, capsys):
        """If the limit_width flag is set, a Roll should reroll all matches over width 5."""
        roll = Roll(40, over10=True, limit_width=True)
        out, err = capsys.readouterr()
        assert "too wide, rerolling" in out
        assert roll.widest.width <= 5

        roll = Roll(100, over10=True)
        assert roll.widest.width > 5

    def test_matches(self):
        """
        A Roll with two or more dice of the same value returns a Match object with its .matches property.

        If no matches are found, an empty list is returned.
        """
        roll1 = Roll([1, 1, 2, 2, 3, 3, 3])
        roll2 = Roll([1, 2, 3, 4, 5])

        assert len(roll1.matches) == 3
        assert str(roll1.matches[-1]) == "3x3"
        assert str(roll1.matches[0]) == "2x1"

        assert roll2.matches == []

    def test_matches_highest_widest(self):
        """
        A Roll which results in a match has also a 'highest' and 'widest' match, which return the corresponding Match objects.

        In Rolls without matches, these properties return empty tuples.
        """
        roll1 = Roll([1, 1, 1, 2, 3, 3])
        roll2 = Roll([1, 2, 3, 4, 5])

        assert str(roll1.highest) == "2x3"
        assert str(roll1.widest) == "3x1"

        assert roll2.highest == ()
        assert roll2.widest == ()

    def test_waste_empty(self):
        roll = Roll([2, 2, 3, 3, 3])

        assert roll.waste == []

    def test_waste_partial(self):
        roll = Roll([1, 2, 3, 4, 5, 5, 5])

        assert roll.waste == [1, 2, 3, 4]
        assert len(roll) == len(roll.waste) + sum(x.width for x in roll.matches)

    def test_addition(self):
        """When adding two Rolls the length of the result should be the sum of their lengths."""
        add_roll = Roll() + Roll()
        assert len(add_roll) == 8
        assert len(Roll(10) + Roll(10)) == 20

    def test_addition_exception(self):
        """Trying to add a Roll to some other type should throw an exception."""
        roll = Roll(4)
        with pytest.raises(TypeError):
            roll + 4

        with pytest.raises(TypeError):
            roll + "foo"

        with pytest.raises(TypeError):
            roll + []

    def test_addition_equality(self):
        """When adding two Rolls, the result should be equal to a Roll consisting of the same dice."""
        roll1 = Roll([1, 2, 3])
        roll2 = Roll([4, 5])

        assert (roll1 + roll2) == Roll([1, 2, 3, 4, 5])
        assert (roll1 + Roll(0)) == roll1
        assert (roll1 + roll2) != roll1
        assert (roll1 + roll2) == (roll2 + roll1)

    def test_addition_sum(self):
        """Summing multiple Rolls should be possible."""
        rolls = [Roll(), Roll(), Roll()]
        sum(rolls)

    def test_addition_over10(self):
        """Adding Rolls with a sum of dice greater than ten should set the results over10 field to True."""
        roll1 = Roll(6)
        roll2 = Roll(6)

        assert not roll1.over10
        assert not roll2.over10
        assert (roll1 + roll2).over10

    def test_equality_given_dice(self):
        """Two Rolls should be equal irrespective of the order of their dice."""
        dice1 = [1, 2, 3, 4, 5]
        dice2 = [5, 4, 3, 2, 1]
        assert Roll(dice1) == Roll(dice2)

    def test_equality_fail(self):
        """Rolls with different dice lists should not be equal."""
        dice1 = [1, 2, 3, 4, 5]
        assert Roll(dice1) != Roll()
        assert Roll(dice1) != Roll([1, 1, 1, 1, 1])

    def test_len(self):
        """Roll objects should have a length of the number of dice in them."""
        assert len(Roll(5)) == 5
        assert len(Roll()) == 4
        assert len(Roll()) == len(Roll([1, 1, 1, 1]))
