import numpy as np

# encode matrix
G = np.array([  [1, 1, 0, 1],
                [1, 0, 1, 1],
                [1, 0, 0, 0],
                [0, 1, 1, 1],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]
                ])

# error check matrix
H = np.array([  [1, 0, 1, 0, 1, 0, 1],
                [0, 1, 1, 0, 0, 1, 1],
                [0, 0, 0, 1, 1, 1, 1]
              ])

# decoding matrix
R = np.array([  [0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 1, 0],
                [0, 0, 0, 0, 0, 0, 1]
                ])

def hamming_encode(bits):
    bits_reshaped = np.reshape(bits, (-1, 4)).transpose()
    encoded = np.dot(G,bits_reshaped)%2
    return encoded.transpose()

def hamming_error_check(bits):
    bits_reshaped = np.reshape(bits, (-1, 7)).transpose()
    errors = np.dot(H,bits_reshaped)%2
    return errors.transpose()

def calcerror(arr):
    return np.packbits(errors, axis=1) >> 5

def hamming_correct(res, errs):
    arr = np.zeros((len(errs),7))
    resh = res.reshape(-1,7)
    for i,e in enumerate(errs):
        if e > 0:
            resh[i,8-e] = 1-resh[i,8-e]
    return resh

def hamming_decode(bits):
    bits_reshaped = np.reshape(bits, (-1, 7)).transpose()
    decoded = np.dot(R, bits_reshaped)
    return decoded.transpose()
    