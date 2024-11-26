# Motiváció
A problémát azért választottam, mert mindig is szerettem az autókat, és gyerekkori álmom, hogy egy régi Jaguar XJR-t (X308) vásároljak hobbi autónak. Az első gondolatom az volt, hogy az adatok elemzésével jobban megismerhetem a mai trendeket, és gyermeki kíváncsiságom ösztönzött arra, hogy megvizsgáljak némi statisztikai adatot az autópiacról. Emellett az is motivált, hogy ha egy megrendelő hasonló projektet kérne tőlem, milyen funkciókat tartana értékesnek.

Ezért kigondoltam egy lineáris regresszión alapuló megoldást, amely a bemenő paraméterek alapján meghatározza az autó aktuális piaci értékét. Az autó életkora remek prediktív képességgel bír, ezért egész jól működik az elkészült modell, de a problémát okoz, hogy az autók értéke egy idő után megáll a csökkenésben. Utólag belátom, hogy egy SVM vagy egy kisebb neurális hálózat talán bölcsebb megoldás lett volna.

A projektben SQL adatbázist használtam, mivel ebben van a legtöbb tapasztalatom, és az adat struktúrájának teljesen megfelel. Az adatfeldolgozáshoz pandas-t használtam, a vizualizációhoz pedig plotly-t, mert interaktívabb diagramokat tudok vele készíteni, mint a matplotlib könyvtárral. A frontend részhez egy egyszerű webes felületet valósítottam meg amihez Flask-ot használtam. Sokat hallottam róla, hogy mennyivel egyszerűbb, mint a Django, amit eddig személyes projektjeimhez használtam, és az újdonság varázsa plusz a rendelkezésre álló időkeret befolyásolta a döntésem.
# Used car market analysis

## Introduction
This project is designed to scrape data from AutoScout24 and store the records in an SQL database. 
Additionally, it generates interactive charts to visualize insights and includes a Price Calculator based on Linear Regression to help you understand how your car's value compares to the current market  
meanwhile providing a Front-End application created in Flask.

## Table of Contents
- Introduction
- Setup
- Usage
- Contact

## Setup
### Prerequisites

The project was written in Python 3.9.13

```bash
# Clone the Project Repository
git clone https://github.com/Drotkefe/dmlab_project.git
```
Navigate to the Project Directory and
Create a new [virtual environment](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)
```bash
# create virtual env
python -m venv <virtual-environment-name>
```
Install Dependencies:

```bash
# install packages
pip install -r requirements.txt
```

## Usage
### To run the program
Make sure you activated your virtual environment and you are using the right python.exe for running the program  
By cloning the repository you will already have the scraped data.
```bash
# You should be able to run your project by:
# The specific command may depend on your project's structure.
python frontend_app.py
```
If you need the most recent data from the web, please run the followings:
1. collect_data.py
2. data_evaluation.py
3. frontend_app.py

## Contact
### Feel free to contact me for additional help or info
email: patrikmeresz@gmail.com


