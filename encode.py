import numpy as np
# import matplotlib.pyplot as plt

def encode_string(input_string):
    quad_arr = []
    for char in input_string:
        for i in [3,2,1,0]:
            # Right shift by the right amount and mask off last 2 bits
            quad_arr.append( (ord(char) >> 2 * i) & 0x03 )
    return quad_arr

def decode_string(quad_arr):
    if len(quad_arr) % 4 != 0: return 'ERR'
    idx = 0
    curr_ord = 0
    output_string = ''
    while idx < len(quad_arr):
        for i in [3,2,1,0]:
            curr_ord += quad_arr[idx+i] << 2*i
            idx += 1
        output_string += (chr(curr_ord))
        curr_ord = 0
    return output_string

def encode(sig, fname):
    tmp = np.zeros(2*len(sig), dtype='float32')
    tmp[::2] = np.real(sig)
    tmp[1::2] = np.imag(sig)
    tmp.tofile(fname)


if __name__ == '__main__':
    fname = 'send.dat'
    # Send ascii 'a' 0b01100001 and '!' 0b00100001
    # not really but 0b01110001 and 0b00100101
    header = np.array([3, 0, 0, 3, 3, 0, 2, 0, 2, 3, 3, 1, 2, 3, 1, 1, 1, 3, 3, 3, 2, 2, 3,
       1, 2, 0, 1, 0, 2, 2, 1, 1])
    pp = np.repeat(1+1j, 100)
    mm = np.repeat(-1-1j, 100)
    pm = np.repeat(1-1j, 100)
    mp = np.repeat(-1+1j, 100)
    bits = np.array([mm, mp, pm, pp])
    header = bits[header]
    header = header.flatten()
    tmp = np.concatenate((mm, pm, pp, pm, mm, mp, mm, pp))
    arr1 = np.tile(tmp, 20)
    arr1 = np.concatenate((np.zeros(5000), header, np.zeros(1000), arr1))
    arr1 = np.append(arr1, np.zeros(5000))
    encode(arr1, fname)

    q_arr = encode_string('Hello, World!')
    print('q_arr ' +str(q_arr))
    print(decode_string(q_arr))
