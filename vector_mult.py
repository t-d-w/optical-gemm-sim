import matplotlib.pyplot as plt
import numpy as np

from simphony.libraries import siepic
from simphony.simulators import MonteCarloSweepSimulator, SweepSimulator
from simphony.simulation import Detector, DifferentialDetector, Laser, Simulation


def mz_laser_ps(long, short):
    gc_input1 = siepic.GratingCoupler()
    gc_input2 = siepic.GratingCoupler()

    dc_1 = siepic.DirectionalCoupler()
    wg_long = siepic.Waveguide(long)
    wg_short = siepic.Waveguide(short)
    dc_2 = siepic.DirectionalCoupler()
    gc_output1 = siepic.GratingCoupler()
    gc_output2 = siepic.GratingCoupler()

    # next we connect the components to each other
    # you can connect pins directly:
    #y_splitter["pin1"].connect(gc_input["pin1"])

    #wg_long.multiconnect(gc_input, dc_1["pin1"])
    #wg_short.multiconnect(in2, dc1)
    dc_1["pin1"].connect(gc_input1["pin1"])
    dc_1["pin2"].connect(gc_input2["pin2"])

    # or connect components with components:
    # (when using components to make connections, their first unconnected pin will
    # be used to make the connection.)
    #y_splitter.connect(wg_long)
    dc_1["pin3"].connect(wg_long)
    dc_1["pin4"].connect(wg_short)

    # or any combination of the two:
    #y_splitter["pin3"].connect(wg_short)
    # y_splitter.connect(wg_short["pin1"])

    # when making multiple connections, it is often simpler to use `multiconnect`
    # multiconnect accepts components, pins, and None
    # if None is passed in, the corresponding pin is skipped
    #y_recombiner.multiconnect(gc_output, wg_short, wg_long)

    # next we connect the components to each other
    # you can connect pins directly:
    #y_splitter["pin1"].connect(gc_input["pin1"])
    dc_2["pin1"].connect(wg_long)
    dc_2["pin2"].connect(wg_short)

    # or connect components with components:
    # (when using components to make connections, their first unconnected pin will
    # be used to make the connection.)
    #y_splitter.connect(wg_long)
    dc_2["pin3"].connect(wg_long)
    dc_2["pin4"].connect(wg_short)

    with Simulation() as sim:
        l = Laser(wl=1550e-9).powersweep(1e-3, 100e-3).connect(gc_input1)
        l2 = Laser(wl=1550e-9).powersweep(1e-3, 100e-3).connect(gc_input2)
        #Detector().connect(gc_input1)
        Detector().multiconnect(gc_output1, gc_output2)
        Detector()
        data = sim.sample()
        # print("data: ", data[])

        with Simulation() as sim2:
            
        
        return data

power_outs = []

i=0
dec = 1 # instead of increasing by 1, 1/4
N=400
plt.figure()
max=0
while i<N:
    long_in = 150e-6
    if i==0:
        short_in=long_in - 1550e-9
    else :
        short_in = long_in - i*(1/300)*1550e-9 # this will determine the delta_L/lambda ratio to make the math easier
    #short_in = long_in-i*1550e-9
    #short_in=long_in
    #short_in = long_in - i*1550e-9
    # path_length_difference/lambda = i
    data_out = mz_laser_ps(long_in, short_in)
    #str="small_factor="+i
    #print(str)
    #print("len(data): ", len(data_out[0]))
    power = np.linspace(1e-3, 100e-3, 500)
    slope = (data_out[0][499]-data_out[0][0])/(power[499]-power[0])/.3035
    # .0000 = 0 
    # 1.0000 = 1 
    if(slope>max):
        max=slope
        #print("")
    power_outs.append(slope)
    print("Slope: ", slope)
   # str = str + " and slope = " + slope
    plt.plot(power, data_out[0])
    i+=dec

print(max)

plt.title("Input vs. Output power for integer values of delta_L/lambda (including half integer)")
plt.show()

n_s = np.linspace(0, N-dec, int((1/dec))*N)
plt.figure(2)
plt.plot(n_s, power_outs)
plt.title("power scale vs. integer value of delta_L/lambda (including half integer)")
plt.show()

plt.figure(3)
plt.plot(n_s, np.sqrt(power_outs))
plt.title("amplitude scale vs. integer value of delta_L/lambda (including half integer)")
plt.show()
