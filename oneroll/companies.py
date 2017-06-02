from collections import Counter
from random import choice
from textwrap import dedent
import tracery

from oneroll.core import Roll


_actions = {
    "attack": (("might", "treasure"), ("might", "territory")),
    "being_informed": (("influence", "sovereignty"), ("influence", "treasure")),
    "counter-espionage": (("influence", "territory"), ("influence", "treasure")),
    "defend": (("might", "territory"), ("might", "treasure")),
    "espionage": (("influence", "treasure"), ("influence", "sovereignty")),
    "improve_sovereignty": (("territory", "treasure"), ()),
    "policing": (("might", "sovereignty"), ("influence", "might")),
    "improve_influence": (("sovereignty", "territory"), ()),
    "improve_might": (("sovereignty", "territory"), ()),
    "unconventional_warfare": (("influence", "might"), ("might", "sovereignty")),
    }


_ORC_table = {
    1: {
        1: ["Oracle", ("influence", 1)],
        2: ["Gossipy Old Folks", ("influence", 1), ("assets", "Culture of Shame and Gossip")],
        3: ["Paid Network of Informants", ("influence", 1)],
        4: ["Elite Secret Agents", ("influence", 1)],
        5: ["Traitor", ("assets", "Mole")]

        },

    2: {
        1: ["Advantageous Marriage", ("assets", "Entangling Alliance")],
        2: ["Access to Bored, Jaded Sybarites", ("influence", 1), ("assets", "Cultural Tradition")],
        3: ["Open Ears (and Doors) for the Riff-Raff", ("influence", 1)],
        4: ["Good Roads, Fast Horses", ("influence", 1)],
        5: ["Elaborately Titled Diplomatic Corps", ("assets", "Eloquent Diplomats")]
    },

    3: {
        1: ["Loan Operation", ("treasure", 1)],
        2: ["Fertile Foothills", ("treasure", 1), ("assets", "Civic Theater")],
        3: ["Bountiful Peaks", ("treasure", 1)],
        4: ["Towering Crags", ("treasure", 1)],
        5: ["Implacable Sky Walls", ("assets", "Defensible Terrain")],
    },

    4: {
        1: ["Exotic Crop", ("assets", "Unbalanced Economy")],
        2: ["Pleasant Copses", ("treasure", 1), ("assets", "Shipshape Navy")],
        3: ["Extensive Woods", ("treasure", 1)],
        4: ["Vast Tracts of Timber", ("treasure", 1)],
        5: ["Deep Dark Forests", ("assets", "Magic Resistant")]
    },

    5: {
        1: ["Murderous Thugs With No Moral Center", ("assets", "Sinister Operatives")],
        2: ["Storied Warrior Family", ("might", 1), ("assets", "Defiant Tradition")],
        3: ["Traditional Soldier Caste", ("might", 1)],
        4: ["Code of Death Before Dishonor", ("might", 1)],
        5: ["Elite Soldier-Sorcerers", ("assets", "Irregular Forces")]
    },

    6: {
        1: ["An Underappreciated But Scrappy Officer Who Will Take Charge When All Seems Doomed And Save The Day, Only To Lose His Life In The Process", ("assets", "Unexpected Deliverance")],
        2: ["Broad Appreciation for Tactics", ("might", 1), ("assets", "Rules of Plunder")],
        3: ["Wide Reading of a Classical Strategic Treatise", ("might", 1)],
        4: ["Established War College", ("might", 1)],
        5: ["Peerless Tactical Secrets", ("assets", "Keen")]
    },

    7: {
        1: ["Splendid Roads to Market", ("territory", 1)],
        2: ["Nice Bit of the River Valley", ("territory", 1), ("assets", "Patriotism")],
        3: ["Pleasant Fruiting Trees", ("territory", 1)],
        4: ["We Call it 'The Grain Sea'", ("territory", 1)],
        5: ["Bounteous Harvest", ("assets", "Fortune Smiles")]
    },

    8: {
        1: ["Coast", ("territory", 1)],
        2: ["High-Quality Smithing", ("territory", 1), ("assets", "Foundries, Smiths and Armorers")],
        3: ["Tidy Bureaucracy", ("territory", 1)],
        4: ["Artistic Renaissance", ("territory", 1)],
        5: ["Oppression", ("assets", "Permanent Underclass")]
    },

    9: {
        1: ["Charismatic Elite", ("assets", "Mass Appeal")],
        2: ["Expectation of Piety", ("sovereignty", 1), ("assets", "Classic Enemy")],
        3: ["Culture of Worship", ("sovereignty", 1)],
        4: ["Church Acknowledges the Crown", ("sovereignty", 1)],
        5: ["High Holy Days", ("assets", "Predictable Bounty")]
    },

    10: {
        1: ["Culture of Inquisitiveness", ("assets", "Small Horizon")],
        2: ["Recent Happiness", ("assets", "Payoff")],
        3: ["Just Courts", ("sovereignty", 1)],
        4: ["Justified Pride", ("assets", "Epic History")],
        5: ["Culture of Obedience", ("sovereignty", 1)]
    }
}


