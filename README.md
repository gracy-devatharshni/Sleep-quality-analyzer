# Sleep Quality Analyzer

This project predicts sleep quality based on user inputs using a machine learning model.

## Setup

1. Ensure you have Python installed (preferably 3.8+).
2. Create and activate a virtual environment:
   ```
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the App

To run the Streamlit web app:

```
streamlit run app.py
```

This will start a local web server. Open the provided URL in your browser to use the app.

## Training the Model (Optional)

If you want to retrain the model, open and run the `train.ipynb` notebook in Jupyter.

## Data

The dataset is located in `data/Sleep_health_and_lifestyle_dataset.csv`.

## Troubleshooting

- If you get import errors, ensure all dependencies are installed.
- Make sure the model files in `model/` are present.