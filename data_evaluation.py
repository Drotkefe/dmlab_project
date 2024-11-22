import pandas as pd
import sqlite3
import numpy as np
import os
import plotly
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from datetime import datetime
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.linear_model import LinearRegression
import joblib


def load_data_into_df(db_name: str) -> pd.DataFrame:
    try:
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM cars")
        df = pd.DataFrame(
            cursor.fetchall(),
            columns=[
                "Brand",
                "Model",
                "Fuel type",
                "Year",
                "Horse power",
                "Mileage",
                "Transmission",
                "Price",
                "Hash",
            ],
        )
        df = df.drop("Hash", axis=1)
        df["Year"] = datetime.now().year - df["Year"]
        return df
    except:
        print("Failed to load database")
        return


df = load_data_into_df("cars_data.db")
df_for_LR = df.drop(["Model", "Transmission", "Fuel type", "Price"], axis=1)
brands = sorted(df["Brand"].unique())
years = df["Year"].unique()


def fuel_type_distribution(df: pd.DataFrame, plot_name: str):
    names = df["Fuel type"].unique()
    counts = []
    for n in names:
        count = df[df["Fuel type"] == n].shape[0]
        counts.append(count)
    fig = make_subplots(1, 1, specs=[[{"type": "domain"}]])
    fig.add_trace(go.Pie(labels=names, values=counts, title="Fuel types distribution"))
    plotly.offline.plot(fig, filename=plot_name, auto_open=False, auto_play=False)


def best_selling_brands(df: pd.DataFrame, plot_name: str, top_n: int):
    brand_counts = pd.DataFrame(
        df.Brand.value_counts().reset_index().values, columns=["Manufacturers", "Count"]
    )
    data = brand_counts.head(top_n)
    fig = px.bar(
        data, x="Manufacturers", y="Count", title="Most popular car manufacturers"
    )
    plotly.offline.plot(fig, filename=plot_name, auto_open=False, auto_play=False)


def best_selling_models(df: pd.DataFrame, plot_name: str, top_n: int):
    top_brand = df["Brand"].value_counts().idxmax()
    df.drop(df[df["Model"] == "egyéb"].index, inplace=True)
    model_counts = pd.DataFrame(
        df.Model.value_counts().reset_index().values, columns=["Model", "Count"]
    )
    model_counts = model_counts.merge(
        df[["Model", "Brand"]], on="Model"
    ).drop_duplicates()
    model_counts["Color"] = model_counts["Brand"].apply(
        lambda x: "red" if x == top_brand else "blue"
    )
    data = model_counts.head(top_n)
    fig = px.bar(
        data,
        x="Model",
        y="Count",
        title=f"Most popular car models, models which relate to top brand is highlighted currently: {top_brand}",
        color="Color",
    ).update_xaxes(categoryorder="total descending")
    fig.update_layout(showlegend=False)
    plotly.offline.plot(fig, filename=plot_name, auto_open=False, auto_play=False)


def top_modell_statistics(df: pd.DataFrame, plot_name: str):
    def create_trace(col_name: str, subplots, row: int, col: int):
        traces = []
        fig = px.box(df[col_name])
        for trace in range(len(fig["data"])):
            traces.append(fig["data"][trace])
        for t in traces:
            subplots.append_trace(t, row=row, col=col)

    top_model = df["Model"].value_counts().idxmax()
    df = df[df["Model"] == top_model].iloc[:, 3:]
    df = df.describe().loc[["mean", "std", "min", "max"]]
    fig = make_subplots(rows=2, cols=2)
    create_trace("Year", fig, 1, 1)
    create_trace("Horse power", fig, 1, 2)
    create_trace("Mileage", fig, 2, 1)
    create_trace("Price", fig, 2, 2)
    fig.update_layout(title_text=f"{top_model} statistics")
    plotly.offline.plot(fig, filename=plot_name, auto_open=False, auto_play=False)


def car_age_distribution(df: pd.DataFrame, plot_name: str):
    group_by_age = (
        df.groupby(["Year"]).size().reset_index(name="counts").set_index("Year")
    )
    fig = px.line(group_by_age, y="counts", title="Number of vehicles for each age")
    fig.update_yaxes(title_text="number of vehicles")
    plotly.offline.plot(fig, filename=plot_name, auto_open=False, auto_play=False)


def median_price_variation_over_time(df: pd.DataFrame, plot_name: str):
    pivot = pd.pivot_table(df, values="Price", index="Year", aggfunc=np.median)
    pivot.columns = ["Median Price"]
    fig = px.line(pivot, y="Median Price", title="Median price changes over time")
    plotly.offline.plot(fig, filename=plot_name, auto_open=False, auto_play=False)


def average_milage_for_each_brand_over_time(df: pd.DataFrame, plot_name: str):
    df = df.sort_values(by="Year")
    fig = px.histogram(
        df,
        orientation="h",
        animation_frame="Year",
        y="Brand",
        x="Mileage",
        histfunc="avg",
        title="Average milage for each brand over the years",
    )
    fig.update_yaxes(categoryorder="total ascending")
    plotly.offline.plot(fig, filename=plot_name, auto_open=False, auto_play=False)


def linear_regression_modell_for_prediction_prices(
    df: pd.DataFrame,
) -> LinearRegression:
    # print(df.corr())
    df = df.drop(["Model", "Transmission", "Fuel type"], axis=1)

    y = df["Price"]
    df = df.drop(["Price"], axis=1)
    df = pd.get_dummies(df, columns=["Brand"], drop_first=True)
    X = df
    X_train, X_valid, y_train, y_valid = train_test_split(
        X, y, train_size=0.9, test_size=0.1, random_state=0
    )

    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_valid)
    print(f"LR Model error {mean_absolute_percentage_error(y_valid, y_pred)}")
    # print(pd.DataFrame(zip(X.columns, model.coef_)))
    new_car = pd.DataFrame(
        {"Brand": ["opel"], "Year": [10], "Horse power": [100], "Mileage": [10000]}
    )
    new_car_dummied = pd.get_dummies(new_car, columns=["Brand"], drop_first=True)
    new_car_dummied = new_car_dummied.reindex(columns=df.columns, fill_value=0)
    print(model.predict(new_car_dummied))

    joblib.dump(model, "model.pkl")


if __name__ == "__main__":
    template_path = "templates"
    df = load_data_into_df("cars_data.db")
    # fuel_type_distribution(df, os.path.join(template_path, "fuel_distribution.html"))
    # best_selling_brands(
    #     df, os.path.join(template_path, "best_selling_car_brands.html"), 20
    # )
    # best_selling_models(df, os.path.join(template_path, "best_selling_models.html"), 30)
    # top_modell_statistics(df, os.path.join(template_path, "top_model_statistics.html"))
    # car_age_distribution(df, os.path.join(template_path, "car_age_distribution.html"))
    # median_price_variation_over_time(
    #     df, os.path.join(template_path, "median_price_variation_over_time.html")
    # )
    # average_milage_for_each_brand_over_time(
    #     df, os.path.join(template_path, "average_milage_for_each_brand.html")
    # )
    linear_regression_modell_for_prediction_prices(df)
