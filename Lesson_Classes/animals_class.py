# Необходимо реализовать классы животных на ферме:
# 	• Коровы, козы, овцы, свиньи;
# 	• Утки, куры, гуси.
# Условия:
# 	1. Должен быть один базовый класс, который наследуют все остальные животные.
# 	2. Базовый класс должен определять общие характеристики и интерфейс.


class HomeAnimal:

    weight = 0  # вес
    height = 0  # рост
    sex = ('male', 'female')  # пол
    breed = None  # порода
    birthday = None  # дата рождения
    placement = None  # место ночевки на ферме
    eating_schedule = None  # график кормления
    color = None  # окрас

    def __init__(self):
        pass

    def get_age(self):  # получить возраст животного
        pass

    def feed(self):  # кормить
        pass

    def start_walking(self):  # отправить на выгул
        pass

    def stop_walking(self):  # завершить выгул
        pass

    def stab(self):  # забить (убить)
        pass


class Cow(HomeAnimal):  # Корова

    milk_per_day = 0  # удойность л/день
    nickname = ''  # кличка
    mil_fat_content = 0  # жирность молока

    def do_milk(self):  # доить
        pass


class Goat(HomeAnimal):  # Коза

    milk_per_day = 0  # удойность л/день
    mil_fat_content = 0  # жирность молока

    def do_milk(self):  # доить
        pass


class Sheep(HomeAnimal):  # Овца

    shear_count = 0  # скольро раз стричь в год
    shear_weight = 0  # кг шерсти с одного подстрига

    def shear(self):  # стричь
        pass


class Pig(HomeAnimal):  # Свинья

    nickname = ''  # кличка
    child_count = 0  # кол-во приплода


class Duck(HomeAnimal):  # Утка

    egg_count = 0  # кол-во яиц в день

    def collect_egg(self):
        pass


class Chicken(HomeAnimal):  # Курица

    egg_count = 0  # кол-во яиц в день

    def collect_egg(self):
        pass


class Goose(HomeAnimal):  # Гусь

    egg_count = 0  # кол-во яиц в день

    def collect_egg(self):
        pass
