# Automatic water level control project

[English](PROJECT.md) | [Português](../../DESCRICAO_PROJETO.md)

The system controls filling in a transparent rectangular tank. The example uses internal dimensions of 20 × 12.5 × 23 cm. With the overflow standpipe installed, the calculated volume up to the rim is approximately 5.47 L, excluding flanges and other fittings. The calculations use a 5 L limit to leave a margin below the rim.

Water flows from a tap through a normally closed 12 V DC solenoid valve and enters the tank through a side connection near the base.

Three capacitive sensors mounted outside the tank send level signals to an Arduino Uno. Refilling starts when the water drops below the 1 L sensor and stops when it reaches the 2 L sensor. The third sensor is positioned at the 2.5 L reference and triggers emergency shutdown and lockout. During assembly, set the positions using water volumes measured with all internal hydraulic components installed.

The reference power supply is an external, isolated, regulated 12 V / 1 A unit. A converter provides 5 V for the sensors, relay module, and Arduino USB power input. The valve receives 12 V through the relay's COM and NO contacts. A 1N4001 diode connected across the coil limits the voltage spike when the valve is switched off. A 10 kΩ resistor between the control signal and GND keeps the relay off during startup.

The program checks the inputs before allowing filling. It uses two 35-second timeouts: from opening the valve until the lower sensor detects water, and from that detection until the upper sensor detects water. Each stage adds approximately 1 L. At a net inflow of 2 L/min, this takes 30 seconds, leaving a 5-second margin. Level-based shutdown takes priority over the timeouts.

The system locks out filling if a timeout expires, the sensor signals are inconsistent, or the emergency input is activated. EEPROM retains the lockout after power is disconnected. The manual reset button allows the program to check the sensors again; the valve command is enabled only when the filling conditions are met.

The overflow uses an open vertical standpipe inside the tank, with a reference internal diameter of 50 mm and its rim at the 2.8 L level. Excess water flows over the rim and through a sealed bottom fitting to a free, visible discharge outlet without a shutoff valve. The base leaves clearance for the fitting. The tank and discharge path remain vented, and the design does not rely on siphoning.

The discharge pipe follows a short descending route without reverse slopes. The reference minimum slope is 1% in horizontal runs, with the disposal point below the tank and a total elevation difference of up to 1 m. The base and supports must carry the pipework without transferring its weight to the plastic tank wall.

A separate manual drain near the base allows the tank to be emptied or water to be transferred. It is not part of the electronic control, but using it affects net inflow during filling.

The simulations reproduced filling cycles and the protections implemented in the program. For inlet flows up to 12 L/min, the hydraulic model calculated equilibrium below 5 L. The [report](SIMULATION_RESULTS.md) records flow assumptions, results, and faults the controller can detect. These are software tests and hydraulic calculations; they do not include measurements from a physical assembly.

The [geometry and wiring notes](GEOMETRY_AND_WIRING.md) include the 3D view, sensor heights, and electrical diagram.
