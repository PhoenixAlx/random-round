from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Philipp Chapkovski'

doc = """
Chance to continue to the next round with a certain probability 
"""


class Constants(BaseConstants):
    name_in_url = 'rround'
    players_per_group = None
    num_rounds = 1
    prob_to_continue = .8

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    smth = models.IntegerField()
