#!/usr/bin/env bash
mkdir -p ../dev/safespace
cp FairfaxHD.sfd ../dev/safespace/FairfaxHD.bak
cp FairfaxHDBold.sfd ../dev/safespace/FairfaxHDBold.bak
python ../bin/sfdpatch.py ../dev/safespace/FairfaxHD.bak -sp -s > FairfaxHD.sfd
python ../bin/sfdpatch.py ../dev/safespace/FairfaxHDBold.bak -sp -s > FairfaxHDBold.sfd
