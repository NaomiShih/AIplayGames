from __future__ import print_function
import cv2
import sys
sys.path.append("game/")
import Wrapped_LK as game
import random
from collections import deque
import numpy as np
from keras import backend as K
import tensorflow as tf 
import keras
import keras.initializers as initializer
from keras.models import Model
from keras.layers import *
from keras.optimizers import *
from keras.activations import *
from keras.models import Sequential, Model
from functools import reduce
import math
import os
from keras.models import load_model
import keras.losses


ACTIONS = 2 # number of valid actions
GAMMA = 0.99 # decay rate of past observations
OBSERVE = 50000. # timesteps to observe before training
EXPLORE = 2000000. # frames over which to anneal epsilon
FINAL_EPSILON = 0.1 # final value of epsilon
INITIAL_EPSILON = 0.0001 # starting value of epsilon
REPLAY_MEMORY = 50000 # number of previous transitions to remember
BATCH = 32 # minibatch size

	
def image_preprocess(img):
	resized = cv2.resize(img, (80, 80))
	gray =  np.expand_dims(cv2.transpose(cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)), axis=2)
	r ,t = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
	t = np.reshape(t, (80, 80, 1))
	#print(x_t.shape, resized.shape)
	s_t = np.concatenate((t,t,t,t),axis=2)
	#print(s_t.shape, resized.shape)
	return s_t


## Custom Loss function using keras layers as input
def custom_loss(mul,y):
	def loss(y_true,y_pred):
		L = K.square(y - mul)
		return L
	# Return a function
	return loss


def network():
	inputs = Input((80,80,4))
	a = Input(shape=(ACTIONS,))
	y = Input(shape=(1,),dtype = float)
	conv1 = Conv2D(filters=32, strides=4, activation='relu',padding='same',use_bias=True, 
		kernel_size=[8,8], kernel_initializer=initializer.TruncatedNormal(stddev=0.01),
		bias_initializer=initializer.Constant(value=0.01))(inputs)
	maxpool1 = MaxPooling2D(pool_size=2, strides=2, padding='same')(conv1)
	conv2 = Conv2D(filters=64, strides=2, activation='relu',padding='same',use_bias=True, 
		kernel_size=[4,4], kernel_initializer=initializer.TruncatedNormal(stddev=0.01),
		bias_initializer=initializer.Constant(value=0.01))(maxpool1)
	#maxpool2 = MaxPooling2D(pool_size=2, strides=2, padding='same')(conv2)
	conv3 = Conv2D(filters=64, strides=1, activation='relu',padding='same',use_bias=True, 
		kernel_size=[1,1], kernel_initializer=initializer.TruncatedNormal(stddev=0.01),
		bias_initializer=initializer.Constant(value=0.01))(conv2)
	#maxpool3 = MaxPooling2D(pool_size=2, strides=2, padding='same')(conv3)
	fci = Flatten()(conv3)
	fc1 = Dense(512, activation='relu',use_bias=True,kernel_initializer=initializer.TruncatedNormal(stddev=0.01), bias_initializer=initializer.Constant(value=0.01))(fci)
	fc2 = Dense(ACTIONS, activation='linear',use_bias=True,kernel_initializer=initializer.TruncatedNormal(stddev=0.01), bias_initializer=initializer.Constant(value=0.01))(fc1)
	
	mask = Dot(axes=1)([fc2,a])

	model = Model([inputs,a,y], fc2)
	
	opt = Adam(lr=0.0001)
	model.compile(optimizer=opt,loss=custom_loss(mask,y))
	
	model.summary()
	return model

def train():
	B = int(input('Press 0 if you want to train from start or 1 if you want to test : '))
	model = network()
	if B==1:
		model.load_weights("trained_model/dell-4410000.h5")
	D = deque()
	epsilon = INITIAL_EPSILON
    #showed error: 
    #IndentationError: unindent does not match any outer indentation level
    #but wtf?
    game_state = game.GameState(player, Platform)

	dummy_a = np.zeros(ACTIONS)
	dummy_a[0] = 1

    #wtf is dummy_a? replaced variavle in frame_step	
    x_tc, r_t, T_t = game_state.frame_step()
	x_t = image_preprocess(x_tc)
	x_tt = x_t
	t = 0
	while 1:
		t += 1
		
		x_t = np.asarray([x_tt])
		a_t = np.zeros([ACTIONS])
		dummy_a = np.asarray([a_t])
		dummy_y = np.asarray([[0.0]])
		action_index = 0
		
		Q_t = model.predict([x_t,dummy_a,dummy_y])[0]  ## Model prediction using current image
		
		## Choosing action

		if random.random() <= epsilon:
			print("RANDOM step")
			action_index = random.randrange(ACTIONS)
		else:
			action_index = np.argmax(Q_t)
		a_t[action_index] = 1

		if epsilon > FINAL_EPSILON and t > OBSERVE:
			epsilon -= (INITIAL_EPSILON - FINAL_EPSILON) / EXPLORE

		x_tc, r_t, T_t = game_state.frame_step(a_t)
		
		x_tn = image_preprocess(x_tc)
		D.append((x_tt, a_t, r_t, x_tn, T_t))	# Maintaining replay memory
		
		x_tt = x_tn

		if len(D) > REPLAY_MEMORY:
			D.popleft()

		if B != 1:
			if t % 25000 == 0:
				model.save_weights('trained_model/' + 'dqn' + str(t)+'.h5')
				print("Time : ", t)


			if t > OBSERVE:

				## Sampling mini batch at random to train 
				
				minibatch = random.sample(D, BATCH)

				s_t_batch = np.asarray([d[0] for d in minibatch])
				a_batch = np.asarray([d[1] for d in minibatch])
				r_batch = np.asarray([d[2] for d in minibatch])
				s_tn_batch = np.asarray([d[3] for d in minibatch])
				t_batch = [d[4] for d in minibatch]

				y_batch = np.zeros(BATCH)
				y_batch_dummy = np.zeros(BATCH)
				Q_tn_batch = model.predict_on_batch([s_tn_batch,a_batch,y_batch_dummy])
				for i in range(0, len(minibatch)):
					if t_batch[i]:
						#print("terminal", r_batch[i])
						y_batch[i] = r_batch[i]
					else:
						y_batch[i] = r_batch[i] + GAMMA * np.max(Q_tn_batch[i])
				#print(y_batch)
				#break
				model.fit(x=[s_t_batch,a_batch,y_batch], y=y_batch,batch_size=32,verbose=0)

		print("T:", t ,"| EPS:", epsilon, "| A", action_index, "| R", r_t, "| Q ", Q_t)

def main():
	train()

if __name__ == "__main__":
	main()