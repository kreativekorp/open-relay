#!/usr/bin/env bash
mkdir -p ../dev/safespace
cp KreativeSquare.sfd ../dev/safespace/KreativeSquare.bak
SFDPATCH="python ../openrelay-tools/tools/sfdpatch.py"
$SFDPATCH ../dev/safespace/KreativeSquare.bak -sp -s > KreativeSquare.sfd
