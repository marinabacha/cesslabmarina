from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants, Player

import random


class Instructions(Page):
    pass


class RoleWaitPage(WaitPage):
    pass


class IdealPage(Page):
    form_model = 'player'
    form_fields = ['ideal']


class RoleNotificationPage(Page):
    pass


class ContributionPage(Page):
    form_model = 'player'
    form_fields = ['contribution']

    def is_displayed(self):
        return self.player.role == 2


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
            group = self.group
            players = group.get_players()
            contributions = [p.contribution for p in players if p.role == Constants.WEALTHY]
            group.contribution = sum(contributions)
            for player in players:
                if player.role == Constants.WEALTHY:
                    # Phase 1 Payment Calculation
                    if self.round_number == Constants.phase_one_round and self.round_number<Constants.phase_two_round:
                        subsidy = Constants.phase_one_subsidy
                        endowment = Constants.endowment
                        contribution = player.contribution
                        player.payoff = endowment +(subsidy*contribution)-contribution
                    # Phase 2 Payment Calculation
                    else:
                        subsidy = Constants.phase_two_subsidy
                        endowment = Constants.endowment
                        contribution = player.contribution
                        player.payoff = endowment - contribution + subsidy*contribution
                # Poor Player
                else:
                    if self.round_number == Constants.phase_one_round and self.round_number < Constants.phase_two_round:
                        cost = Constants.phase_one_cost
                        player.payoff = group.contribution*(1-cost)
                    else:
                        cost = Constants.phase_two_cost
                        player.payoff = group.contribution*(1-cost)


class RoundResultsPage(Page):
    pass



class Results(Page):
    def vars_for_template(self):
        if self.round_number == Constants.num_rounds:
            group = self.group
            players = group.get_players()
            random_round = random.randint(1, Constants.num_rounds)
            for player in players:
                player.pay = self.player.in_round(random_round).payoff
                print(player.pay)
            return {'final_pay': player.pay, 'random_round': random_round}
        return {}

    def is_displayed(self):
        return self.round_number == Constants.num_rounds







class ChangePage(Page):
    def is_displayed(self):
        return self.round_number == (Constants.num_rounds / 2)





class MatchingWaitPage(WaitPage):
    def after_all_players_arrive(self):
        players = self.group.get_players()
        random_p = random.randint(1, Constants.players_per_group)
        for player in players:
            print("rand id = {}, player id = {}".format(random_p, player.id_in_group))
            if random_p == player.id_in_group:
                player.role = Constants.POOR
            else:
                player.role = Constants.WEALTHY

class InstructionsPage(Page):
    def is_displayed(self):
        return self.round_number==1

page_sequence = [
    InstructionsPage,
    MatchingWaitPage,
    IdealPage,
    RoleNotificationPage,
    ContributionPage,
    ResultsWaitPage,
    RoundResultsPage,
    ChangePage,
    Results
]
