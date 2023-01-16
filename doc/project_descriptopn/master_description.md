# Introduction
On average, one hundred persons are killed by avalanches in Europe each year. In Norway alone, an average of nine persons succumb, and another 71 persons get injured from avalanches yearly. For an avalanche victim, time is of the absolute essence. If a rescuer finds the victim within 15 minutes of burial, the chances of survival are roughly $93\%$. However, afterward, the survival rate quickly drops to about $30\%$. 

When moving in avalanche-prone areas, it is a standard safety precaution for a person to be wearing an avalanche beacon. An avalanche beacon is a radio device that the user can switch between transmitting a signal and receiving a signal. 
When the user switches the beacon to receive mode, it will show a direction and distance estimate to the nearest beacon in transmit mode. When moving through avalanche terrain, users will always have the beacon set to transmit mode. If an avalanche accident occurs, the part of the group that is not buried will switch their receivers into receive mode and follow the direction shown on their beacons until they are within a couple of meters of the victim. The group will then proceed to probe the snow with a long pole in a circular motion until they hit the victim. When the victim is found, the group will start digging after the victim as quickly as possible.


# Problem statement
Even in the ideal case, where a beacon signal is found immediately, and the victim is buried close to the rescuers. The rescue process is physically demanding. Typically, the digging phase alone takes around five minutes per meter under the snow where the victim is buried. Therefore, any time saved during the search phase could mean the difference between survival and death. Furthermore, the problem increases in difficulty as the number of buried victims grows, and the number of rescuers decreases.

To decrease the time spent during the search phase of avalanche rescue, rescuers could use drones to conduct a course search of the avalanche and mark the potential victims. The drones will allow the rescuers to focus more on digging out the victim. For example, in the case of several burials, the drone could start searching for the next victim while the rescuers dig out the first victim.

# Master thesis goal
To develop such a drone, a module is needed to pick up the signal transmitted from an avalanche beacon and calculate the transmitter's direction and distance. Avalanche beacons transmits on a frequency of 457 khz. Therefore, an antenna that resonates on this frequency is needed. The signal from the antenna can be read through a software-defined radio, making it possible to do a fully digital analysis of the signal.

# Timeline
