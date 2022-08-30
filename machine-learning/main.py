import pandas as pd
from tensorflow import keras
from tensorflow.keras import layers
from datetime import datetime
import os


model = keras.Sequential(
    [
        keras.Input(shape=(1,)),
        layers.Dense(32, activation="relu", name="layer1"),
        layers.Dense(32, activation="relu", name="layer2"),
        layers.Dense(, name="layer3"),
    ]
)

model.compile(optimizer='rmsprop', loss='categorical_crossentropy')


for l in os.listdir("../data/csvs/"):
    df = pd.read_csv("../data/csvs/" + l)

    # fill nan with zeros
    df = df.fillna(0)

    date = l.split(".")[0]
    date = date.split("_")[-1]
    date = date[:4] + "-" + date[4:6] + "-" + date[6:8]
    date = datetime.fromisoformat(date)
    days = (datetime.strptime('22-02-2026', '%d-%m-%Y') - date).days

    model.train_on_batch((days,), df)
