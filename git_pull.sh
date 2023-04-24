#!/usr/bin/env bash

# DEPRECATED. Replaced by https://github.com/south-coast-science/scs_mfr/wiki/git_pull

# copy this file to the ~/SCS directory and edit as required...

GIT_PATH=~/SCS/scs_airnow/                  # comment out if the package is not installed
echo ${GIT_PATH}
git -C ${GIT_PATH} pull
echo '-'

GIT_PATH=~/SCS/scs_analysis/                # comment out if the package is not installed
echo ${GIT_PATH}
git -C ${GIT_PATH} pull
echo '-'

GIT_PATH=~/SCS/scs_comms_ge910/             # comment out if the package is not installed
echo ${GIT_PATH}
git -C ${GIT_PATH} pull
echo '-'

GIT_PATH=~/SCS/scs_core/                    # comment out if the package is not installed
echo ${GIT_PATH}
git -C ${GIT_PATH} pull
echo '-'

GIT_PATH=~/SCS/scs_dev/                     # comment out if the package is not installed
echo ${GIT_PATH}
git -C ${GIT_PATH} pull
echo '-'

GIT_PATH=~/SCS/scs_dfe_eng/                 # comment out if the package is not installed
echo ${GIT_PATH}
git -C ${GIT_PATH} pull
echo '-'

GIT_PATH=~/SCS/scs_display_inky/            # comment out if the package is not installed
echo ${GIT_PATH}
git -C ${GIT_PATH} pull
echo '-'

GIT_PATH=~/SCS/scs_host_bbe_southern/       # replace with the appropriate host package, as necessary
echo ${GIT_PATH}
git -C ${GIT_PATH} pull
echo '-'

GIT_PATH=~/SCS/scs_mfr/                     # comment out if the package is not installed
echo ${GIT_PATH}
git -C ${GIT_PATH} pull
echo '-'

GIT_PATH=~/SCS/scs_ndir/                    # comment out if the package is not installed
echo ${GIT_PATH}
git -C ${GIT_PATH} pull
echo '-'

GIT_PATH=~/SCS/scs_philips_hue/             # comment out if the package is not installed
echo ${GIT_PATH}
git -C ${GIT_PATH} pull
echo '-'

GIT_PATH=~/SCS/scs_psu/                    # comment out if the package is not installed
echo ${GIT_PATH}
git -C ${GIT_PATH} pull
echo '-'

date +%y-%m-%d > ~/SCS/latest_update.txt
