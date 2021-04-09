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
    RUB_RATE = 1.0
    USD_RATE = 77.22
    EURO_RATE = 91.74

    # Сurrency это курс в котором хочет его увидеть пользователь,
    # доступные значения - 'rub', 'eur', 'usd'.
    def get_today_cash_remained(self, currency):
        # Отнимаем от всего лимита потраченное за день
        ostatok = self.limit - self.get_today_stats()

        courses = {
            'rub': ('руб', self.RUB_RATE),
            'usd': ('USD', self.USD_RATE),
            'eur': ('Euro', self.EURO_RATE)
        }

        # Здесь приводи его к вибронному курсу
        result = ostatok / courses[currency][1]

        # И переделываем из такого 3,293921039 в эта 3,92 - обрезаем :)
        result = round(result, 2)

        # Если остаток равняется 0,
        # приводить его в полноценное число - 555.0 = 555
        if (result - int(result)) == 0.0:
            result = int(result)

        # Сюда ложем названия курса
        course_name = courses[currency][0]

        # Если осталось больше 0
        if result > 0:
            return f'На сегодня осталось {result} {course_name}'

        # Если превышен лимит
        elif result < 0:
            # Функция abs убирает минусы с отрицательных чисел
            return ('Денег нет, держись: '
                    f'твой долг - {abs(result)} {course_name}')

        # И если равен 0
        else:
            return 'Денег нет, держись'


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
