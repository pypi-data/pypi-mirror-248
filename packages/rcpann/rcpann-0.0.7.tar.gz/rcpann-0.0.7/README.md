# RCPANN - Ring Current Proton ANN Model

[![N|Solid](https://cldup.com/dTxpPi9lDf.thumb.png)](https://nodesource.com/products/nsolid)

The Ring Current Proton Artificial Neural Network (RCPANN) model specifies the ring current proton distribution using artificial neural network (multi-layer perceptron).

This model is based on RBSP/RBSPICE measurements from 2013-2018. The RBSPICE measures proton flux at 14 energy channels from 45 keV to 598 keV, and this model provides proton spin-averaged flux in those 14 energy channels. The data for the training and modeling are available at https://doi.org/10.5281/zenodo.7651736. The training program are available ar https://github.com/jinxingli87/RCPANN.

## How to use the RCPANN model
First, pip install the 'rcpann' package. Tensorflow and Pytorch packages are required. 
```sh
pip3 install rcpann
```

## ✨ Example 1: Predict proton flux at a specific moment
Input: iek, coord in shape of either (4,) or (1,4), and tstr in form of 'yyyy-mm-dd hh:mm:ss'
The iek should be a number between 0 and 13, and the corresponding energy is listed below.
|iek|0|1|2|3|4|5|6|7|8|9|10|11|12|13|
| ------ | ------ |------ | ------ |------ | ------ |------ | ------ |------ | ------ |------ | ------ |------ | ------ |------ |
|Energy (keV)|45|55|67|82|99|121|148|181|220|269|328|400|489|598|
```python3
from rcpann import *
iek=1
coord=np.array([3.5, 0.0, 1.0, 0.0]) # L=3.5, cos(theta)=0, sin(theta)=1.0, Lat=0.0, which means MLT = 6h
print(pflux(iek,coord,tstr = '2017-03-01 22:42:00'))
```

## ✨ Example 2. Model the global distribution of proton flux
```python3
from rcpann import *
iek=1
tstr1='2017-03-01 22:42:00'
tstr2='2017-03-04 23:59:00'
rcpann_global_dist(iek,tstr1,tstr2)
```



Please contact jinxing.li.87@gmail.com for support.


## License

MIT

**Free Software, Hell Yeah!**


