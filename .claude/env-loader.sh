#!/bin/bash
# Load environment variables from .env.local
# Usage: source this file or use: export $(grep -E "^[A-Z]" "$NEURON_ROOT/.env.local" | xargs)

NEURON_ROOT="${NEURON_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"

if [ -f "$NEURON_ROOT/.env.local" ]; then
    export $(grep -E "^[A-Z_]+=" "$NEURON_ROOT/.env.local" | xargs)
fi
