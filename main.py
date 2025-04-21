from __future__ import annotations
from enum import Enum
import asyncio
import random
import threading

max_hp = 100
max_energy = 100
max_food = 100

food_takes = 1
energy_recieved = 3

time_tick = 1
takes_time = 1
time = 43200

class Player:
    def __init__(self, name: str):
        self.name = name
        self.__hp = max_hp
        self.__energy = max_energy
        self.__food = max_food
        self.__inventory = Inventory()
        self.death = False

    def rest(self):
        if self.__food > 0 and self.__food - food_takes >= 0:
            self.__food -= food_takes
            self.__energy += energy_recieved
            if self.__energy > max_energy:
                self.__energy = max_energy
            print("You rested and regained energy.")
        else:
            print("Not enough food to rest.")

    def eat(self):
        if self.__inventory.resources:
            food = self.__inventory.resources[0]
            food_earning = food.food_earning
            self.hp += food_earning.hp
            self.food += food_earning.food
            self.__inventory.remove(food)
            print("You ate some food.")
        else:
            print("You have no food to eat.")

    def move(self):
        self.energy -= 5
        self.food -= 3
        self.hp -= 2
        print("You moved to a new location.")

    def risk(self):
        event(self)

    @property
    def inventory(self):
        return self.__inventory

    @property
    def hp(self):
        return self.__hp

    @hp.setter
    def hp(self, value):
        if value >= 0 and value <= max_hp and not self.death:
            self.__hp = value
            if self.__hp <= 0:
                self.death = True
                print("You have died.")

    @property
    def energy(self):
        return self.__energy

    @energy.setter
    def energy(self, value):
        if value >= 0 and value <= max_energy and not self.death:
            self.__energy = value

    @property
    def food(self):
        return self.__food

    @food.setter
    def food(self, value):
        if value >= 0 and value <= max_food and not self.death:
            self.__food = value

class Inventory:
    def __init__(self):
        self.resources: list[Food] = []

    def add(self, resource: Food):
        if isinstance(resource, Food):
            self.resources.append(resource)

    def remove(self, resource: Food):
        if isinstance(resource, Food):
            self.resources.remove(resource)

    def find_resource(self, resource: Food):
        return resource in self.resources

class Resource:
    def __init__(self, name):
        self.name = name

class Food:
    def __init__(self, food_points, weight, hp_points, expose_time):
        self.__food_points = food_points
        self.weight = weight
        self.__expose_time = expose_time
        self.eated = False
        self._hp_points = hp_points

    def expose(self):
        self.__expose_time -= takes_time

    @property
    def food_points(self):
        points = self.__food_points
        if self.__expose_time < 0:
            points = round(points - ((-self.__expose_time) / 3))
        return max(0, points)

    @property
    def hp_points(self):
        if self.__expose_time < 0:
            return round(((-self.__expose_time) / 4) * -1)
        return self._hp_points

    @property
    def food_earning(self):
        return FoodEarning(self.food_points, self.hp_points)

    @property
    def expose_time(self):
        return self.__expose_time

class FoodEarning:
    def __init__(self, food, hp):
        self.food = food
        self.hp = hp

class Night:
    def __init__(self):
        self.is_running = False
        self.funcs = []
        self.current_time = 0

    def start(self):
        self.is_running = True
        asyncio.run(self.__tick_start())

    async def __tick_start(self):
        while self.is_running:
            self.current_time += takes_time
            for func in self.funcs:
                func()
            await asyncio.sleep(time_tick)

class Game:
    players = []
    night = Night()
    client_player = Player("john")
    current_time = time

    @classmethod
    def initialize(cls):
        cls.players.append(cls.client_player)
        cls.night.funcs.append(lambda: cls.tick())

    @classmethod
    def tick(cls):
        cls.current_time -= takes_time
        for player in cls.players:
            for resource in player.inventory.resources:
                resource.expose()
        if cls.current_time <= 0:
            cls.night.is_running = False
            print("Night is over. Game ended.")


def event(player: Player):
    rnd = random.randint(1, 5)
    if rnd == 1:
        player.hp -= 10
        print("You were attacked and lost health.")
    elif rnd == 2:
        player.food += 5
        print("You found some food.")
    elif rnd == 3:
        player.energy += 10
        print("You found a place to rest and gained energy.")
    elif rnd == 4:
        player.hp += 5
        print("You found a medkit and healed a bit.")
    elif rnd == 5:
        player.hp -= 5
        player.food -= 2
        player.energy -= 3
        print("Something bad happened. You lost some resources.")

def print_status(player):
    print(f"HP: {player.hp}, Energy: {player.energy}, Food: {player.food}, Inventory: {len(player.inventory.resources)} items")


def background_loop():
    Game.night.start()

def main():
    Game.initialize()
    player = Game.client_player


    thread = threading.Thread(target=background_loop, daemon=True)
    thread.start()

    while not player.death and Game.current_time > 0:
        print("\nChoose action: [rest, eat, move, risk, find, status, time, quit]")
        cmd = input("Action: ").strip().lower()

        if cmd == "rest":
            player.rest()
        elif cmd == "eat":
            player.eat()
        elif cmd == "move":
            player.move()
        elif cmd == "risk":
            player.risk()
        elif cmd == "find":
            food = Food(10, 1, 5, 10)
            player.inventory.add(food)
            print("You found some food.")
        elif cmd == "status":
            print_status(player)
        elif cmd == "time":
            print(f"Time left until morning: {Game.current_time} ticks")
        elif cmd == "quit":
            print("Game exited.")
            break

if __name__ == "__main__":
    main()
