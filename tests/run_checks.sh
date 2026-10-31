#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p build/evidence
{
  printf 'Software and hydraulic model verification\n'
  date -u +'%Y-%m-%dT%H:%M:%SZ'
  sha256sum ControleNivel/ControleNivel.ino
  g++ --version | head -n 1
  python3 --version
  g++ -std=c++11 -Wall -Wextra -Werror -fsanitize=undefined -Itests tests/test.cpp -o build/test_logic
  ./build/test_logic
  g++ -std=c++11 -Wall -Wextra -Werror -fsanitize=undefined -Itests tests/physical.cpp -o build/test_tank
  ./build/test_tank
  python3 tests/teste_geometria_exemplo.py
  python3 tests/teste_extravasor.py
} 2>&1 | tee build/evidence/simulation.txt
