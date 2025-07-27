# Import necessary libraries
from flask import Flask, request, render_template
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

# Import your custom prediction pipeline and data schema
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

# Initialize Flask app
application = Flask(__name__)
app = application

# -------------------------------------
# Route for landing page (index.html)
# -------------------------------------
@app.route('/')
def index():
    return render_template('index.html')


# -------------------------------------------------
# Route for prediction page (GET = form, POST = predict)
# -------------------------------------------------
@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        try:
            # 1. Get form data and create CustomData instance
            data = CustomData(
                gender=request.form.get('gender'),
                race_ethnicity=request.form.get('ethnicity'),
                parental_level_of_education=request.form.get('parental_level_of_education'),
                lunch=request.form.get('lunch'),
                test_preparation_course=request.form.get('test_preparation_course'),
                reading_score=float(request.form.get('reading_score')),
                writing_score=float(request.form.get('writing_score'))
            )

            # 2. Convert to DataFrame
            pred_df = data.get_data_as_data_frame()
            print("✅ Input DataFrame:\n", pred_df)

            # 3. Predict using pipeline
            predict_pipeline = PredictPipeline()
            results = predict_pipeline.predict(pred_df)
            print("✅ Prediction Result:", results)

            # 4. Return result to page
            return render_template('home.html', results=results[0])

        except Exception as e:
            # 5. Catch and print any errors
            print("❌ ERROR during prediction:", str(e))
            return render_template('home.html', results="⚠️ Error: " + str(e))


# -------------------------------------
# Main entry point
# -------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0")
