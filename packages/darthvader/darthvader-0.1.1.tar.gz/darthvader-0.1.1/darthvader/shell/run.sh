#!/bin/bash

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
echo $SCRIPT_DIR
PARENT_DIR="$(dirname "$SCRIPT_DIR")"
echo $PARENT_DIR
CORE_DIR="$PARENT_DIR/core"


python3 "$CORE_DIR/anakin.py" 1
python3 "$CORE_DIR/leia.py" 2
python3 "$CORE_DIR/luke.py" 3