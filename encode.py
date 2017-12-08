import numpy as np
import matplotlib.pyplot as plt

PP = np.repeat(1+1j, 100)
MM = np.repeat(-1-1j, 100)
PM = np.repeat(1-1j, 100)
MP = np.repeat(-1+1j, 100)
BITS = np.array([MM, MP, PM, PP])

def generate_white_noise():
    mean = 0
    std = 1 
    num_samples = 1000
    np.random.seed(4)
    samples = np.random.normal(mean, std, size=num_samples)
    return samples


def make_pulse(data):
    signal = BITS[data]
    signal = signal.flatten()
    return signal

def encode(sig, fname):
    tmp = np.zeros(2*len(sig), dtype='float32')
    tmp[::2] = np.real(sig)
    tmp[1::2] = np.imag(sig)
    tmp.tofile(fname)


if __name__ == '__main__':
    fname = 'send.dat'
    # Send ascii 'a' 0b01100001 and '!' 0b00100001
    # not really but 0b01110001 and 0b00100101
    # header = np.array([3, 0, 0, 3, 3, 0, 2, 0, 2, 3, 3, 1, 2, 3, 1, 1, 1, 3, 3, 3, 2, 2, 3,
    #    1, 2, 0, 1, 0, 2, 2, 1, 1])
    # header = make_pulse(header)
    noise_header = generate_white_noise()
    tmp = make_pulse(np.array([1,2,3,2,0,1,0,3]))
    arr1 = np.tile(tmp, 20)
    arr1 = np.concatenate((np.zeros(5000), noise_header, np.zeros(5000), arr1))
    arr1 = np.append(arr1, np.zeros(5000))
    encode(arr1, fname)
    plt.plot(arr1)
    plt.show()