# TODO: Build better, more consistent corpus.
class Corpus:
    def __init__(self):
        self.nouns = self.loadwordfile("./nouns.txt")
        self.adjectives = self.loadwordfile("adjectives.txt")

    @property
    def noun(self):
        return choice(self.nouns)

    @property
    def adjective(self):
        return choice(self.adjectives)

    @staticmethod
    def loadwordfile(filename):
        words = []
        try:
            with open(filename, "r") as f:
                for line in f:
                    words.append(line.split()[0])
        except FileNotFoundError:
            pass
        return words

    def randomname(self):

        return "The {} {}".format(self.adjective, self.noun.capitalize())

    def tracery_name(self):
        rules = {"origin": "The #adjective# #noun#"}

        rules["adjective"] = self.adjectives
        rules["noun"] = self.nouns

        grammar = tracery.Grammar(rules)

        return grammar.flatten("#origin#")


# TODO: Build API for doing company actions.
class Company:
    """
    Representation of Reign companies.
    """
    _stats = ["influence", "might", "sovereignty", "territory", "treasure"]

    def __init__(self, name="Some Company", stats=(0, 0, 1, 0, 0), assets=None):
        """

        :param name: The name of the company as String.
        :param stats: Tuple of the companies stats in alphabetical order.
        :param assets: List of company assets as strings.
        """
        self.name = name

        self.influence = stats[0]
        self.might = stats[1]
        self.sovereignty = stats[2]
        self.territory = stats[3]
        self.treasure = stats[4]

        if not assets:
            assets = []
        self.assets = list(assets)

        self.used = Counter()

        self.roll = None

    @property
    def size(self):
        """
        The companies 'size' as a measure of stats + # of assets.
        :return: int
        """
        _size = sum([getattr(self, x) for x in self._stats])
        _size += len(self.assets)

        return _size

    @property
    def stats(self):
        """
        Return companies stats as a {statname: value} dict.

        :return: dict
        """
        return {stat:getattr(self, stat) for stat in Company._stats}

    @property
    def stats_tuple(self):
        """
        Return a tuple of the values of the companies stats.

        :return: 5-Tuple of stat values
        """
        return tuple([getattr(self, stat) for stat in Company._stats])

    def refresh(self):
        """Clear stat usage Counter """
        self.used.clear()

    def do(self, stat1, stat2):
        """
        Roll for Company action.

            >>> company = Company(stats=(2,2,2,2,2))
            >>> roll = company.do("might", "treasure")     # roll for attack
            >>> len(roll)
            4

        :param stat1: Stat name as String.
        :param stat2: Stat name as String.
        :return: Roll
        """

        _value1 = getattr(self, stat1) - self.used[stat1]
        _value2 = getattr(self, stat2) - self.used[stat2]

        self.used[stat1] += 1
        self.used[stat2] += 1

        return Roll(_value1 + _value2)

    def __repr__(self):
        return "Company(name={p.name}, stats={p.stats_tuple}, assets={p.assets}".format(p=self)

    def __str__(self):
        stringrep = """\
                    {c.name}:

                    Influence: {c.influence}
                    Might: {c.might}
                    Sovereignty: {c.sovereignty}
                    Territory: {c.territory}
                    Treasure: {c.treasure}

                    Assets: {c.assets}"""

        return dedent(stringrep).format(c=self)


def onerollcompany(name="OneRollCompany", dice=15):
    """
    Generate a Company randomly.

    :param name: Str of the companies name.
    :param dice: Int of dice to roll for company generation.
    :return: Company object.
    """

    company = Company(name, (0, 0, 1, 0, 0))
    roll = Roll(dice, over10=True, limit_width=True)

    company.roll = roll
    results = []

    # get Match results
    for match in roll.matches:
        width = match[0]
        height = match[1]

        results.extend([_ORC_table[height][x] for x in range(2, width + 1)])

    # get Waste Die results
    results += [_ORC_table[die][1] for die in roll.waste]
    print("Processing Results")
    for res in results:
        for i in res:
            if type(i) == str:
                pass  # maybe do something useful with those strings
            else:
                if type(i[1]) == str:
                    # print(i)
                    company.assets.append(i[1])
                    # print(len(company.assets))
                else:
                    setattr(company, i[0], getattr(company, i[0]) + i[1])
    return company


if __name__ == "__main__":
    foo = Corpus()
    print(foo.tracery_name())
    pass
