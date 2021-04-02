# Привет! Я написал комментарии о том что я писал что бы было удобно и понятно.
# Извиняюсь если неправильно что-то написал :)
# Делал проект - Лёва Нетреба...


# Импортируем библиотеку для роботы с датами
import datetime as dt


# Этот класс сделан для того чтобы в классах -
# CashCalculator, CaloriesCalculator не повторялся одинаковый функционал
class Calculator:
    # Здесь свойства - лимит и список з записями которые мы будем перебирать
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    # Берём записи с классом Record и сохраняем в список
    def add_record(self, record):
        self.records.append(record)

    # Здесь подсчитываем все количество затрат или калорий,
    # которые находились в amount
    def get_today_stats(self):
        total = 0

        # Перебираем весь список
        for record in self.records:
            # Эта функция(метод) отвечает за то что бы записывать
            # все затраты сегодня, так что тут мы берём только те записи
            # которые с сегодняшней датой
            if record.date == dt.datetime.now().date():
                # И чтобы было удобно и красиво ложем в пустую переменною
                total = total + record.amount

        # И return просто возвращает все потраченное за сегодня
        return total

    # Тут все практически то же самое как в функции(методи) get_today_stats(),
    # только все количество затрат или калорий за неделю
    def get_week_stats(self):
        # Здесь охватываем период за неделю
        total = 0
        last_week = dt.date.today() - dt.timedelta(days=7)

        for record in self.records:
            if dt.date.today() >= record.date > last_week:
                total += record.amount

        return total


# Тут говорится о балансе, что осталось или наоборот
class CashCalculator(Calculator):
    # Тут курс евро и доллара взятый с - https://yandex.ru :)
    USD_RATE = 75.53
    EURO_RATE = 88.58

    CUP_DICT = {'usd': (USD_RATE, 'USD'),
                'eur': (EURO_RATE, 'Euro'),
                'rub': (1, 'руб')}

    # Сurrency это курс в котором хочет его увидеть пользователь,
    # доступные значения - 'rub', 'eur', 'usd'.
    def get_today_cash_remained(self, currency):
        result = self.limit - self.get_today_stats()
        result = result / self.CUP_DICT[currency][0]
        result = int(result * 100) / 100
        currency_name = self.CUP_DICT[currency][1]

        if currency == 'rub':
            result = int(result)

        # Если осталось что-то больше 0
        if result > 0:
            # Тут выводим остаток уже в определённом курсе и
            # currency = переменная в которою выше положили названия курса
            return f'На сегодня осталось {result} {currency_name}'

        # Если остаток равен 0
        elif result == 0:
            return 'Денег нет, держись'

        # И все остальное, то есть если ушло в минус
        else:
            return (f'Денег нет, держись: '
                    f'твой долг - {abs(result)} {currency_name}')


# Тут о том сколько нужна еще скушать или хватит есть)
class CaloriesCalculator(Calculator):
    # Тут практически все то же самое как в классе CashCalculator только
    # без всяких курсов и выводится все про калории
    def get_calories_remained(self):
        ostatok = self.limit - self.get_today_stats()

        if ostatok > 0:
            return (f'Сегодня можно съесть что-нибудь ещё, но с общей '
                    f'калорийностью не более {ostatok} кКал')

        else:
            return 'Хватит есть!'


# Тут для удобства сделан класс который распределяет по свойствам
# данные про деньги или калории
class Record:
    # Это формат в который нам нужно видеть дату
    date_format = '%d.%m.%Y'

    # Вот тут свойства, что бы потом можно было класть в них данные
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        self.comment = comment

        # Здесь говорится что нужно если в date ничего не укажут ставить
        # сегодняшнею дату
        if date == '':
            self.date = dt.datetime.now().date()

        # Тут если указана дата, приводим её к нужному формату
        else:
            self.date = dt.datetime.strptime(date, self.date_format).date()
