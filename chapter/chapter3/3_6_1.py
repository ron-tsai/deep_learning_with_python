import keras

from keras.datasets import boston_housing
(train_data,train_targets),(test_data,test_targets)=boston_housing.load_data()

#(x-μ)/st
mean=train_data.mean(axis=0)
train_data-=mean
std=train_data.std(axis=0)
train_data/=std

test_data-=mean
test_data/=std

from keras import models
from keras import layers

def build_model():
    model=models.Sequential()
    model.add(layers.Dense(64,activation='relu',
                           input_shape=(train_data.shape[1],)))
    model.add(layers.Dense(64,activation='relu'))
    model.add(layers.Dense(1))
    model.compile(optimizer='rmsprop',loss='mse',metrics=['mae'])
    return model

#k-fold validation（资料少的情况）
#切成n份，分别做验证数据和训练数据，做n次，将最终数据平均

import numpy as np

k=4
num_val_samples=len(train_data)//k  #//取商（不要小数点）
num_epochs=100
all_scores=[]
for i in range(k):
    print('processing fold #',i)
    val_data=train_data[i*num_val_samples:(i+1)*num_val_samples]
    val_targets=train_targets[i*num_val_samples:(i+1)*num_val_samples]

    partial_train_data=np.concatenate(
        [train_data[:i*num_val_samples],
         train_data[(i+1)*num_val_samples:]],
        axis=0
    )   #axis=0根据y轴粘合
    partial_train_targets=np.concatenate(
        [train_targets[:i*num_val_samples],
         train_targets[(i+1)*num_val_samples:]],
        axis=0
    )

    model=build_model()
    model.fit(partial_train_data,partial_train_targets,
              epochs=num_epochs,batch_size=16,verbose=2)
    val_mse,val_mae=model.evaluate(val_data,val_targets,verbose=2)
    all_scores.append(val_mae)

print(all_scores)

a59=np.mean(all_scores)
print(a59)

from keras import backend as k

k.clear_session()

