# Engineering verification record

[English](ENGINEERING_VERIFICATION.md) | [Português](../VERIFICACAO_ENGENHARIA.md)

Tests executed on 31 October 2026 against firmware from commit `21d1c8ae3aee26a1c4d2b93eeb8f891d9f8d3a54`. The firmware was preserved.

SHA-256 of `ControleNivel/ControleNivel.ino`:

```text
500e459899a0b11b4aed3d9126d9acf1d363b688209859ccfe0785e8e7f47400
```

## Method and results

The sketch was compiled for host execution using simulated Arduino functions and EEPROM. The environment used g++ 13.3.0, C++11, warnings as errors and undefined-behavior sanitization. Python hydraulic calculations used Python 3.12.14.

| Verification | Observed result |
|---|---|
| State transitions, timeouts, noise, reset and simulated EEPROM | Assertions completed without failure |
| Startup and millis rollover | Assertions completed without failure |
| Dynamic tank model | 18 explicit scenarios and 210 operating combinations met their assertions |
| Ten complete cycles | Approximately 2.030 L maximum at 6 L/min |
| Upper sensor failure at 12 L/min | Emergency lockout; approximately 2.560 L maximum |
| Valve stuck open at 12 L/min with available overflow | Approximately 3.063 L equilibrium |
| Current geometry sensitivity | 50 combinations; approximately 3.217 L highest equilibrium |
| Separate historical-geometry analysis | 100 combinations; approximately 4.216 L highest equilibrium |

The historical combinations are not results for the current tank geometry. The 18 scenarios include known limitations: a lower sensor stuck wet prevents refilling without diagnosis; a stuck-open valve with blocked overflow exceeds the capacity limit. Passing these assertions means reproducing those limitations, not resolving them.

The reported 6 L in the last scenario is an extrapolated volume balance beyond the tank's geometric capacity. The model does not represent spilling over the rim. The relevant finding is capacity exceedance, not physical storage of 6 L in this tank.

## Reproduction and evidence

Run `bash tests/run_checks.sh` from the repository root. Output is saved to `build/evidence/simulation.txt`. The record for this revision is available at [../evidencias/simulacao.txt](../evidencias/simulacao.txt); it includes the source hash and environment.

The prepared workflow `.github/workflows/verify.yml` installs Arduino CLI 1.2.2 and Arduino AVR Boards 1.8.6 and runs:

```bash
arduino-cli compile --fqbn arduino:avr:uno --warnings all --output-dir build/uno ControleNivel
```

The [Engineering verification run](https://github.com/EnzoCastro-neko/controle-nivel-agua-arduino/actions/runs/41200581064), for commit `8169cd88a1f489e3e2310ccf8a2cd08cb6ddd415`, successfully completed Uno compilation, simulations and upload of the `engineering-evidence` artifact. The sketch uses 3,928 bytes of program storage (12%) and 387 bytes of static RAM (18%), leaving 1,661 bytes for local variables and stack. This is not a measured worst-case stack margin. The compiler reported four unused-parameter warnings in `new.cpp` from Arduino core 1.8.6; there were no compilation errors. The [compilation log](../evidencias/compilacao_uno.txt) is preserved in the repository. The run artifact contains binaries, logs and hashes and is subject to GitHub retention settings. The runner repeated the simulations using Python 3.12.3 and g++ 13.3.0 with the same reported results.

## Scope

These results support software and model behavior under the stated assumptions. They do not measure sensor operation, supply behavior, actual valve closure, leaks or physical discharge capacity. AVR compilation checks firmware compatibility and generation; it is not a physical test either. Identify computational results as simulation verification when using them in an academic report or portfolio.

The [electrical design](ELECTRICAL_DESIGN.md) adds the reference current budget, supply, converter, conductors and protection selection. Engineering allowances and remaining selection checks are stated explicitly.
