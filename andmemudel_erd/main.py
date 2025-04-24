from __future__ import annotations
from enum import StrEnum, verify, UNIQUE
import time

start_balance = 1000
currency_symbol = "$"
last_id = 0

@verify(UNIQUE)
class ProductCategory(StrEnum):
    CLOTHS = "cloths"
    FOOD = "food"

@verify(UNIQUE)
class PaymentStatus(StrEnum):
    CONFIRMED = "confirmed"
    IN_PROCESS = "in_process"
    FAILED = "failed"

class Client(object):
    def __init__(self, name:str, balance: float):
        self.name = name
        self.__balance = balance
        self.__orders = []

    @property
    def orders(self):
        return self.__orders
    
    def order_append(self, order: Order):
        if isinstance(order, Order):
            self.__orders.append(order)
        else:
            raise TypeError("order should be type of Order")

    @property
    def balance(self):
        return self.__balance

    def __add__(self, value):
        if isinstance(value, float) | isinstance(value, int):
            self.__balance += value
        return self

class Order(object):
    def __init__(self):
        self.__products: list[Product] = []
    
    @property
    def products(self):
        return self.__products.copy()
    
    @property
    def final_price(self):
        sum = 0
        for product in self.__products:
            sum += product.price
        return sum

    def pay(self) -> Payment:
        payment = Payment(time.time(), self.final_price, PaymentStatus.IN_PROCESS)
        return payment
    
    def append(self, product: Product):
        if isinstance(product, Product):
            self.__products.append(product)
        else:
            raise TypeError("product should be instance of Product")

    def remove(self, value: Product | int):
        if isinstance(value, Product):
            if value in self.__products:
                self.__products.remove(value)
        elif isinstance(value, int):
            if len(self.__products) >= value and value >= 0:
                del self.__products[value]
    

class Product(object):
    __last_identity = 0
    
    def __init__(self, name: str, price: float, categories: list[ProductCategory]):
        self.__identity = Product.get_identity()
        if isinstance(name, str):
            self.name = name
        else:
            raise TypeError("name of product should be string")
        if isinstance(price, float):
            self.price = price
        else:
            raise TypeError("price of product should be float")
        if isinstance(categories, list):
            self.__categories = filter(lambda x: isinstance(x, ProductCategory), categories)

    @property
    def id(self):
        return self.__identity

    @property
    def category(self):
        return self.__category.clone()

    @property
    def category(self, value):
        if isinstance(value, list):
            self.__categories = filter(lambda x: isinstance(x, ProductCategory), value)

    def category_append(self, category: ProductCategory):
        if isinstance(category, ProductCategory):
            self.__categories.append(category)
    
    def category_remove(self, value: ProductCategory | int):
        if isinstance(value, ProductCategory) and value in self.__categories:
            self.__categories.remove(value)
        elif isinstance(value, int):
            if len(value) >= value and value >= 0:
                del self.__categories[value]
        
    @classmethod
    def get_identity(cls):
        cls.__last_identity += 1
        return cls.__last_identity

class Payment(object):
    def __init__(self, date: int, summary: float, status: PaymentStatus):
        if isinstance(status, PaymentStatus):
            self.__status = status
        else:
            raise TypeError("payment status should be type of PaymentStatus")
        if isinstance(date, int):
            self.__date = date
        else:
            raise TypeError("date of payment should be integer")
        if isinstance(summary, float):
            self.__summary = summary
        else:
            raise TypeError("summary should be float type")
    @property
    def status(self):
        return self.__status
    
    @property
    def date(self):
        return self.__date

    @property
    def summary(self):
        return self.__summary

