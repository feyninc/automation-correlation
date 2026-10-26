#!/bin/bash
# usage: run.sh <name> <overlay>... [-- pytest args]; builds base + overlays in /tmp/swdev-run/<name> and runs pytest
name=$1; shift; dst=/tmp/swdev-run/$name; rm -rf "$dst"; mkdir -p "$dst"; cp -r /tmp/swdev-repo/base/. "$dst"/
while [ $# -gt 0 ] && [ "$1" != "--" ]; do cp -r /tmp/swdev-repo/ov/$1/. "$dst"/; shift; done
[ "$1" == "--" ] && shift
cd "$dst" && TEST_DATABASE_URL="postgresql+psycopg://postgres:@/postgres?host=/tmp/swdev-pgdata" PYTHONPATH="$dst" /tmp/swdev-venv/bin/python -m pytest -q -p no:cacheprovider "$@" 2>&1 | tail -15
