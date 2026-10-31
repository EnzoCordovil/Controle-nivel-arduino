# Water level controller assembly and configuration

[English](ASSEMBLY.md) | [Português](../../LEIAME.md)

Open `ControleNivel/ControleNivel.ino` in Arduino IDE and select Arduino Uno R3 (ATmega328P). EEPROM is included with Arduino AVR Boards; the sketch uses no external libraries.

## Pins and levels

| Function | Reference volume | Pin |
|---|---:|---|
| Start refilling | 1 L | D2 |
| Stop refilling | 2 L | D3 |
| Emergency shutdown and lockout | 2.5 L | D5 |
| Normally open momentary reset button | Not applicable | D4 to GND |
| Active-HIGH relay control | Not applicable | D7 |
| Fault LED | Not applicable | Built-in D13 |
| Overflow standpipe rim | 2.8 L | Passive hydraulic outlet |

SEN0485 sensors output LOW when they detect water. Connect the red wire to 5 V, black to GND, and green OUT to the Arduino input.

For the example tank with internal dimensions of 200 × 125 × 230 mm and a pipe external diameter of 54 mm, the calculated sensor heights are 44.0, 88.1, and 110.1 mm. The overflow rim is 123.3 mm above the internal floor. These dimensions were chosen for the example. During assembly, adjust positions using measured water volumes with the pipe installed, since it occupies space inside the tank.

The sensor has a 3 mm sensing distance. Check wall thickness, mounting, and possible interference. Use the tank's internal geometry and the space occupied by internal parts when calculating heights.

## Power and relay

The reference supply is an external isolated 12 V / 1 A unit and a converter with a regulated 5 V / 1 A output. The converter powers the Arduino through USB. The sensors and relay module receive 5 V in parallel, sharing a common control GND.

Connect a 10 kΩ resistor between D7 and GND. The 12 V valve is powered through the relay's COM and NO contacts, with its return connected to supply negative. Leave NC unconnected. Place the 1N4001 diode across the coil, with the band toward the positive terminal after NO.

Do not apply 12 V to signal pins, the 5V pin, or USB. Disconnect the converter's USB cable before connecting a computer. Size the supply, conductors, and overcurrent protection for the selected load, and check polarity before applying power.

## Program behavior

- During startup, the program keeps the relay off for at least 1 s and waits for stable sensor signals.
- Filling starts when the lower sensor is dry and stops when the upper sensor detects water. If the controller starts between these levels, it waits for the water to drop.
- The first timeout allows 35 s for the lower sensor to detect water. The second starts at that first confirmed detection and allows up to 35 s to reach the upper sensor. Lower-sensor fluctuations do not restart this timer.
- The raw upper-sensor input immediately interrupts the valve command. After 100 ms of confirmation, the program ends the cycle.
- The D5 emergency input immediately locks out the system, including during startup. It does not wait for the input filter. If electrical noise triggers it, inspect the cause before resetting.
- If the upper sensor indicates water while the lower sensor remains dry, confirmation of that combination triggers lockout.
- The button uses INPUT_PULLUP and a 40 ms filter. After a fault, release it and press it again. Reset requires stable, consistent sensor signals and an inactive emergency input.
- Lockout occupies EEPROM byte 0 and survives RESET or power loss. The write has no redundancy or protection against power interruption during writing.
- The Serial Monitor runs at 9600 baud.

## Timeouts and flow rates

Each stage has a 35 s timeout. Adding 1 L at a net inflow of 2 L/min takes 30 s; the remaining 5 s are the selected margin. Calculations use inlet flows from 3 to 12 L/min.

If water is withdrawn during filling, net inflow must remain at least 2 L/min. Below this rate, the controller may time out even with working sensors. The previous 65 s timeout was replaced with this 35 s setting.

## Overflow standpipe

The overflow is an open vertical standpipe with a reference internal diameter of 50 mm and its rim at the 2.8 L level. Check the selected product's internal diameter; its nominal DN size alone does not define that measurement.

The discharge passes through a sealed bottom fitting and continues to a disposal point below the tank. The base must leave clearance for the fitting. Keep the route short and descending, with a reference minimum slope of 1% in horizontal runs and a total elevation difference of up to 1 m.

Keep the outlet free, visible, and vented. Avoid shutoff valves, siphons, kinked hoses, submerged outlets, and direct sealed connections to a sewer. Check fit, sealing, and bottom-fitting support before drilling.

The model assumes a free rim and pipe discharge capacity of at least 18 L/min. Manning's equation gives approximately 21.15 L/min for a straight, half-full pipe with a 50 mm internal diameter, n=0.015, and 1% slope. This calculation excludes local losses at bends, the inlet, and fittings. The 18 L/min value is a simulation assumption; the assembly's capacity depends on sizing and testing the complete route.

## Limitations

If the lower sensor sticks in the water-detected state, the tank may receive no refill and no alarm. The third sensor shares the Arduino and relay with the other sensors, so it is not an independent safety circuit. If the valve sticks open, water removal depends on the overflow; obstruction or insufficient capacity can cause overflow over the tank rim.

The pipe takes up volume and must fit alongside fittings, supports, and sensors. Internal dimensions, rim capacity, and low-head discharge coefficients have not been measured in a physical assembly. The same applies to actual response delays and power-supply behavior with temperature.

## Repeat the simulations

Run from the repository root:

```bash
g++ -std=c++11 -Wall -Wextra -Werror -Itests tests/test.cpp -o teste_logica
./teste_logica
g++ -std=c++11 -Wall -Wextra -Werror -Itests tests/physical.cpp -o teste_tanque
./teste_tanque
python3 tests/teste_extravasor.py
python3 tests/teste_geometria_exemplo.py
```

Read the [project description](PROJECT.md) and [simulation results](SIMULATION_RESULTS.md). AVR compilation for Arduino Uno completed successfully in [GitHub Actions](https://github.com/EnzoCastro-neko/controle-nivel-agua-arduino/actions/runs/41200581064). Physical testing has not been performed.

The [electrical diagram and calculation notes](GEOMETRY_AND_WIRING.md) provide the connection details. Check terminal labels on the selected hardware during assembly.

## Electrical reference configuration

See [ELECTRICAL_DESIGN.md](ELECTRICAL_DESIGN.md) for valve, supply, converter, conductor and F1 selection, including the current budget and application conditions.
