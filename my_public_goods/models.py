from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import random


author = 'Marina Lisboa Bacha'

doc = """
The Impact of Tax Deductions and Expectations on Donor’s Decisions - Code for Experiment
"""


class Constants(BaseConstants):
    name_in_url = 'my_public_goods'
    players_per_group = 4

    multiplier = 1
    num_rounds = 4

    phase_one_round = 1
    phase_two_round = num_rounds/2

    phase_one_cost = 0.20
    phase_two_cost = 0.30

    phase_one_subsidy = 0.20
    phase_two_subsidy = 0.40

    endowment = 100.00
    ideal_max = 300.00

    POOR = 1
    WEALTHY = 2



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    contribution = models.FloatField()


class Player(BasePlayer):
    role = models.IntegerField(default=0)
    ideal = models.FloatField(min=0, max=Constants.ideal_max)
    contribution = models.FloatField(min=0, max=Constants.endowment)


