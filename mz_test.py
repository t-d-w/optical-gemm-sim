import matplotlib.pyplot as plt
import numpy as np

from simphony.libraries import siepic
from simphony.simulators import MonteCarloSweepSimulator, SweepSimulator
from simphony.simulation import Detector, DifferentialDetector, Laser, Simulation


def mz_laser_ps(long, short):
    gc_input = siepic.GratingCoupler()
    y_splitter = siepic.YBranch()
    wg_long = siepic.Waveguide(long)
    wg_short = siepic.Waveguide(short)
    y_recombiner = siepic.YBranch()
    gc_output = siepic.GratingCoupler()

    # next we connect the components to each other
    # you can connect pins directly:
    y_splitter["pin1"].connect(gc_input["pin1"])

    # or connect components with components:
    # (when using components to make connections, their first unconnected pin will
    # be used to make the connection.)
    y_splitter.connect(wg_long)

    # or any combination of the two:
    y_splitter["pin3"].connect(wg_short)
    # y_splitter.connect(wg_short["pin1"])

    # when making multiple connections, it is often simpler to use `multiconnect`
    # multiconnect accepts components, pins, and None
    # if None is passed in, the corresponding pin is skipped
    y_recombiner.multiconnect(gc_output, wg_short, wg_long)
    with Simulation() as sim:
        #l = Laser(wl=1550e-9).powersweep(1e-3, 100e-3).connect(gc_input)
        Detector().connect(gc_output)
        data = sim.sample()
        # print("data: ", data[])
        return data

power_outs = []

i=0
dec = .25 # instead of increasing by 1, 1/4
N=30
plt.figure()
while i<N:
    long_in = 150e-6
    short_in = long_in - i*1550e-9 # this will determine the delta_L/lambda ratio to make the math easier
    #short_in=long_in
    #short_in = long_in - i
    data_out = mz_laser_ps(long_in, short_in)
    #str="small_factor="+i
    #print(str)
    #print("len(data): ", len(data_out[0]))
    power = np.linspace(1e-3, 100e-3, 500)
    slope = (data_out[0][499]-data_out[0][0])/(power[499]-power[0])
    power_outs.append(slope)
    print("Slope: ", slope)
   # str = str + " and slope = " + slope
    plt.plot(power, data_out[0])
    i+=dec

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

