from flask import Flask, render_template, request
from data_evaluation import brands, df_for_LR
import pandas as pd
import joblib
import webbrowser
from threading import Timer

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
    brand = ""
    year = ""
    horse_power = ""
    mileage = ""

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

        df = pd.get_dummies(df_for_LR, columns=["Brand"], drop_first=True)
        new_car_dummied = pd.get_dummies(new_car, columns=["Brand"], drop_first=True)
        new_car_dummied = new_car_dummied.reindex(columns=df.columns, fill_value=0)
        try:
            model = joblib.load("model.pkl")
            price = model.predict(new_car_dummied)
            if price[0] > 0:
                result = f"Price: € {int(price[0])}"
            else:
                result = "The model is not suitable for such specs"
        except:
            result = "A problem has occurred please try again later"

    return render_template(
        "calculator.html",
        brands=brands,
        result=result,
        year=year,
        brand=brand,
        horse_power=horse_power,
        mileage=mileage,
    )


def open_browser():
    webbrowser.open_new("http:/127.0.0.1:5000")


if __name__ == "__main__":
    Timer(1, open_browser).start()
    app.run(port=5000)
