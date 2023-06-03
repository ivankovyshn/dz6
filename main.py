import logging
import random

logging.basicConfig(filename='simulation.log', level=logging.INFO)

class House:
    def __init__(self):
        self.mess = 0
        self.food = 0

class Auto:
    brands_of_car = {
        'BMW': {'fuel': 100, 'strength': 100, 'consumption': 6},
        'ZAZ': {'fuel': 50, 'strength': 40, 'consumption': 10},
        'Volvo': {'fuel': 70, 'strength': 150, 'consumption': 8},
        'Ferrari': {'fuel': 80, 'strength': 120, 'consumption': 14},
    }

    def __init__(self):
        self.brand = random.choice(list(Auto.brands_of_car))
        self.fuel = Auto.brands_of_car[self.brand]['fuel']
        self.strength = Auto.brands_of_car[self.brand]['strength']
        self.consumption = Auto.brands_of_car[self.brand]['consumption']

    def drive(self):
        if self.strength > 0 and self.fuel >= self.consumption:
            self.fuel -= self.consumption
            self.strength -= 1
            return True
        else:
            logging.info('Car cant move')
            return False

class Job:
    job_list = {
        'Java developer': {'salary': 50, 'sadness': 10},
        'Python developer': {'salary': 40, 'sadness': 3},
        'C++ developer': {'salary': 45, 'sadness': 25},
        'Rust developer': {'salary': 70, 'sadness': 1},
    }

    def __init__(self):
        self.job_title = random.choice(list(Job.job_list))
        self.salary = Job.job_list[self.job_title]['salary']
        self.sadness = Job.job_list[self.job_title]['sadness']

class Human:
    def __init__(self, name='Human', job=None, home=None, car=None):
        self.name = name
        self.money = 100
        self.happiness = 50
        self.satiety = 50
        self.job = job
        self.car = car
        self.home = home

    def get_home(self):
        self.home = House()

    def get_car(self):
        self.car = Auto()

    def get_job(self):
        if self.car.drive():
            self.job = Job()
        else:
            self.to_repair()

    def to_repair(self):
        self.car.strength += 100
        self.money -= 50

    def eat(self):
        if self.home.food <= 0:
            self.shopping('food')
        else:
            if self.satiety >= 100:
                self.satiety = 100
            else:
                self.satiety += 5
                self.home.food -= 5

    def shopping(self, goal):
        if self.car.drive():
            pass
        else:
            if self.car.fuel < 20:
                goal = 'fuel'
            else:
                self.to_repair()
                return
        if goal == 'fuel':
            logging.info('I bought fuel')
            self.money -= 100
            self.car.fuel += 100
        elif goal == 'food':
            logging.info('I bought food')
            self.money -= 50
            self.home.food += 50
        elif goal == 'sweets':
            logging.info('I bought sweets')
            self.money -= 15
            self.satiety += 2
            self.happiness += 10

    def work(self):
        if self.car.drive():
            pass
        else:
            if self.car.fuel < 20:
                self.shopping('fuel')
                return
            else:
                self.to_repair()
                return
        self.money += self.job.salary
        self.happiness -= self.job.sadness
        self.satiety -= 4

    def chill(self):
        self.happiness += 10
        self.home.mess += 5

    def clean_home(self):
        self.happiness -= 5
        self.home.mess = 0

    def status(self, day):
        day_str = f'Today is the {day} day of {self.name}\'s life'
        logging.info(f'{day_str:=^50}')
        human_info = f'{self.name}\'s info'
        logging.info(f'{human_info:^50}')
        logging.info(f'money: {self.money}')
        logging.info(f'satiety: {self.satiety}')
        logging.info(f'happiness: {self.happiness}')
        home_info = 'Home info'
        logging.info(f'{home_info:^50}')
        logging.info(f'food: {self.home.food}')
        logging.info(f'mess: {self.home.mess}')
        car_info = f'{self.car.brand}\'s info'
        logging.info(f'{car_info:^50}')
        logging.info(f'fuel: {self.car.fuel}')
        logging.info(f'strength: {self.car.strength}')

    def is_alive(self):
        if self.happiness < 0:
            logging.info('Depression...')
            return False
        if self.satiety < 0:
            logging.info('Dead...')
            return False
        if self.money < -500:
            logging.info('Bankrupt...')
            return False
        else:
            return True

    def live_a_day(self, day):
        if not self.is_alive():
            return False
        if self.home is None:
            logging.info('Settled in the house')
            self.get_home()
        if self.car is None:
            self.get_car()
            logging.info(f'I bought a car: {self.car.brand}')
        if self.job is None:
            self.get_job()
            logging.info(f'I am going to get a job {self.job.job_title} with salary {self.job.salary}')
        self.status(day)
        dice = random.randint(1,4)
        if self.satiety < 20:
            logging.info('Ill go to eat')
            self.eat()
        elif self.happiness < 20:
            if self.home.mess > 15:
                self.clean_home()
            else:
                self.chill()
        elif self.money < 0:
            logging.info('Start working!')
            self.work()
        elif self.car.strength < 15:
            logging.info('Gonna repair my car')
            self.to_repair()
        elif dice == 1:
            logging.info('Lets chill!')
            self.chill()
        elif dice == 2:
            logging.info('Start working!')
            self.work()
        elif dice == 3:
            logging.info('Cleaning time!')
            self.clean_home()
        elif dice == 4:
            logging.info('Time for sweets')
            self.shopping('sweets')
        return True

nick = Human(name='Nick')

for day in range(1, 8):
    if not nick.live_a_day(day):
        break