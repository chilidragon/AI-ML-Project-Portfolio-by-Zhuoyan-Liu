from flask import Flask, render_template, request, jsonify
import boto3
import pandas as pd
from io import BytesIO, StringIO
import joblib

app = Flask(__name__, template_folder='templates', static_folder='static')

BUCKET_NAME = 'cloud-project-2'
MODEL_FILE_NAME = 'artifacts/trained_model_object.pkl'
DATA_FILE_NAME = 'artifacts/heart.csv'

s3 = boto3.client('s3')

def load_model():
    try:
        response = s3.get_object(Bucket=BUCKET_NAME, Key=MODEL_FILE_NAME)
        model_bytes = response['Body'].read()
        model = joblib.load(BytesIO(model_bytes)) 
        return model
    except Exception as e:
        app.logger.error(f"Failed to load model: {e}")
        return None

def load_data():
    try:
        response = s3.get_object(Bucket=BUCKET_NAME, Key=DATA_FILE_NAME)
        data_str = response['Body'].read().decode('utf-8')
        data = pd.read_csv(StringIO(data_str))
        return data
    except Exception as e:
        app.logger.error(f"Failed to load data: {e}")
        return None

data = load_data()
model = load_model()

@app.route('/', methods=['GET', 'POST'])
def index():
    if model is None:
        return jsonify({"error": "Model could not be loaded"}), 500

    if data is None:
        return jsonify({"error": "Data could not be loaded"}), 500

    try:
        # Handle the form input
        if request.method == 'POST':
            num_patients = int(request.form.get('num_patients', 5))  # Default value is 10 if not provided
        else:
            num_patients = 5  # Default value if the method is GET

        top_patients = data.nlargest(num_patients, 'prediction')[['Age', 'Cholesterol', 'Heart Rate']]

        # Generate data for charts
        age_data = data['Age'].value_counts().sort_index()
        age_labels = list(age_data.index)
        age_values = list(age_data.values)

        sedentary_data_0 = data[data['Heart Attack Risk'] == 0]['Sedentary Hours Per Day'].tolist()
        sedentary_data_1 = data[data['Heart Attack Risk'] == 1]['Sedentary Hours Per Day'].tolist()
        sedentary_labels = list(range(len(sedentary_data_0)))

        # Descriptive statistics
        descriptive_stats = data.groupby('Heart Attack Risk')['Sedentary Hours Per Day'].describe()
        shpd_descriptive_stats = descriptive_stats[['count', 'mean', 'std']].to_html(classes='table table-striped')

        return render_template(
            'index.html',
            patients=top_patients.to_html(classes='table table-striped'),
            age_labels=age_labels,
            age_data=age_values,
            sedentary_labels=sedentary_labels,
            sedentary_data_0=sedentary_data_0,
            sedentary_data_1=sedentary_data_1,
            shpd_stats=shpd_descriptive_stats,
            total_visits=data.shape[0],
            total_likes=sum(data['Heart Attack Risk'] == 1),
            total_comments=sum(data['Heart Attack Risk'] == 0)
        )
    except Exception as e:
        app.logger.error(f"Error processing data or generating visuals: {e}")
        return jsonify({"error": f"Error processing data or generating visuals: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
