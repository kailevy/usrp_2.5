numpy.savetxt('outfile.txt', numpy.column_stack([
    array1.view(float).reshape(-1, 2),
    array2.view(float).reshape(-1, 2),
]))

array1, array2 = numpy.loadtxt('outfile.txt', unpack=True).view(complex)
