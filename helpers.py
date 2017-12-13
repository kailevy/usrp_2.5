def first_trim(signal, numbins=100):
    bin_length = len(signal)//numbins
    bins = np.array_split(signal, numbins)
    maxes = np.array([arr.max() for arr in bins])
    avg_max = maxes.mean()
    i = 0
    while maxes[i] < avg_max:
        i+=1
    j = -1
    while maxes[j] < avg_max:
        j-=1
    return ((i-1)*bin_length,(j+1)*bin_length)

def phaseCapture(signal):
    phase_captured = []
    phase_offset_t = []
    phase_offset = 0
    corrected_sample = 0
    avg_mag = np.mean([np.absolute(p) for p in signal])
    
    for point in signal:
        if np.absolute(point) > 0.25 * avg_mag:
            # apply previous correction factor
            corrected_sample = point * np.exp(-1j*phase_offset)

            received_angle = np.angle(corrected_sample) # range from -pi to pi
            received_angle += 2 * np.pi # Correct to range of 0 to 2 pi

            #calculate multiples of pi/2 the received was offset from 0
            num_quadrants = np.floor((received_angle + np.pi / 4) / (np.pi / 2) )
            original_angle = np.pi * num_quadrants / 2

            #calculate received angle offset from intended angle
            measured_offset = received_angle - original_angle
            
        # add forgetting factor
        phase_offset = phase_offset + 0.5 * measured_offset
        
        # wrap phase_offset from 0 to -2 pi
        while (phase_offset > 2 * np.pi):
            phase_offset = phase_offset - 2 * np.pi
        while (phase_offset < 0):
            phase_offset = phase_offset + 2 * np.pi

        #apply final correction factor and output
        phase_captured.append(point * np.exp(-1j*phase_offset))
        phase_offset_t.append(phase_offset)
    
    return phase_captured, phase_offset_t

def sample(signal, offset=40, bucket=20, period=100):
    length = len(signal)
    num_pads = int(period * np.ceil(length/period))-length
#     pads = (int(np.floor(num_pads/2)), int(np.ceil(num_pads/2)))
    signal_padded = np.pad(signal, (0,num_pads), 'constant', constant_values=np.NaN)
    signal_reshaped = np.reshape(signal_padded, (-1, period))
    signal_sliced = signal_reshaped[:, range(offset, offset+bucket+1)]
    signal_mean = np.nanmean(signal_sliced, axis=1)
    return signal_mean

def parse(signal, threshold=0.05):
    for sample in signal:
        if np.absolute(np.real(sample))+np.absolute(np.imag(sample)) < threshold:
            yield(-1)
            continue
        if np.real(sample) < 0:
            if np.imag(sample) < 0:
                yield(0)
            else:
                yield(1)
        else:
            if np.imag(sample) < 0:
                yield(2)
            else:
                yield(3)

def autoTrim(raw_signal, header, footer):
    signal = approxPhaseCorrect(raw_signal)
    header_corr = np.correlate(signal, header, mode="valid")
    footer_corr = np.correlate(signal, footer, mode="valid")
    start_time = np.argmax(np.absolute(header_corr))
    end_time = np.argmax(np.absolute(footer_corr))
    trimmed = signal[start_time+len(header)-500:end_time]
    
    #     plt.figure(figsize=(15,8))
    #     plt.subplot(411)
    #     plt.plot(np.real(signal))
    #     plt.subplot(412)
    #     plt.plot(np.real(header_corr))
    #     plt.subplot(413)
    #     plt.plot(np.real(footer_corr))
    #     plt.subplot(414)
    #     plt.plot(trimmed)

    #     print("start: {}".format(start_time))
    #     print("end: {}".format(end_time))
    
    return trimmed

def argand(signal):
    """Plots an argand diagram of a complex signal"""
    plt.plot(np.real(signal),np.imag(signal), marker='.',linestyle='')
    
def fullPlot(signal):
    """Plots an argand diagram of a complex signal, along with the real and complex components in time"""
    plt.figure(figsize=(15,5))
    plt.subplot(131)
    argand(signal)
    
    plt.subplot(132)
    plt.plot(np.real(signal))
    
    plt.subplot(133)
    plt.plot(np.imag(signal))
    
    plt.show()

def approxPhaseCorrect(raw_sig,rate=22050,verbose=False):
    """Applies a approximate phase correction to a complex signal, returning the corrected signal"""
    duration = len(raw_sig)
    freq_data = np.fft.fftshift(np.fft.fft(raw_sig**4))
    rad_axis= np.linspace(-np.pi, np.pi*(duration-1)/duration, len(freq_data))
    if verbose:
        pass
    peak = np.argmax(freq_data)
    print(freq_data[peak])
    offset = rad_axis[peak]/4
    correction = -np.exp(-1j*np.linspace(0,duration-1,duration)*offset)
    return raw_sig*correction*freq_data[peak]

def generate_white_noise(seed=None):
    mean = 0
    std = 1
    num_samples = 5000
    np.random.seed(seed)
    samples = np.random.normal(mean, std, size=num_samples)
    header=samples + (1j * samples)
    return header

def phaseCapture2(signal):
    captured = np.zeros(len(signal), dtype='complex64')
    phase_offset_t = np.zeros(len(signal), dtype='complex64')
    freq_t = np.zeros(len(signal), dtype='complex64')
    phase_offset = 0
    freq = 0
    corrected_sample = 0
    signal = signal/np.std(signal)
    avg_mag = np.mean([np.absolute(p) for p in signal])
    
    for n,point in enumerate(signal):
        if np.absolute(point) > 0.25 * avg_mag:
            # apply previous correction factor
            nco = np.exp(-phase_offset*1j)
            corrected_sample = point * nco

            measured_offset = np.sign(np.real(corrected_sample))*np.imag(corrected_sample)-np.sign(np.imag(corrected_sample))*np.real(corrected_sample)
            
            
        
            # add forgetting factor
            freq = freq + 0.005 * measured_offset
            phase_offset = phase_offset + 0.05 * measured_offset + freq

            # wrap phase_offset from 0 to -2 pi
            while (phase_offset > np.pi):
                phase_offset = phase_offset - 2 * np.pi
            while (phase_offset < -np.pi):
                phase_offset = phase_offset + 2 * np.pi
            while (freq > np.pi):
                freq = freq - 2 * np.pi
            while (freq < -np.pi):
                freq = freq + 2 * np.pi

            # apply final correction factor and output
            captured[n] = corrected_sample
            phase_offset_t[n] = phase_offset
            freq_t[n] = freq
        
        else:
            captured[n] = point
        
    
    return captured, phase_offset_t, freq_t