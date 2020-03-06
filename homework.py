import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        # Записываем все поступившие объекты в records
        self.records.append(record)

    def get_today_stats(self):
        amount_list = []

        # Записываем в список все поступившие значения record.amount за сегодня
        for record in self.records:
            # Записываем в список, если дата соответствует
            if record.date == dt.date.today():
                amount_list.append(record.amount)
        
        # Суммируем значения в списке
        sum_amount = sum(amount_list)

        return sum_amount

    def get_week_stats(self):
        amount_list_week = []
        # Находим дату начала диапазона
        day_delta = dt.timedelta(days=7)
        date_start = dt.date.today() - day_delta

        # Отбираем данные за неделю
        for record in self.records:
            if date_start <= record.date <= dt.date.today():
                amount_list_week.append(record.amount)
        
        # Находим их сумму
        sum_amount = sum(amount_list_week)

        return sum_amount


class Record:
    # Получаем текущую дату
    today = dt.date.today()
    
    # Если тип данных аргумента date - str, меняем на date
    def __init__(self, amount, comment, date=today):
        if isinstance(date, str):
            date = dt.datetime.strptime(date, '%d.%m.%Y').date()

        self.amount = amount
        self.date = date
        self.comment = comment


class CashCalculator(Calculator):
    USD_RATE = 60.0
    EURO_RATE = 70.0

    def exchange_rate(self, currency='rub'):
        # Курсы валют
        exchange_rate = {
            'rub': [1, 'руб'],
            'usd': [CashCalculator.USD_RATE, 'USD'],
            'eur': [CashCalculator.EURO_RATE, 'Euro'],
        }

        # Выбор курса валюты
        if currency in exchange_rate:
            result = exchange_rate[currency]

        return result

    def amount_of_money_rate_format(self, amount_of_money_rate):
        # Если остаток по курсу валюты дробный, оставляем 2 знака после запятой
        if isinstance(amount_of_money_rate, float):
            amount_of_money_rate = float('{:.2f}'.format(amount_of_money_rate))

        return amount_of_money_rate

    def get_today_cash_remained(self, currency):
        # Определение курса валют
        rate_list = self.exchange_rate(currency)
        currency_rate = rate_list[0]
        chosen_currency = rate_list[1]

        # Определение суммы потраченных денег
        sum_amount = self.get_today_stats()

        # Определение остатка денег
        sum_money = self.limit - sum_amount

        # Определение остатка денег в выбранной валюте
        amount_of_money_rate = sum_money / currency_rate

        # Если остаток по курсу валюты дробный, оставляем 2 знака после запятой
        amount_of_money_rate = self.amount_of_money_rate_format(amount_of_money_rate)

        # Возврат результата
        if sum_money == 0:
            return 'Денег нет, держись'
        elif sum_money < 0:
            return f'Денег нет, держись: твой долг - {abs(amount_of_money_rate)} {chosen_currency}'
        elif sum_money > 0:
            return f'На сегодня осталось {amount_of_money_rate} {chosen_currency}'

    def get_week_stats(self, currency='rub'):
        # Получаем сумму потраченных денег за неделю
        sum_amount = Calculator.get_week_stats(self)

        # Определение курса валют
        rate_list = self.exchange_rate(currency)
        currency_rate = rate_list[0]
        chosen_currency = rate_list[1]
        
        # Определяем сумму потраченных денег в выбранной валюте
        amount_of_money_rate = sum_amount / currency_rate

        # Если остаток по курсу валюты дробный, оставляем 2 знака после запятой
        amount_of_money_rate = self.amount_of_money_rate_format(amount_of_money_rate)

        return f'За последнюю неделю потрачено {amount_of_money_rate} {chosen_currency}'


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        # Определение съеденных калорий
        sum_amount = self.get_today_stats()

        # Определение доступного остатка каллорий
        sum_calories = self.limit - sum_amount

        # Вывод результата
        if sum_calories == 0 or sum_calories < 0:
            return 'Хватит есть!'
        elif sum_calories > 0:
            return f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {sum_calories} кКал'

    def get_week_stats(self):
        # Получаем сумму съеденных калорий за неделю
        sum_amount = Calculator.get_week_stats(self)

        return f'За последнюю неделю съедено {sum_amount} кКал'


cash_calculator = CashCalculator(1000)
calories_calculator = CaloriesCalculator(1000)

cash_calculator.add_record(
    Record(amount=1045, comment="кофе"))
cash_calculator.add_record(
    Record(amount=300, comment="Серёге за обед"))
cash_calculator.add_record(
    Record(amount=3000, comment="бар в Танин др", date="08.11.2019"))

print(cash_calculator.get_today_cash_remained("usd"))
print(cash_calculator.get_week_stats("usd"))

calories_calculator.add_record(
    Record(amount=1186, comment="Кусок тортика. И ещё один."))
calories_calculator.add_record(
    Record(amount=84, comment="Йогурт.", date="2.03.2020"))
calories_calculator.add_record(
    Record(amount=1140, comment="Баночка чипсов.", date="10.02.2020"))

print(calories_calculator.get_calories_remained())
print(calories_calculator.get_week_stats())
