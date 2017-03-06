import scipy.signal as signal
import pylab as pl
import numpy as np

#取样频率为8kHz
sampling_rate = 100.0

# 设计一个带通滤波器：
# 通带为0.2*4000 - 0.5*4000
# 阻带为<0.1*4000, >0.6*4000
# 通带增益的最大衰减值为2dB
# 阻带的最小衰减值为40dB
b, a = signal.iirdesign([0.2, 0.5], [0.1, 0.6], 2,40)

sig=np.random.random([1000])

# 将频率扫描信号进行滤波
out = signal.lfilter(b, a, sig)

# 将波形转换为能量

pl.subplot(211)
pl.plot(sig)
pl.subplot(212)
pl.plot(out)
