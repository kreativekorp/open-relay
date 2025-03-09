#!/usr/bin/env bash
mkdir -p ../dev/safespace
cp AlcoSans.sfd ../dev/safespace/AlcoSans.bak
SFDPATCH="python ../openrelay-tools/tools/sfdpatch.py"
$SFDPATCH ../dev/safespace/AlcoSans.bak -sp -s > AlcoSans.sfd
