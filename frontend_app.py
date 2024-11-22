from flask import Flask, render_template, request
from data_evaluation import brands, years, df_for_LR
import pandas as pd
import joblib

app = Flask(__name__)


@app.route("/")
def introduction():
    return render_template("index.html")


@app.route("/average_milage")
def diagramm_average_milage_diagram():
    return render_template("average_milage_for_each_brand.html")


@app.route("/best_selling_car_brand")
def diagramm_best_selling_car():
    return render_template("best_selling_car_brands.html")


@app.route("/best_selling_models")
def diagramm_best_selling_models():
    return render_template("best_selling_models.html")


@app.route("/fuel_distribution")
def diagramm_fuel_distribution():
    return render_template("fuel_distribution.html")


@app.route("/car_age_distribution")
def diagramm_car_age_distribution():
    return render_template("car_age_distribution.html")


@app.route("/median_price_variation")
def diagramm_median_price_variation():
    return render_template("median_price_variation_over_time.html")


@app.route("/top_model_statistics")
def diagramm_top_model():
    return render_template("top_model_statistics.html")


@app.route("/calculator", methods=["GET", "POST"])
def calculate_price():
    result = None
    new_car = pd.DataFrame(
        {
            "Brand": ["audi"],
            "Year": [20],
            "Horse power": [200],
            "Mileage": [200000],
        }
    )
    new_car_dummied = pd.get_dummies(new_car, columns=["Brand"], drop_first=True)
    new_car_dummied = new_car_dummied.reindex(columns=df_for_LR.columns, fill_value=0)
    # try:
    model = joblib.load("model.pkl")
    price = model.predict(new_car_dummied)
    result = f"Price: € {price}"
    print(result)
    if request.method == "POST":
        brand = request.form["brand"]
        year = int(request.form["year"])
        horse_power = int(request.form["horse_power"])
        mileage = int(request.form["mileage"])

        new_car = pd.DataFrame(
            {
                "Brand": [brand],
                "Year": [year],
                "Horse power": [horse_power],
                "Mileage": [mileage],
            }
        )
        # new_car_dummied = pd.get_dummies(new_car, columns=["Brand"], drop_first=True)
        # new_car_dummied = new_car_dummied.reindex(
        #     columns=df_for_LR.columns, fill_value=0
        # )
        # # try:
        # model = joblib.load("model.pkl")
        # price = model.predict(new_car_dummied)
        # result = f"Price: € {price}"
        # print(result)
        # except:
        result = "A problem has occurred please try again later"

    return render_template("calculator.html", brands=brands, years=years, price=result)


if __name__ == "__main__":
    app.run()
