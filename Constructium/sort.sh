#!/usr/bin/env bash
mkdir -p ../dev/safespace
cp Constructium.sfd ../dev/safespace/Constructium.bak
SFDPATCH="python ../openrelay-tools/tools/sfdpatch.py"
$SFDPATCH ../dev/safespace/Constructium.bak -sp -s > Constructium.sfd
