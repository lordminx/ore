# OneRoll
A Python library for the One Roll Engine rpg rules.

## Introduction

My goal with the OneRoll module is to create a pythonic library for the One Roll Engine rpg rules set.
This will not be a dice-rolling app or something like that (Though there will probably be some utility scripts that can be used for that.), but a tool for people to create their own ORE apps in python.

For this to work, the lib should be as easy to use and intuitive as possible, with a pythonic API and (eventually) good documentation.

Right now, though, OneRoll is basically a rough sketch of a library, with a lot of work left to do.

So far, the focus has been on the One Roll Engine version presented in Reign, because this project grew out of a setting generation project using Reigns company rules.
(You can still see that code in the `companies` submodule.)

## Tutorial

### Installation

While OneRoll will probably land in PyPI some day, for now, the only way to use it is to `git clone` this repository.
For now, the repository has two branches:

* The code in `master` mostly works and the idea is to keep it "releaseworthy".
* In `dev` sits my current delevopment version. Stuff might be broken every now and then, but if you want to get the most current version or help develop, you probably want to pull from there.

### Module Overview
**Disclaimer**: This will almost certainly change a lot in the future.

For now, there are two main components to the library:

- In `core.py` are the central classes and methods for the ORE engine, like the `Roll` class (Representing a single roll of an ORE dice pool.) or the contest functions.
- `companies.py` holds code for representing and randomly generating Reign companies using the One Roll Companies rules.

### Usage

The basic unit of OneRoll is the `Roll` class. It represents a single roll of an ORE dice pool. When initialized without firther arguments, it defaults to a random roll of 4 dice.

    >>> pool =  Roll()
    >>> print(pool)
    [2, 3, 4, 4] #random example

A `Roll` can be initialized either using an `int`, which means it will roll that many d10, or using a list of ints, which represent a specific roll.

    >>> specific = Roll([2, 2, 3, 3, 3, 4, 4, 4, 4])
    >>> len(specific.matches)
    3
    >>> specific.matches
    [2x2, 3x3, 4x4]

You can also have it roll with penalties, in which case the number of rolled dice is reduced. By default, it also rolls at most 10 dice, though that can be overriding by setting the `over10` argument to `True`.

    >>> penalty = Roll(5, penalty=2)
    >>> len(penalty)
    3
    >>> print(penalty)
    [1, 2, 3]   # for example
    >>> huge = Roll(15, over10=True)
    >>> print(huge)
    [3x2, 3x3, 2x6, 2x9, 1, 4, 5, 7, 8]
    >>> len(huge)
    15


The class saves the rolled dice as a list internally, but has various other properties to access the rolls results.

    >>> specific.dice
    [2, 2, 3, 3, 3, 4, 4, 4, 4]
    >>> specific.widest
    4x4
    >>> specific.waste
    []   # no waste dice, as all dice are in a match.
    >>> if specific.matches:    # allows for easy "truthiness" check of rolls
    ...     print("Success!")
    "Success!"

As you can see, `Roll` objects are quite pythonic: They behave correctly when checking for lengths, they print nicely, they are easily accessible.
They are also easily changeable:

    >>> fail = Roll([1, 2, 3, 4])
    >>> fail.matches
    []
    >>> fail.dice.append(4)
    >>> fail.matches
    [2x4]
    >>> fail.reroll(0)
    >>> fail.dice
    [9, 2, 3, 4, 4]     # Rerolled the 1 and got, for example, a 9 instead.


## Contribution

## TODOs

