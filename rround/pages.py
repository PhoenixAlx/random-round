from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random
from .generating_round import one_more_round


class MyPage(Page):
    form_model = 'player'
    form_fields = ['smth']


class Results(Page):
    def before_next_page(self):
        if random.random() < Constants.prob_to_continue:
            one_more_round(self, page_sequence)


page_sequence = [
    MyPage,
    Results
]
