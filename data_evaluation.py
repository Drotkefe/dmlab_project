import pandas as pd
import sqlite3
import seaborn as sns
import matplotlib.pyplot as plt
import plotly
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go



def load_data_into_df(db_name: str) -> pd.DataFrame:
    connection=sqlite3.connect(db_name)
    cursor=connection.cursor()
    cursor.execute('SELECT * FROM cars')
    df=pd.DataFrame(cursor.fetchall(),columns=['Brand', 'Model','Fuel type','Year','Horse power','Mileage','Transmission','Price','Hash'])
    return df

# fuel type distribution
# best selling brand in europe
# best selling model for the first brand
# best selling modell statistics (Price, mileage, fuel, transmission)
# count of selling cars by age
# count of selling cars by mileage
# What is the average milage for each brand as the year changes
# Median price change by age of vehicle
    
def fuel_type_distribution(df):
    names=df['Fuel type'].unique()
    counts=[]
    for n in names:
        count=df[df['Fuel type'] == n].shape[0]
        counts.append(count)
    fig=make_subplots(1,1,specs=[[{"type":"domain"}]])
    fig.add_trace(go.Pie(labels=names,values=counts,title="Üzemanyag típusok eloszlása"))
    plotly.offline.plot(fig,filename="fuel_distribution.html")
    fig.write_image("fuel_distribution.png")
    
    
    


if __name__ == "__main__":
    df=load_data_into_df("cars_data.db")
    df=df.drop('Hash',axis=1)
    fuel_type_distribution(df)
    print(df)
    print(df.describe())