from enum import Enum
import asyncio

max_hp = 100
max_enery = 100
max_food = 100

food_takes = 1
energy_recieved = 3

time_tick = 1
takes_time = 1
time = 43200

class Player(object):
    def __init__(self, name: str):
        self.name = name
        self.__hp: int = max_hp 
        self.__energy: int = max_enery
        self.__food: int = max_food
        self.__inventory = Inventory()
        self.death: bool = False

    def rest(self):
        if self.__food > 0 and self._food - food_takes >= 0: 
            self.__food = self.__food - food_takes
            self.__energy = self.__energy + energy_recieved

    def eat(food: Food):
        if self.__inventory.find_resource(food):
            food_earning: FoodEarning = food.food_earning
            self.hp = self.hp + food_earning.hp
            self.food = self.food + food_earning.food
            self.__inventory.remove(food)

    @property
    def inventory(self):
        return self.__inventory

    @property
    def hp(self) -> int:
        return self.__hp

    @hp.setter
    def hp(self, value) -> None:
        if value >= 0 and value <= max_hp and self.death != True:
            self.__hp = value
            if self.__hp == 0:
                self.death = True

    @property
    def energy(self) -> int:
        return self.__energy

    @energy.setter
    def energy(self, value) -> None:
        if value >= 0 and value <= max_energy and self.death != True:
            self.__energy = value

    @property
    def food(self) -> int:
        return self.__food
    
    @food.setter
    def food(self, value) -> None:
        if value >= 0 and value <= max_food and self.death != True:
            self.__food = value

        
class Inventory(object):
    def __init__(self):
        self.resources: list[Food] = []

    def add(resource: Food):
        if isinstance(resource, Food):
            self.resources.append(resource)

    def remove(resource: Food):
        if isinstance(resource, Food):
            self.resources.remove(resource)
        elif isinstance(resource, int):
            self.resources = self.resources.pop(resource)
        

class Resource(object):
    def __init__(self, name):
        self.name = name

class Food(object):
    def __init__(self, food_points, weight, hp_points, expose_time):
        self.__food_points = food_points
        self.weight = weight
        self.__expose_time = expose_time
        self.eated: bool = False
        self.hp_points = hp_points

    def expose(self):
        self.__expose_time = self.__expose_time - takes_time
        
    @property
    def food_points(self):
        points = self.__food_points
        if self.__expose_time < 0:
            points = round(points - ((self.__expose_time * -1) / 3))
        return points

    @property
    def hp_points(self):
        if self.__expose_time < 0:
            return round(((self.__expose_time * -1) / 4) * -1)

    @property
    def food_earning(self):
        return FoodEarning(self.food_points, self.hp_points)
        

    @property
    def expose_time(self):
        return self.__expose_time

class FoodEarning(object):
    def __init__(self, food, hp):
        self.food = food
        self.hp = hp


class Night(object):
    def __init__(self):
        self.is_running = False
        self.funcs = []
        self.current_time: int = 0

    def start(self):
        self.is_running = True
        asyncio.run(self.__tick_start)

    async def __tick_start(self):
        while self.is_running:
            self.current_time += takes_time
            for func in self.funcs:
                func()
            await asyncio.sleep(time_tick)


class Game(object):
    players = []
    night = Night()
    client_player = Player("john")
    current_time = time

    @staticmethod
    def initialize():
        night.funcs.append(tick)
        while True:

    @staticmethod
    def tick():
        current_time = current_time - takes_time
        for player in players:
            for resource in player.inventory
                resource.expose()

        

    