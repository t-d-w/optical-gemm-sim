import matplotlib.pyplot as plt
import numpy as np

from simphony.libraries import siepic
from simphony.simulators import MonteCarloSweepSimulator, SweepSimulator
from simphony.simulation import Detector, DifferentialDetector, Laser, Simulation

#short=150e-6 - 3.220296627962994e-8
short=1e-3
print("short: ", short)

gc_input = siepic.GratingCoupler()
y_splitter = siepic.YBranch()
wg_long = siepic.Waveguide(length=150e-6)
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


#l = Laser(wl=1550e-9).powersweep(1e-3, 100e-3).connect(gc_input)
#Detector().connect(gc_output)
#data = sim.sample()
#with Simulation(seed=117) as sim:
with Simulation() as sim:
    l = Laser(wl=1550e-9).powersweep(1e-3, 100e-3).connect(gc_input)
    Detector().connect(gc_output)
    data = sim.sample()
   # print("data: ", data[])
    print("datlena: ", len(data[0]))
    power = np.linspace(1e-3, 100e-3, 500)
    slope = (data[0][499]-data[0][0])/(power[499]-power[0])
    print("Slope: ", slope)
    plt.plot(power, data[0])
    plt.show()
    #plt.plot()


'''
simulator.multiconnect(gc_input, gc_output)
Detector().connect(gc_output)
data = sim.sample()

f, p = simulator.simulate()
print("f[0]", f[0])
print("p[0]", p[0])
plt.plot(f, p)
plt.title("MZI")
plt.tight_layout()
plt.show()

'''