class Warehouse(object):
    __last_identity = 0

    def __init__(self, products: list[Product]):
        self.__identity = Warehouse.get_identity()
        self.__products = filter(lambda x: isinstance(x, Product), products)
    
    @property
    def products(self):
        return self.__products.clone()

    def append(self, product: Product):
        if isinstance(product, Product):
            self.__products.append(product)
        else:
            raise TypeError("product should be type of Product")

    def get_product(self, identity) -> None | Product:
        if isinstance(identity, int):
            product = filter(lambda x: x.id == identity, self.__products)
            if len(product) == 0:
                return None
            else:
                return product[0]
        else:
            raise TypeError("identity should be instance of 'int'")

    @classmethod
    def get_identity(cls):
        cls.__last_identity += 1
        return cls.__last_identity

class Shop(object):
    def __init__(self, warehouses: list[Warehouse]):
        self.__warehouses = filter(lambda x: isinstance(x, Warehouse), warehouses)

    @property
    def warehouses(self):
        return self.__warehouses.clone()

    @property
    def all_products(self):
        products = []
        for warehouse in self.__warehouses:
            for product in warehouse.products:
                products.append(product)
        return products

    def append(self, warehouse: Warehouse):
        if isinstance(warehouse, Warehouse):
            self.__warehouses.append(warehouse)
        else:
            raise TypeError("warehouse should be type of Warehouse")

    def get_warehouse(self, identity) -> None | Warehouse:
        if isinstance(identity, int):
            warehouse = filter(lambda x: x.id == identity, self.__warehouses)
            if len(warehouse) == 0:
                return None
            else:
                return warehouse[0]


class UIService(object):
    def __init__(self):
        name = input("What's your name?")
        self.client = Client(name, start_balance)
        self.shop = Shop()

    def show_warehouse_products(self, warehouse_identity:int):
        warehouse = self.shop.warehouses[warehouse_identity]
        products = warehouse.products
        for product in products:
            print(f"{product.id}. {product.name} [{currency_symbol}{product.price}")
            print(f"Categories: {", ".join(product.categories)}")
        print("\n")
        return products

    def start(self):
        to_continue = True
        while to_continue:
            print("Welcome.")
            print("""
            1. Check the balance
            2. See all products
            3. View the order
            4. admin panel
            5. Buy order
            404. exit
            """)
            
            response = int(input("Choose the variant: "))
            match response:
                case 1:
                    print(f'Your balance: {self.client.balance}')
                    pass
                case 2:
                    print("Choose a warehouse!")
                    for warehouse in self.shop.warehouses:
                        print(f"{warehouse.id}. count of products: {len(warehouse.products)}")
                    warehouse_response = int(input("Your answer: "))
                    warehouse = self.shop.get_warehouse(warehouse_response)
                    print("\n")
                    print("List of products:")
                    self.show_warehouse_products(warehouse_response)
                    print("\n")
                    product_response = input("Do you something? ('no' = continue)\n")
                    if product_response != "no":
                        integer_response = int(product_response)
                        product = warehouse.get_product(integer_response)
                        if product != None:
                            self.client.order.append(product)
                        else:
                            print("Invalid identity")
                            
                case 3:
                    print(f"Count of products in your order: {len(self.client.order.products)}")
                    for product in self.client.order.products:
                        print(f"{product.id}. {product.name} {currency_symbol}{product.price}")
                    print(f"Summary: {self.client.order.final_price}\n")
                    
                case 4:
                    to_continue = False
                    self.admin()
                case 5:
                    pass
                case 404:
                    break
                case _:
                    print("There's no variants like this")

    def admin(self):
        to_continue = True
        while to_continue:
            print("Admin panel")
            print("""
            1. client panel
            2. add money
            3. add warehouse
            4. add product
            404. exit
            """)
            response = int(input("Choose the variant: "))
            match response:
                case 1:
                    to_continue = False
                    self.start()
                case 2:
                    hmch = int(input("How many?"))
                    self.client + hmch
                case 3:
                    warehouse = Warehouse()
                    self.shop.append(warehouse)
                case 4:
                    pass
                case _:
                    pass

def main():
    pass

if __name__ == "__main__":
    main()