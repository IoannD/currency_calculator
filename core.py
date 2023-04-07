import datetime as dt
from forex_python.converter import CurrencyRates
import functools


class Record():
    def __init__(self, date, amount, category, comment) -> None:
        self.date = date
        self.amount = amount
        self.category = category 
        self.comment = comment


class Calculator():
    def __init__(self, limit) -> None:
        self.currency_converter = CurrencyRates()
        self.limit = limit
        self.records = []
    
    def currency_rate_exchange(self, currency):
        try: 
           ans =  self.currency_converter.get_rate(currency, 'RUB')
        # except RatesNotAvailableError: 
        except :
            rates = {
                'RUB': 1, 
                'USD': 75, 
                'EURO': 85, 
            }
            ans = rates[currency]

        return ans

    def print_record(self):
        def print_i_record(i):
            print(f'# {i} date: {self.records[i].date}'
                  f' amount: {self.records[i].amount}'
                  f' category: {self.records[i].category}'
                  f' comment: {self.records[i].comment}')
    
        if 0 < len(self.records) < 5:
            for num in range(len(self.records)-1, -1, -1):
                print_i_record(num)
        else:
            for num in range(len(self.records) - 1, len(self.records) - 5, -1):
                print_i_record(num)


    def add_record(self, record):
        self.records.append(record)

    def __sum_spends_on_date(self, spends, record, date):
        if record.date == date:
            spends += record.amount
        return spends 
    
    def get_today_stats(self):
        today = dt.date.today()

        # solution No. 1 
        # spends = 0 
        # for item in self.records:
        #     if today == item.date:
        #         spends += item.amount

        # solution No. 2
        # spends = functools.reduce(lambda spends, item: spends + item.amount if item.date == today else spends, self.records, spends)
        
        # solution No. 3 
        # def my_func(spends, item):
        #     if item.date == today:
        #         spends += item.amount
        #     return spends
        # spends = functools.reduce(my_func, self.records, 0)

        # solution No. 4
        spends = functools.reduce(lambda spends, item: self.__sum_spends_on_date(spends, item, today), self.records, 0) 
        return spends

    def get_today_cash_remained(self, currency):
        spends = self.get_today_stats()

        post_fix = {
            'RUB': 'руб', 
            'USD': 'USD', 
            'EURO': 'Euro',
        }

        if spends == self.limit:
            text = 'Денег нет, держись'
        else: 

            if spends < self.limit:
                remain = (self.limit - spends) / self.currency_rate_exchange(currency)
                text = f'На сегодня осталось {remain:.2f} '

            elif spends > self.limit: 
                exceeding = (spends - self.limit) / self.currency_rate_exchange(currency)
                text = f'Денег нет, держись: твой долг - {exceeding:.2f} '

            text = text + post_fix[currency]


    def get_week_stats():
        pass



if __name__ == '__main__':


    r1 = Record(dt.date(2023, 3, 12), amount=350, category='Food', comment='for a week')
    r2 = Record(dt.date(2023, 3, 19), amount=65, category='Eating out', comment='coffee to go')
    r3 = Record(dt.date(2023, 4, 7), amount=550, category='Book', comment='')
    r4 = Record(dt.date(2023, 4, 7), amount=100, category='Book', comment='')

    cash_calculator = Calculator(1000)

    cash_calculator.add_record(r1)
    cash_calculator.add_record(r2)
    cash_calculator.add_record(r3)
    cash_calculator.add_record(r4)

    cash_calculator.print_record()

    print(cash_calculator.currency_rate_exchange('RUB'))

    print(cash_calculator.get_today_stats())
    print(cash_calculator.get_today_cash_remained('RUB'))

    print(cash_calculator.get_today_cash_remained('USD'))

    print(cash_calculator.get_today_cash_remained('EURO'))

    # print(cash_calculator.sum_spends_on_date(spends=0, record=r3, date=dt.date.today()))
