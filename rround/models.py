from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from .utils import get_num_rounds
from rround import cp
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
    def creating_session(self):
        from .generating_round import preparing_db
        if self.round_number == 1:
            for p in self.session.get_participants():
                p.vars['final_round'] = get_num_rounds(Constants.prob_to_continue)
                cp(p.vars['final_round'])
            max_round = max([p.vars['final_round'] for p in self.session.get_participants()])
            self.session.vars['max_round'] = max_round
            preparing_db(self.session)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    smth = models.IntegerField()
