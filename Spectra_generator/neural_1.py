# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 09:01:07 2023

@author: Alonso
"""

import tensorflow as tf
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve
from sklearn.metrics import auc
import matplotlib as mpl
import matplotlib.pyplot as plt

ndata = 10
nfreq = 32768
x = np.loadtxt('I:\\a\\espectros\\prueba\\alonso\\x.txt', dtype = 'float64')
x = x.reshape(ndata, nfreq, 1)
y = np.loadtxt('I:\\a\\espectros\\prueba\\alonso\\yalinear.txt', dtype = 'float64')
y = y.reshape(ndata, nfreq, 1)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.5)

model = tf.keras.models.Sequential([
  tf.keras.layers.Conv1D(64, kernel_size = 5, activation = 'relu', input_shape = (nfreq, 1)),
  tf.keras.layers.Conv1D(32, kernel_size = 5, activation = 'relu'),
  tf.keras.layers.Flatten(),
  tf.keras.layers.Dense(100, activation = 'relu'),
  tf.keras.layers.Dense(nfreq, activation = 'relu')
])

model.compile(optimizer='adam',
              loss='mean_squared_error',
              metrics=['mean_squared_error'])


model.fit(x_train, y_train, epochs = 100)

model.summary()

model.evaluate(x_train, y_train)
model.evaluate(x_test, y_test)