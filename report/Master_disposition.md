# Abstract
# Introduction
## Avalanche dynamics
- Loose snow avalanches
- Slab avalanches

## Avalanche Beacons
- History
- Usage

## Avalanche search and rescue today
- Companion rescue
- Proffesional rescue

## Problem statement
- People die
    - Despite advancement of the tech many people still die.
- Problem when avalanche beacon run out of power
    - Refrence to avalanche report of skittentind and blåbærfjellet
- Need a beacon that can collect signal data digitally and store the data
- Should be small enough so that it can be fitted on a drone

# Backgorund(Theoretical framework)
## Understanding the functionality of modern avalanche beacons
- Flux lines
- Magnetic field
- AM-radio
- Direction estimation  
- Distance estimation

## Digital Signal processing
- I/Q data
- Frequency domain
- Fourier transform
    -DFT
    -FFT

## SDR
- Decimation
- Linear low noise amplifier

## Antenna design
- Dipole antenna
- Ferrite core antenna
    - Low frequency
    - Directivity
    - Equations to calculate inductance and capacitance
    
## 3D printing
## Raspberry PI(?)
## Related work
    - Harvard drone
        - Mostly hardware
        - Successfull testing
    - Uppsala drone
        - SDR's
        - One antenna
        - Low range
        - Little knowledge of radio wave propagation

# Material and methods
## Development strategy
- Versioning
    - Create a prototype
    - Test it
    - Discover problems
    - Fix problems
    - Test it
    - ...

## Choice of SDR
- Airspy HF+
- Other choices
    - USRP
    - Pros
        - High sampling rate, High sampling resolution, very configurable with own cards, mutliple inputs
    - Cons
        - Expensive, large, needs own powersupply, not open source, little used in the community
    - RTL-SDR
    - Pros
        - Small, USB driven, open source, good doc, cheap
    - Cons
        - Poor sampling resolution(8 bit)
        -Created for higher frequencies
        - Varies from module to module
            - Usally from a couple of hundreds MHz to couple of thousands MHz.
    - Airspy HF+
    - Pros
        - Cheap(around 1000Nok)
        - OK sampling res(16 bit)
        - Small
        - Open source
    - Cons
        - Sampling res could be higher
        - Poor documentation
        - Unfinished libraries
    - Pluto SDR
    - Pros
        - Created for education
        - Easy to use
        - Two antenna inputs
        - Lots of prewritten libraries
        - Python, C, C++
    - Cons
        - Expensive
        - Created for higher frequency range
        
## How to do measurments
- Raspberry Pi
    - With powerbank
    - Write raw signal data to file
    - Do analysis in retrospect
- Two SDRs

# Version 1
## Implementation and design
- Passive antenna
    - 20, 50, 100 turns
    - Calculations on inductance
    - Find capacitance
- System design
    - Laptop
    - Two airspys
    - Taped to cardboard
## Evaluation
- Test environemnt
    - Office
    - Got approximate range of 8 meter
    - Tested only 5
## Problems
- Difficult to do tests
- Test environment with much radio interference(?)
    - Do measurements of noise floor
## Version 1.5
- Hypothesis: Increase in indcutance should improve signal quality
- Increase inductance
    - Create coil of 300 turns
    - Result:
    - Inductance increased
    - Problem
        - The increase in inductance made the needed capacitance too small
        - Creep capacitance in the circuit made it hard to reach the correct resonance frequency
# Version 2
## Active antenna
 - Show Diagram

## System design
- 3D print frame
- Use RPi to collect data
## Evaluation
- Test 1 with mammut element
    - New test environment
    - Outside
    - Less radio interference(?)
- Test 2 with mammut barrywox S
    - Hopfully better
## Problems
- Test with mammut element
    - Avalanche beacon transmited on wrong frequency
- Still low range compared to state of the art avalanche beacons.
    - Hypothesis, noise from RPi?

# Evaluation
- Test grid search with single avalanche beacon
    - Estimate direction and calculate H
- Test grid with multiple avalanche becons
    - Plot H field over the grid
    - Hopefully, get hotspots over the beacon

# Discussion / Future work
- Discuss results from last section
## Future work
- Improve antenna reception
- Match radio data to GPS data
- Product reasearch
    - Who will be the users of this product
    - How should the product be created for the users

# Conclusion / Summary of project
- Proof of concept works
    - No large problems
    - Some improvements are needed
