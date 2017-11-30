# ADC Final Project Fall 2017

## USRP setup instructions

Make sure gnu-radio is installed:
```
$ sudo apt install gnuradio
```

Install USRP libraries:
```
$ sudo apt install libuhd-dev libuhd003 uhd-host
```

Run USRP setup script:
```
$ sudo /usr/lib/uhd/utils/uhd_images_downloader.py
```

You should then be able to see a connected uhd device by running:
```
$ uhd_find_devices
```

Note that if GRC is running, you may not be able to see the connected device.



