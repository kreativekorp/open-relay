#!/usr/bin/env bash
mkdir -p ../dev/safespace
cp FairfaxHD.sfd ../dev/safespace/FairfaxHD.bak
cp FairfaxHDBold.sfd ../dev/safespace/FairfaxHDBold.bak
SFDPATCH="python ../openrelay-tools/tools/sfdpatch.py"
$SFDPATCH ../dev/safespace/FairfaxHD.bak -spr -s > FairfaxHD.sfd
$SFDPATCH ../dev/safespace/FairfaxHDBold.bak -spr -s > FairfaxHDBold.sfd
