import bs4
import requests
import sqlite3
import pandas as pd

URL = "https://www.autoscout24.hu/lst?sort=standard&desc=0&ustate=N%2CU&atype=C&source=homepage_search-mask"

class Car:
    def __init__(self,brand,model,fuel_type,year,horse_power,milage,transmission,price):
        self.brand=brand
        self.model=model
        self.fuel_type=fuel_type
        self.year=year
        self.horse_power=horse_power
        self.milage=milage
        self.transmission=transmission
        self.price=price

    def __init__(self):
        pass

    @staticmethod
    def read_hp(s: bs4.element):
        pass

    @staticmethod
    def read_transmission(s: bs4.element):
        pass
    
    @staticmethod
    def read_fuel_type(s: bs4.element):
        pass

def init_db():
    connection = sqlite3.connect("cars_data.db")
    cursor = connection.cursor()
    cursor.execute(''' CREATE TABLE cars( 
                  BRAND TEXT NOT NULL,
                  MODEL TEXT NOT NULL,
                  FUEL_TYPE TEXT NOT NULL,
                  YEAR INT NOT NULL,
                  HORSE_POWER INT NOT NULL,
                  MILAGE INT NOT NULL,
                  TRANSMISSION TEXT NOT NULL,
                  PRICE INT NOT NULL);
              ''')
    return cursor

def get_cars():
    cars=[]
    result = requests.get(URL)
    soup = bs4.BeautifulSoup(result.text,"html.parser")
    pages=1
    while len(cars)<2000:
        for row in soup.find_all('article'):
            new_car=Car()
            new_car.brand=row['data-make']
            new_car.model=row['data-model']
            new_car.fuel_type=row.find('span', {'data-testid' : 'VehicleDetails-gas_pump'}).text
            new_car.year=row['data-first-registration'][-4:]
            new_car.horse_power=new_car.read_hp("alma")
            new_car.milage=row['data-milage']
            new_car.transmission=row['']
            new_car.price=row['data-price']
            cars.append(new_car)
            print(row['data-price'])
            print(row['data-make'])
        pages+=1
        result= requests.get(f"https://www.autoscout24.hu/lst?atype=C&desc=0&page={pages}&search_id=yui93b7btz&sort=standard&source=listpage_pagination&ustate=N%2CU")

    

if __name__ == "__main__":
    # db=init_db()
    get_cars()