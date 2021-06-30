import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import shap
import pickle

with open('finalized_model.pkl', 'rb') as file:
    model = pickle.load(file)


def load_dataframe(file_name):
    df = pd.read_csv(file_name).iloc[:100]
    return df


def plot_feature_importance(model):
    df = pd.read_csv('model.csv')
    df.drop(columns=['Unnamed: 0', 'Unit Price ($ PSF)'], inplace=True)

    features = df.columns.to_list()
    importances = model.best_estimator_.feature_importances_
    indices = np.argsort(importances)

    features_ordered = [features[i] for i in indices]

    fig, ax = plt.subplots(figsize=(12, 8))

    ax.barh(
        y=range(len(indices)),
        width=importances[indices],
        tick_label=features_ordered)
    ax.set(
        title='Feature Importances',
        xlabel='Relative Importance'
    )

    st.pyplot(fig)


def st_shap(plot, height=None):
    shap_html = f"<head>{shap.getjs()}</head><body>{plot.html()}</body>"
    components.html(shap_html, height=height)


def shap_plot(model):
    df = pd.read_csv('model.csv')
    df.drop(columns=['Unnamed: 0', 'Unit Price ($ PSF)'], inplace=True)

    explainer = shap.TreeExplainer(model.best_estimator_)
    shap_values = explainer.shap_values(df)

    st_shap(shap.force_plot(explainer.expected_value, shap_values, df), 400)


def app():
    # csv file used to train
    st.write('''
    # Understand our model! 
    
    First up, let's set some context!

    Here is a snippet of the data we used to train our model. Do keep in mind that this is after cleaning! (But before preprocessing)
    
    We got this data from (INSERT LINK HERE!)
    ''')
    train_df = load_dataframe('to_show_public.csv')
    st.dataframe(train_df)

    # Model performance
    st.write('''
    We used this data to train a random forest data with a r2 score of 0.88 and a rmse score of 182.

    This means that we are 95% confident of that our prediction is within +- $182/sqft!

    Below, you can also see which features are the most important in making the predictions!
    ''')

    # feature importance from sklearn
    plot_feature_importance(model)

    # feature importance from shap
    # Seems like this takes too long to load D:
    # shap_plot(model)
