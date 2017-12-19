# Необходимо реализовать классы животных на ферме:
# 	• Коровы, козы, овцы, свиньи;
# 	• Утки, куры, гуси.
# Условия:
# 	1. Должен быть один базовый класс, который наследуют все остальные животные.
# 	2. Базовый класс должен определять общие характеристики и интерфейс.

from datetime import date


class HomeAnimal:

    weight = 0  # вес
    height = 0  # рост
    sex = ('male', 'female')  # пол
    breed = None  # порода
    birthday = None  # дата рождения
    placement = None  # место ночевки на ферме
    eating_schedule = None  # график кормления
    color = None  # окрас

    def __init__(self, sex, birthday, weight):
        self.sex = sex
        self.birthday = birthday
        self.weight = weight

    def get_age(self): pass  # получить возраст животного

    def feed(self, food):  # кормить
        self.weight += food * 0.3

    def start_walking(self): pass  # отправить на выгул

    def stop_walking(self): pass  # завершить выгул

    def stab(self): pass  # забить (убить)


class HomeBird(HomeAnimal):

    egg_count = 0  # кол-во яиц в день
    eggs = 0  # всего собрано яиц
    nickname = ''  # кличка

    def collect_egg(self, num):
        self.eggs += num

    def __init__(self, nickname):
        self.nickname = nickname


class HomeAnimalWithMilk(HomeAnimal):

    milk_per_day = 0  # удойность л/день
    nickname = ''  # кличка
    mil_fat_content = 0  # жирность молока

    def do_milk(self): pass  # доить

    def __init__(self, nickname, sex, birthday, weight):
        super().__init__(sex, birthday, weight)
        self.nickname = nickname


class Cow(HomeAnimalWithMilk): pass  # Корова


class Goat(HomeAnimal): pass  # Коза


class Sheep(HomeAnimal):  # Овца

    shear_count = 0  # скольро раз стричь в год
    shear_weight = 0  # кг шерсти с одного подстрига

    def shear(self): pass  # стричь


class Pig(HomeAnimal):  # Свинья

    nickname = ''  # кличка
    child_count = 0  # кол-во приплода

    def __init__(self, nickname, sex, birthday, weight):
        super().__init__(sex, birthday, weight)
        self.nickname = nickname

    def child_bith(self, count):
        self.child_count += count


class Duck(HomeBird): pass  # Утка


class Chicken(HomeBird): pass  # Курица


class Goose(HomeBird): pass  # Гусь


# Несколько экземпляром класса Утка

duck1 = Duck('Donald')
duck2 = Duck('Martin')

print(duck1.nickname)
print(duck2.nickname)

# Корова

cow1 = Cow('Варя', 'female', date.today(), 20)
print('Вес коровы при рождении: {}'.format(cow1.weight))

cow1.feed(100)
print('Вес коровы после кормления: {}'.format(cow1.weight))

# Свинья

pig1 = Pig('Маня', 'female', date.today(), 30)
pig1.child_bith(10)
print('Свинья "{}" за свою жизнь родила {} поросят'.format(pig1.nickname, '%d' % pig1.child_count))
