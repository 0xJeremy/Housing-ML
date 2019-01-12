from __future__ import absolute_import, division, print_function

import pathlib

import pandas as pd
import seaborn as sns

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
#import data
raw_dataset = pd.read_csv('training_housing_data.csv', na_values = '?')
dataset = raw_dataset.copy()

#normalize price for zipcode
dataset['price'] = dataset['price']/dataset['homemarkup']
dataset = dataset.drop(['homemarkup'], axis=1)

#split data
train_dataset = dataset.sample(frac=0.8, random_state=0)
test_dataset = dataset.drop(train_dataset.index)

#dataset statistics
train_stats = train_dataset.describe()
train_stats.pop('price')
train_stats = train_stats.transpose()


#sns.pairplot(train_dataset[['price', 'bedrooms', 'bathrooms', 'floors', 'sqft_basement', 'sqft_living15', 'sqft_lot15', 'homevalue']], diag_kind='kde')
#split off labels
train_labels = train_dataset.pop('price')
test_labels = test_dataset.pop('price')



def norm(x):
  return (x - (train_stats['50%']+train_stats['mean'])/2) / train_stats['std']

normed_train_data = norm(train_dataset)
normed_test_data = norm(test_dataset)


def build_model():
  model = keras.Sequential([
        layers.Dense(64, activation=tf.nn.relu, input_shape=[len(train_dataset.keys())]),
        layers.Dense(64, activation=tf.nn.relu), 
        layers.Dense(64, activation=tf.nn.relu),
        layers.Dense(1)
        ])
  
  optimizer = tf.train.RMSPropOptimizer(0.001)
  
  model.compile(loss='mse',
            optimizer=optimizer,
            metrics=['mae','mse'])
  return model

model = build_model()

early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=50)

class PrintDot(keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs):
         epoch % 100 == 0: print('')
        int('.', end='')
        POCHS = 100000

history = model.fit(normed_train_data, train_labels, epochs=EPOCHS,
            validation_split=0.2, verbose=0,
            callbacks=[early_stop, PrintDot()])

hist = pd.DataFrame(history.history)
hist['epoch'] = history.epoch
print(hist.tail())

#analysis
import matplotlib.pyplot as plt
#error
def plot_history(history):
  plt.figure()
  plt.xlabel('Epoch')
  plt.ylabel('Mean Abs Error [Price]')
  plt.plot(hist['epoch'], hist['mean_absolute_error'],
         label='Train Error')
  plt.plot(hist['epoch'], hist['val_mean_absolute_error'],
         label = 'Val Error')
  plt.legend()
  plt.ylim([0,5])
  
  plt.figure()
  plt.xlabel('Epoch')
  plt.ylabel('Mean Square Error [Price^2]')
  plt.plot(hist['epoch'], hist['mean_squared_error'],
         label='Train Error')
  plt.plot(hist['epoch'], hist['val_mean_squared_error'],
         label = 'Val Error')
  plt.legend()
  plt.ylim([0,5000000000])

plot_history(history)

#absolute average dollar error
loss, mae, mse = model.evaluate(normed_test_data, test_labels, verbose=0)
print("Testing set Mean Abs Error: ${:5.2f}".format(mae))

#predicted vs. actual sale prices
test_predictions = model.predict(normed_test_data).flatten()

plt.scatter(test_labels, test_predictions)
plt.xlabel('True Values [Normalized Price]')
plt.ylabel('Predictions [Normalized Price]')
plt.axis('equal')
plt.axis('square')
plt.xlim([0,plt.xlim()[1]])
plt.ylim([0,plt.ylim()[1]])
_ = plt.plot([-100, 100], [-100, 100])

#error distribution
error = test_predictions - test_labels
plt.hist(error, bins = 25)
plt.xlabel("Prediction Error [Normalized Price]")
_ = plt.ylabel("Count")

#test with independent homes
test_property = pd.read_csv['testproperties.csv']
test_property = norm(test_property)
test_predictions = model.predict(test_prop)
print(test_predictions)
#this is the normalized price. You then need to go back and correct for home value gain since 01/2014 
#as well as home value by zipcode