import pandas as pd
import sqlite3
import seaborn as sns
import matplotlib.pyplot as plt
import plotly
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime



def load_data_into_df(db_name: str) -> pd.DataFrame:
    connection=sqlite3.connect(db_name)
    cursor=connection.cursor()
    cursor.execute('SELECT * FROM cars')
    df=pd.DataFrame(cursor.fetchall(),columns=['Brand', 'Model','Fuel type','Year','Horse power','Mileage','Transmission','Price','Hash'])
    return df

# Hány év után kerülnek fel az autók.
# What is the average milage for each brand as the year changes
# Median price change by age of vehicle

def file_exists(file_path: str):
    file=Path(file_path)
    return file.exists()

def fuel_type_distribution(df:pd.DataFrame,plot_name:str):
    if not file_exists(plot_name):
        names=df['Fuel type'].unique()
        counts=[]
        for n in names:
            count=df[df['Fuel type'] == n].shape[0]
            counts.append(count)
        fig=make_subplots(1,1,specs=[[{"type":"domain"}]])
        fig.add_trace(go.Pie(labels=names,values=counts,title="Üzemanyag típusok eloszlása"))
        plotly.offline.plot(fig,filename=plot_name,auto_open='False',auto_play='False')

def best_selling_brands(df:pd.DataFrame,plot_name:str,top_n:int):
    if not file_exists(plot_name):
        brand_counts=pd.DataFrame(df.Brand.value_counts().reset_index().values, columns=['Manufacturers','Count'])
        data=brand_counts.head(top_n)
        fig=px.bar(data,x='Manufacturers',y='Count',title="Legnépszerűbb autó gyártók")
        plotly.offline.plot(fig,filename=plot_name)

def best_selling_models(df:pd.DataFrame,plot_name:str,top_n:int):
    if not file_exists(plot_name):
        top_brand=df['Brand'].value_counts().idxmax()
        df.drop(df[df['Model']=='egyéb'].index, inplace=True)
        model_counts=pd.DataFrame(df.Model.value_counts().reset_index().values, columns=['Model','Count'])
        model_counts=model_counts.merge(df[['Model','Brand']],on='Model').drop_duplicates()
        model_counts['Color']= model_counts['Brand'].apply(lambda x: 'red' if x == top_brand else 'blue')
        data=model_counts.head(top_n)
        fig=px.bar(data,x='Model',y='Count',title=f"Legnépszerűbb modellek darabszámai kiemelve a top gyártó: {top_brand} modelleket", color='Color').update_xaxes(categoryorder='total descending')
        fig.update_layout(showlegend=False)
        plotly.offline.plot(fig,filename=plot_name)

def top_modell_statistics(df:pd.DataFrame,plot_name:str):
    def create_trace(col_name:str,subplots,row:int,col:int):
        traces=[]
        fig=px.box(df[col_name])
        for trace in range(len(fig['data'])):
            traces.append(fig["data"][trace])
        for t in traces:
            subplots.append_trace(t,row=row,col=col)

    if not file_exists(plot_name):
        top_model=df['Model'].value_counts().idxmax()
        df=df[df['Model']==top_model].iloc[:,3:]
        df['Year']=datetime.now().year-df['Year']
        df=df.describe().loc[['mean','std','min','max']]
        fig=make_subplots(rows=2,cols=2)
        create_trace('Year',fig,1,1)
        create_trace('Horse power',fig,1,2)
        create_trace('Mileage',fig,2,1)
        create_trace('Price',fig,2,2)
        fig.update_layout(title_text=f"{top_model} statisztikák")
        plotly.offline.plot(fig,filename=plot_name)
    


if __name__ == "__main__":
    df=load_data_into_df("cars_data.db")
    df=df.drop('Hash',axis=1)
    fuel_type_distribution(df,"fuel_distribution.html")
    best_selling_brands(df,"best_selling_car_brands.html",20)
    best_selling_models(df,"best_selling_models.html",30)
    top_modell_statistics(df,"top_modell_statistics.html")
    print(df)