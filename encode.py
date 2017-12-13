import numpy as np
# import matplotlib.pyplot as plt
from hamming import *
from bits import *

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
            quad_arr.append( (byte >> (2 * i)) & 0x03 )
    return quad_arr

# Takes in a flattened list of bits and maps them to pulses
def encode_bit_stream(bit_list):
    if (len(bit_list) % 2 > 0):
        bit_list.append('0')
    i = 0
    quad_arr = []
    while i < len(bit_list):
        symbol = (int(bit_list[i])<<1) + (int(bit_list[i+1]))
        quad_arr.append(symbol)
        i += 2
    return quad_arr

# Takes in a list of MSB-first QAM values and reconstructs a bit list
def decode_bit_stream(quad_arr):
    padded = False
    bit_list = []
    if (len(quad_arr) * 2) % 7 == 1:
        padded = True
    for symbol in quad_arr:
        bit_list += [symbol >> 1, symbol & 1]
    if padded:
        bit_list = bit_list[:-1]
    return bit_list

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
        gb_addr = ''.join(infile.readlines())
        gb_bits = tobits(gb_addr)
        print('bit length   : ' + str(len(gb_bits)))
        hamming_bits = hamming_encode(gb_bits).flatten()
        print('hamming(4,7) : ' + str(len(hamming_bits)))
        print('Ratio        : ' + str(len(gb_bits)/len(hamming_bits)))
        print('4/7          : ' + str(4/7))
        tx = encode_bit_stream(hamming_encode(tobits(gb_addr)).flatten())
        print('QAM symbols  : ' + str(len(tx)))
        tx_data = make_pulse(tx)
        arr1 = np.concatenate((np.zeros(50*pulse_length), noise_header4, header_pulse, tx_data, noise_footer5))
        signal = encode(arr1, fname)

        tx_o = tx[0:21]
        tx[5] = 0
        # tx = tx[0:21]
        # print(tx)
        rx = np.array(decode_bit_stream(tx)).flatten()
        rx_o = np.array(decode_bit_stream(tx_o)).flatten()
        # print('og',rx_o)
        # print('rx', rx)
        # # print(H.shape)
        # print(np.reshape(rx, (7,-1)).shape)
        errors = hamming_error_check(rx)
        # print('e', errors)
        err_tmp = calcerror(errors).flatten()
        # print(err_tmp)
        rx_corrected = hamming_correct(rx, err_tmp).flatten()
        # print('og',rx_o)
        # print('rx', rx)
        # print('co', rx_corrected)
        bits_decode = hamming_decode(rx).flatten()
        bits_decode_corr = hamming_decode(rx_corrected).flatten()
        print(frombits(bits_decode))
        print(frombits(bits_decode_corr))


        # expected = header + tx
        # print(expected)
        # print(len(expected))
        # print('num_samples:' + str(len(arr1)/pulse_length))


        # gb_addr = ''.join(infile.readlines())
        # print(gb_addr)
        # print(encode_string(gb_addr))
        # print(decode_string(encode_string(gb_addr)))

        # in_bits = [0, 1, 1, 0, 1, 0, 1]
        # print(in_bits)
        # print(encode_bit_stream(in_bits))
        # print(decode_bit_stream(encode_bit_stream(in_bits)))
