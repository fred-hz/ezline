
class Performance(object):
    def __init__(self, sim_params, trading_calendar):
        self.sim_params = sim_params
        self.trading_calendar = trading_calendar

        self.period_start = sim_params.period_start
        self.period_end = sim_params.period_end
        self.capital_base = sim_params.capital_base

