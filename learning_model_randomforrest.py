# -*- coding: utf-8 -*-
"""Learning_Model_RandomForrest.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ptxk7RN6P2cRWWbbwCBs7xmn1nZYx4IV
"""

# Install Our Libraries
!apt-get update
!apt-get install openjdk-11-jdk-headless -qq > /dev/null
!wget https://dlcdn.apache.org/spark/spark-3.5.3/spark-3.5.3-bin-hadoop3.tgz
!tar -xvzf spark-3.5.3-bin-hadoop3.tgz
!pip install -q findspark
!pip install hvplot holoviews bokeh
!pip install plotly
!pip install keras-tuner

!pip install tensorflow-addons==0.21.0

#Importing in our dependencies
import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import os
from pyspark import SparkFiles
import holoviews as hv
hv.extension('bokeh')
import hvplot.pandas
from pathlib import Path
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.utils import resample
import plotly.express as px
import tensorflow as tf
from sklearn.preprocessing import OneHotEncoder
import hvplot


# Set Environment Variables
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-11-openjdk-amd64"
os.environ["SPARK_HOME"] = "/content/spark-3.5.3-bin-hadoop3"
os.environ["PATH"] += ":/content/spark-3.5.3-bin-hadoop3/bin"


# Start a SparkSession
import findspark
findspark.init()

# Start Spark session
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("DataFrame Basics").getOrCreate()

# Start a Spark session
from pyspark.sql import SparkSession

# Adding in the header and printing our DataFrame
df = spark.read.csv("/content/school_modality_data.csv", header = True, inferSchema=True)
df.show()

# Print our schema
df.printSchema()

# Describe our data
df.describe()

# Drop the uneccesary columns
school_modality_df = df.drop('operational_schools', 'zip_code', "district_nces_id")
school_modality_df.show()

#Converting our dataframe from a spark dataframe to a pandas dataframe
cleaned_modality_df = school_modality_df.toPandas()
cleaned_modality_df.head()

# Dropping BI from our States Column
cleaned_modality_df = cleaned_modality_df.drop(cleaned_modality_df[cleaned_modality_df['state'] == 'BI'].index)

# Converting the weeks column to a Ordinal version
cleaned_modality_df['week'] = cleaned_modality_df['week'].apply(lambda x: x.toordinal())

# Counting totals of our learning modalities
modality_counts = cleaned_modality_df.groupby("learning_modality").size().reset_index(name='count')
print(modality_counts)

# Encoding our Dataframe
encoder = OneHotEncoder(sparse_output=False)
modality_encoded = encoder.fit_transform(cleaned_modality_df[['learning_modality']])

# Add the encoded columns back to the DataFrame
modality_encoded_df = pd.DataFrame(modality_encoded, columns=encoder.get_feature_names_out(['learning_modality']))
encoded_modality_df = pd.concat([cleaned_modality_df, modality_encoded_df], axis=1).drop(columns=['learning_modality'])
encoded_modality_df = encoded_modality_df.dropna()
encoded_modality_df.head()

# Selecting our Features
X = encoded_modality_df[['learning_modality_Remote', 'learning_modality_In Person', 'learning_modality_Hybrid']]
y = encoded_modality_df['student_count']

X_train = encoded_modality_df[['learning_modality_Remote', 'learning_modality_In Person', 'learning_modality_Hybrid']]

print(X_train.shape)

# Splitting up the Data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

from sklearn.ensemble import RandomForestRegressor

# Fitting up our Model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Check if it's a DataFrame and for NaN values
print(X_train.shape, X_test.shape)
print(X_train.info())
print(np.isnan(X_train).sum())

# Replace NaN and infinite values with 0
X_train = np.nan_to_num(X_train)
X_test = np.nan_to_num(X_test)

# Convert our y-train to integer
y_train = y_train.astype(int)

from sklearn.preprocessing import LabelEncoder

# Reindex the Labels for consisten range
encoder = LabelEncoder()
y_train_encoded = encoder.fit_transform(y_train)

# Create and fit the StandardScaler
from sklearn.preprocessing import StandardScaler

# Fit and scale training data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Assigning Class Weights because of how large the DataFrame is
from sklearn.utils.class_weight import compute_class_weight

# Compute class weights
class_weights = compute_class_weight('balanced', classes=np.unique(y_train_encoded), y=y_train_encoded)
class_weights_dict = dict(zip(np.unique(y_train_encoded), class_weights))

print(class_weights_dict)

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from tensorflow.keras.regularizers import l2

# Define the model
nn = Sequential()

# Input layer and first hidden layer
nn.add(Dense(256, activation='relu', input_shape=(X_train_scaled.shape[1],)))
nn.add(BatchNormalization())
nn.add(Dropout(0.5))

# Second hidden layer
nn.add(Dense(128, activation='relu'))
nn.add(BatchNormalization())
nn.add(Dropout(0.5))

# Third hidden layer
nn.add(Dense(64, activation='relu'))
nn.add(BatchNormalization())
nn.add(Dropout(0.5))

# Noramlize the Batch & Dropout to improve Generalization and Convergence
nn.add(tf.keras.layers.BatchNormalization())
nn.add(tf.keras.layers.Dropout(0.5))

# Output layer
nn.add(Dense(len(np.unique(y_train_encoded)), activation='softmax'))

# Check if there are any NaN or inf values in the training data
print(np.any(np.isnan(X_train_scaled)), np.any(np.isinf(X_train_scaled)))

# Check the mean and standard deviation
print("Mean of X_train_scaled:", np.mean(X_train_scaled, axis=0))
print("Std of X_train_scaled:", np.std(X_train_scaled, axis=0))

print(np.bincount(y_train))

from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping

# Set a fraction of the data (e.g., 10%)
sample_fraction = 0.1
sample_size = int(sample_fraction * X_train_scaled.shape[0])

# Create the sampled dataset
X_train_sampled = X_train_scaled
y_train_sampled = y_train_encoded

# Compiling out Model
nn.compile(optimizer=Adam(learning_rate=1e-4),
           loss="sparse_categorical_crossentropy",
           metrics=["accuracy"])

early_stopping = EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True)

# Train the model with the sampled data
fit_model = nn.fit(
    X_train_sampled, y_train_sampled,
    epochs=50, batch_size=128, validation_split=0.2,
    class_weight=class_weights_dict,
    callbacks=[early_stopping]
)

from sklearn.metrics import mean_squared_error, r2_score

# Evaluation of the Model
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
rmse = mse ** 0.5
r2 = r2_score(y_test, y_pred)

print("RMSE:", rmse)
print("R² Score:", r2)

#Scatter Plot of Student Counts based on Modality
student_count_plot = cleaned_modality_df.hvplot.scatter(
    x="learning_modality",
    y="student_count",
    by="week",
    title="Student Counts by School Modality (Faceted by Week)"
)
student_count_plot