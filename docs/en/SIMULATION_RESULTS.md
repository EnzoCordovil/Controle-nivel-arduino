# Simulation results: 200 × 125 × 230 mm tank

[English](SIMULATION_RESULTS.md) | [Português](../../RESULTADOS_SIMULACAO.md)

The model uses the example dimensions of 200 × 125 × 230 mm. The Arduino sketch retains the pin assignments, volume references, and 35-second timeouts. In `tests/physical.cpp`, the tank area above the overflow rim is 0.025 m². Sensor-height calculations use a pipe with a 50 mm internal diameter and a 54 mm external diameter, as described in the [calculation notes](GEOMETRY_AND_WIRING.md).

## Tests run on 31 October 2026

The tests were compiled as C++11 with `-Wall -Wextra -Werror -fsanitize=undefined`. The dynamic model also used `-O1`. Both executables and both Python tests exited with code zero. This run did not include AVR compilation or physical assembly tests.

| Check | Result |
|---|---|
| Logic, startup, filters, timeouts, simulated EEPROM, reset, and millis rollover | Implemented checks passed |
| 18 dynamic scenarios, including ten cycles | Expected results |
| 210 normal combinations of flow and initial volume | No unintended lockouts within the model assumptions |
| Normal operation at 6 L/min | Maximum 2.030 L |
| Upper sensor failure at 12 L/min, emergency input working | Maximum 2.560 L |
| Upper and emergency sensors stuck dry, working overflow | Maximum 3.063 L |
| Valve stuck open at 12 L/min, working overflow | Equilibrium approximately 3.063 L |
| 50 hydraulic combinations for the example geometry | Highest equilibrium 3.217 L at Cd=0.2 |
| Two historical geometries | 100 combinations; highest equilibrium 4.216 L |
| Valve stuck open and blocked overflow | Model exceeds 5 L; known limitation |
| Lower sensor stuck indicating water | No refilling or fault diagnosis; known limitation |

The historical values of 3.692 L and 4.216 L below belong to earlier geometries. Those tests remain available for comparison. For the current example, the calculated capacity to the rim is 5.468 L excluding flanges, and the calculation limit remains 5 L.

The model assumes discharge coefficients Cd, pipe discharge capacity of at least 18 L/min, a non-submerged outlet, and a 300 ms valve-closing delay. These are calculation assumptions without measurements from a physical assembly.

## Historical record of earlier geometries

### Procedure

The 35 s version was tested before the files were updated. The new-timeout test failed with the previous 65 s code and passed after the change. The .ino file ran as C++11 with simulated Arduino functions and EEPROM, -Wall -Wextra -Werror, and UndefinedBehaviorSanitizer. That run also excluded AVR compilation and physical testing.

The tests covered program logic, 18 dynamic scenarios, 210 combinations of flow and initial volume, ten complete cycles, and 100 hydraulic combinations. Each case produced its expected result. In limit tests, that result is the reproduction of a known failure, such as overflow over the tank rim with a stuck-open valve and blocked standpipe.

### Changes incorporated after testing

- Lower sensor at 1 L, upper sensor at 2 L, and emergency sensor at 2.5 L.
- Two 35 s timeouts (1 L at 2 L/min takes 30 s, plus a 5 s margin).
- An open vertical overflow standpipe with a reference internal diameter of 50 mm and rim at 2.8 L replaces the high circular opening in the wall.
- Pins D2/D3/D5, relay D7, reset button D4, and persistent lockout remain unchanged.

### Model and assumptions

The time step is 1 ms. Sensors switch ideally at the reference volumes, and the valve closes with an assumed delay of 300 ms. The minimum design net inflow is 2 L/min, with inlet flow from 3 to 12 L/min. The earlier model assumes 5 L at the tank rim, without confirmation for the commercial container.

Overflow follows a horizontal circular-crest model: `Q = (2/3) Cd pi D sqrt(2g) H^(3/2)`, capped at the assumed pipe discharge capacity of 18 L/min. The dynamic test uses Cd=0.4, with sensitivity checks from 0.2 to 0.6. The dynamic model uses the external footprint of 848.7 cm² as a scenario; sensitivity tests also examine an equivalent area of 438.6 cm². These are calculation geometries, not measured dimensions. Calibrate volumes with the pipe installed to account for its displacement.

As an order-of-magnitude check, Manning's equation gives approximately 21.15 L/min for a straight, half-full pipe with a 50 mm internal diameter, n=0.015, and 1% slope. A capacity of 18 L/min has not been demonstrated for the actual route. Bends, the bottom fitting, ventilation, outlet submergence, and obstructions require assessment. The model does not use a siphon and does not calculate wall stresses or the fit of the container's connections.

Conceptual references: [USACE HEC-HMS spillway equations](https://www.hec.usace.army.mil/confluence/hmsdocs/hmstrm/reservoir-modeling/reservoir-modeling-concepts-and-equations/spillways) and [USBR weir selection and low-head effects](https://www.usbr.gov/tsc/techreferences/mands/wmm/chap07_16.html). Applying these relationships at this scale uses assumed coefficients; the sources do not provide calibration for this assembly.

### Main historical results

| Test | Model result |
|---|---|
| Normal operation, 6 L/min | Normal cutoff; maximum 2.030 L |
| Normal operation, 3 L/min | Maximum 2.015 L; no unintended lockout |
| Inlet 3 L/min, withdrawal 1 L/min | Maximum 2.010 L; no lockout |
| Inlet 6 L/min, withdrawal 1 L/min for 10 min | Maximum 2.025 L; no lockout |
| Upper sensor stuck dry, 12 L/min | Emergency lockout; maximum 2.560 L |
| Lower and upper sensors stuck dry, working emergency input | Emergency lockout; maximum 2.560 L |
| Upper and emergency sensors stuck dry, 12 L/min, working overflow | Maximum 3.692 L; timeout lockout followed by drainage |
| Valve stuck open at 12 L/min, working overflow | Equilibrium approximately 3.692 L; command off and locked out |
| Ten complete cycles | Maximum 2.030 L |
| 210 normal combinations (3 to 12 L/min; initial volume 0 to 2 L) | No unintended lockouts; maxima below 2.07 L |
| Hydraulic sensitivity: 100 combinations | Highest calculated equilibrium 4.216 L at Cd=0.2 |
| Power cycle after stored fault and manual reset | Expected behavior |
| Input fluctuations, held button, and millis rollover | Expected behavior |

### Reproduced limitations

- A lower sensor stuck indicating water leaves an empty tank without refilling or an alarm. The higher sensors alone cannot identify this fault unambiguously.
- A stuck-open valve with a blocked overflow causes the model to exceed 5 L. Software cannot resolve this combination.
- Equilibrium volumes depend on the hydraulic assumptions. Changes to pipe capacity, geometry, actual rim volume, or coefficients can change the results.
- Simulated EEPROM writes are instantaneous and do not demonstrate tolerance to power loss during a write.

### Interpretation

The version passed the specified operating and protection scenarios within the model assumptions. The text and sketch were updated after those results. Installation, discharge capacity, sealing, actual dimensions, and power require checks during assembly; the simulations do not establish universal operation or physical approval.
