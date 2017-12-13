import numpy as np
import matplotlib.pyplot as plt

pulse_length = 5

PP = np.repeat(1+1j, pulse_length)
MM = np.repeat(-1-1j, pulse_length)
PM = np.repeat(1-1j, pulse_length)
MP = np.repeat(-1+1j, pulse_length)
BITS = np.array([MM, MP, PM, PP])

# Take in a string and construct an array of values 0-3 which represent 2-bit QAM encodings
def encode_string(input_string):
    quad_arr = []
    for char in input_string:
        for i in [3,2,1,0]:
            # Right shift by the right amount and mask off last 2 bits
            quad_arr.append( (ord(char) >> 2 * i) & 0x03 )
    return quad_arr

# Take in a list of bytes and return a list of MSB-first QAM values
def encode_byte_list(input_list):
    quad_arr = []
    for byte in input_string:
        for i in [3,2,1,0]:
            # Right shift by the right amount and mask off last 2 bits
            quad_arr.append( byte >> 2 * i) & 0x03 )
    return quad_arr

# Take an array of 0-3 QAM values and reconstruct a string
def decode_string(quad_arr):
    if len(quad_arr) % 4 != 0: return 'ERR'
    idx = 0
    curr_ord = 0
    output_string = ''
    shift = 0
    for symbol in quad_arr:
        curr_ord += symbol << (3-shift)*2
        shift = (shift + 1) % 4
        if shift == 0:
            output_string += (chr(curr_ord))
            curr_ord = 0
    return output_string

# Take an array of 0-3 MSB-first QAM values and reconstruct a byte list
def decode_byte_list(quad_arr):
    if len(quad_arr) % 4 != 0: return 'ERR'
    idx = 0
    curr_byte = 0
    output_list = []
    shift = 0
    for symbol in quad_arr:
        curr_byte += symbol << (3-shift)*2
        shift = (shift + 1) % 4
        if shift == 0:
            output_list.append(curr_byte)
            curr_byte = 0
    return output_list

def generate_white_noise(std=5, samples=5000, seed=4):
    mean = 0
    np.random.seed(seed)
    samples = np.random.normal(mean, std, size=samples)
    return samples+1j*samples


def make_pulse(data):
    data = np.array(data)
    signal = BITS[data]
    signal = signal.flatten()
    return signal

def encode(sig, fname):
    tmp = np.zeros(2*len(sig), dtype='float32')
    tmp[::2] = np.real(sig)
    tmp[1::2] = np.imag(sig)
    tmp.tofile(fname)
    return tmp


if __name__ == '__main__':
    fname = 'send.dat'
    # Send ascii 'a' 0b01100001 and '!' 0b00100001
    # not really but 0b01110001 and 0b00100101
    # header = np.array([3, 0, 0, 3, 3, 0, 2, 0, 2, 3, 3, 1, 2, 3, 1, 1, 1, 3, 3, 3, 2, 2, 3,
    #    1, 2, 0, 1, 0, 2, 2, 1, 1])
    header = [0, 3, 1, 2]
    header_pulse = make_pulse(header)
    noise_header4 = generate_white_noise(seed=4)
    noise_footer5 = generate_white_noise(seed=5)


    with open('gb_addr.txt', 'r') as infile:
        tx = encode_string(''.join(infile.readlines()))
        tx_data = make_pulse(tx)
        arr1 = np.concatenate((np.zeros(50*pulse_length), noise_header4, header_pulse, tx_data, noise_footer5))
        signal = encode(arr1, fname)

        expected = header + tx
        print(expected)
        print(len(expected))
        print('num_samples:' + str(len(arr1)/pulse_length))

    #     gb_addr = ''.join(infile.readlines())
    #
    #     print(gb_addr)
    #     print(encode_string(gb_addr))
    #     print(decode_string(encode_string(gb_addr)))
