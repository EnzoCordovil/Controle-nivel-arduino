# Electrical design

[English](ELECTRICAL_DESIGN.md) | [Português](../DIMENSIONAMENTO_ELETRICO.md)

This reference configuration completes the existing wiring diagram. Catalogue specifications and engineering allowances are identified separately. No assembled-unit measurements are claimed.

## Reference configuration

| Item | Selection or requirement |
|---|---|
| Controller | Arduino Uno R3, ATmega328P, 5 V logic |
| Sensors | Three DFRobot SEN0485 units, 5 V, less than 5 mA each, active-LOW outputs |
| Relay module | DFRobot DFR0017, active-HIGH input, COM/NO contacts |
| Valve | Adafruit 997, normally closed, 12 V DC, approximately 320 mA at 12 V |
| Converter | Pololu D24V10F5, regulated 5 V, up to 1 A typical output subject to thermal conditions |
| Supply | Isolated, regulated 12 V / 1 A, with current limiting and short-circuit protection |
| D1 | 1N4001 across the valve, cathode towards the positive terminal after NO |
| R1 | 10 kΩ, 1/4 W, between D7 and GND |
| F1 | Initial T750 mA choice, DC rated, with breaking capacity suitable for the supply |

The 997 valve needs at least 0.02 MPa differential pressure, approximately 3 psi, and permits flow in one direction. This selection assumes a pressurized inlet, not a low-head gravity supply. The 3–12 L/min inlet range must be established by the inlet hydraulics and checked on the assembly. This valve selection does not establish that range or the 0.3 s closure delay assumed in the model.

## Current budget

| 5 V load | Design current | Basis |
|---|---:|---|
| Uno without additional peripherals | 100 mA | Engineering allowance, not a measurement |
| Three sensors | 15 mA | Rounded upper allowance from manufacturer data |
| Energized relay module | 100 mA | Engineering allowance; confirm for the purchased revision |
| Total | 215 mA | Sum |

Converter output power is `5 × 0.215 = 1.075 W`. At an assumed 80% efficiency, input current is `1.075 / (12 × 0.80) = 0.112 A`. This assumed efficiency is consistent with the published typical range; it is not measured at this operating point. Adding 1 mA for converter housekeeping gives a 0.113 A input budget.

With the valve energized, the total supply budget is `0.320 + 0.113 = 0.433 A`, or 5.20 W. A 25% allowance raises this to 0.541 A, within the nominal 12 V / 1 A supply rating. The corresponding 5 V budget is 269 mA, within the converter's nominal rating. Temperature, tolerances and transient behavior still require checking.

## Wiring and protection

Use 0.50 mm² flexible copper for the 12 V supply and valve circuits, with up to 1 m one-way length. Use 0.20 mm² copper for 5 V distribution and signals, with up to 0.5 m one-way length per run. Cable insulation, connectors and installation conditions must suit the voltage and current.

At reference copper resistivity `0.0175 Ω·mm²/m`, the 12 V loop resistance is `2 × 1 × 0.0175 / 0.50 = 0.070 Ω`. The calculated drop at 0.433 A is 0.030 V. The corresponding 5 V loop drop at 0.215 A is approximately 0.019 V. These calculations exclude connector resistance and increased resistance with temperature. The sections are choices for short bench wiring, not universal ampacity ratings.

Place F1 immediately after the supply positive terminal, ahead of the branch split. T750 mA is the initial choice because it exceeds the 541 mA budget with margin. Confirm its time-current curve against startup current and the supply's short-circuit behavior. A current-limited supply might not deliver enough fault current to open this fuse promptly. No protection coordination or selectivity is claimed; source current limiting remains necessary.

R1 draws 0.5 mA and dissipates 2.5 mW when D7 is HIGH. D7 drives only the relay module input. It does not power either coil. Route valve return current directly to supply negative rather than through Arduino signal wiring.

Place D1 near the valve terminals. Adafruit recommends 1N4001 for this valve. A flyback diode can extend coil release time; measure hydraulic closure delay with the diode installed before treating the model's 0.3 s delay as a hardware characteristic. Check relay switching capability for the actual DC inductive load and module revision; a resistive contact rating alone does not establish that capability.

## Uno power connection

Power the Uno through a suitable USB power cable from the converter. Power sensors and the relay module in parallel from the converter distribution. Disconnect converter USB power before connecting computer USB. Never connect both sources simultaneously or apply 12 V to signals or the 5 V rail.

Read the drawing's generic sizing notes together with this reference configuration. The emergency input still shares the Arduino and relay with normal control; it is not an independent safety chain.

## Sources

- [DFRobot SEN0485](https://wiki.dfrobot.com/sen0485)
- [DFRobot DFR0017](https://wiki.dfrobot.com/dfr0017/)
- [Adafruit 997](https://www.adafruit.com/product/997)
- [Pololu D24V10F5](https://www.pololu.com/product/2831)

Current allowances, wire sections and F1 selection are explicit engineering decisions, not manufacturer certification of the complete assembly.
