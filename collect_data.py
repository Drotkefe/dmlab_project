import bs4
import requests
import sqlite3
import pandas as pd
import re
import time
import random

URL = "https://www.autoscout24.hu/lst?sort=standard&desc=0&ustate=N%2CU&atype=C&source=homepage_search-mask"

class Car:
    def __init__(self,brand='',model='',fuel_type='',year=0,horse_power=0,milage=0,transmission='',price=0):
        self.brand=brand
        self.model=model
        self.fuel_type=fuel_type
        self.year=year
        self.horse_power=horse_power
        self.milage=milage
        self.transmission=transmission
        self.price=price
        self.hash=hash(self)

    @staticmethod
    def read_hp(s: str):
        try:
            hp=re.findall(r'\d+',s)[-1]
            return hp
        except:
            return 0
        
    def __eq__(self, other):
        return isinstance(other,Car) and self.brand==other.brand and self.model==other.model and self.fuel_type==self.fuel_type and self.horse_power==other.horse_power and self.milage==other.milage and self.model==other.price and self.year==other.year and self.transmission==self.transmission

    def __hash__(self):
        return hash((self.price,self.milage,self.year))

def init_db():
    try:
        with sqlite3.connect("cars_data.db") as connection:
            cursor = connection.cursor()
            cursor.execute(''' CREATE TABLE IF NOT EXISTS cars( 
                        [BRAND] TEXT NOT NULL,
                        [MODEL] TEXT NOT NULL,
                        [FUEL_TYPE] TEXT NOT NULL,
                        [YEAR] INT NOT NULL,
                        [HORSE_POWER] INT NOT NULL,
                        [MILAGE] INT NOT NULL,
                        [TRANSMISSION] TEXT NOT NULL,
                        [PRICE] INT NOT NULL,
                        [HASH] TEXT UNIQUE NOT NULL);
                ''')
            return connection
    except:
        print("Database initialization failed")

def get_cars():
    cars=[]
    result = requests.get(URL)
    soup = bs4.BeautifulSoup(result.text,'html.parser')
    number_of_cars=0
    pages=1
    while pages<21:
        for row in soup.find_all('article'):
            brand=row['data-make']
            model=row['data-model']
            fuel_type=row.find('span', {'data-testid' : 'VehicleDetails-gas_pump'}).text
            year=row['data-first-registration'][-4:]
            horse_power=Car.read_hp(row.find('span', {'data-testid' : 'VehicleDetails-speedometer'}).text)
            milage=row['data-mileage']
            transmission=row.find('span', {'data-testid' : 'VehicleDetails-transmission'}).text
            price=row['data-price']
            cars.append(Car(brand,model,fuel_type,year,horse_power,milage,transmission,price))
            number_of_cars+=1
            print('Current number of cars loaded: [%d]\r'%number_of_cars,end='')
        pages+=1
        result= requests.get(f'https://www.autoscout24.hu/lst?atype=C&desc=0&page={pages}&search_id=xb7tyfpqh2&sort=standard&source=listpage_pagination&ustate=N%2CU')
        soup = bs4.BeautifulSoup(result.text,'html.parser')
    return cars

def insert_data_to_db(data,db):
    cursor=db.cursor()
    for car in data:
        db.execute('''INSERT OR IGNORE INTO cars (brand,model,fuel_type,year,horse_power,milage,transmission,price,hash) 
                   VALUES (?,?,?,?,?,?,?,?,?)''',(car.brand,car.model,car.fuel_type,car.year,car.horse_power,car.milage,car.transmission,car.price,car.hash))
    db.commit()
    cursor.close()
    print("\nCar data saved to Database")

if __name__ == "__main__":
    db=init_db()
    cars=get_cars()
    insert_data_to_db(cars,db)
    db.close()