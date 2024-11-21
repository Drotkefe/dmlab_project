from flask import Flask, render_template, request
from data_evaluation import model, encoder, brands, years

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
    if request.method == "POST":
        brand = request.form["brand"]
        year = request.form["year"]
        horse_power = request.form["horse_power"]
        mileage = request.form["mileage"]

    return render_template("calculator.html", brands=brands, years=years)


if __name__ == "__main__":
    app.run()
