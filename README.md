# scs_mfr
High-level scripts and command-line applications for South Coast Science environmental monitor manufacturing, test and calibration.

_Contains command line utilities and library classes._


**Required libraries:** 

* Third party: Adafruit_BBIO, tzlocal
* SCS root:  scs_core
* SCS host:  scs_host_bbe, scs_host_bbe_southern or scs_host_rpi
* SCS dfe:   scs_dfe_eng
* SCS NDIR:  scs_ndir_alphasense
* SCS PSU:   scs_psu


**Branches:**

The stable branch of this repository is master. For deployment purposes, use:

    git clone --branch=master https://github.com/south-coast-science/scs_mfr.git


**Example PYTHONPATH:**

Raspberry Pi, in /home/pi/.bashrc:

    export PYTHONPATH=~/SCS/scs_analysis/src:~/SCS/scs_dev/src:~/SCS/scs_osio/src:~/SCS/scs_mfr/src:~/SCS/scs_dfe_eng/src:~/SCS/scs_ndir_alphasense/src:~/SCS/scs_host_rpi/src:~/SCS/scs_core/src:$PYTHONPATH


BeagleBone, in /root/.bashrc:

    export PYTHONPATH=/home/debian/SCS/scs_dev/src:/home/debian/SCS/scs_osio/src:/home/debian/SCS/scs_mfr/src:/home/debian/SCS/scs_psu/src:/home/debian/SCS/scs_comms_ge910/src:/home/debian/SCS/scs_dfe_eng/src:/home/debian/SCS/scs_ndir_alphasense/src:/home/debian/SCS/scs_host_bbe/src:/home/debian/SCS/scs_core/src:$PYTHONPATH


BeagleBone, in /home/debian/.bashrc:

    export PYTHONPATH=~/SCS/scs_dev/src:~/SCS/scs_osio/src:~/SCS/scs_mfr/src:~/SCS/scs_psu/src:~/SCS/scs_comms_ge910/src:~/SCS/scs_dfe_eng/src:~/SCS/scs_ndir_alphasense/src:~/SCS/scs_host_bbe/src:~/SCS/scs_core/src:$PYTHONPATH


**Configuration workflow**

Part 1 of 3: Configuration:

    1: ./dfe_conf.py -v -s -p PT1000_ADDR
    2: ./sht_conf.py -v -i INT_ADDR -e EXT_ADDR
    3: ./ndir_conf.py -v -m MODEL -a AVERAGING_PERIOD
    4: ./opc_conf.py -v -m MODEL -s SAMPLE_PERIOD -p { 0 | 1 }
    5: ./psu_conf.py -v -m MODEL
    6: ./gps_conf.py -v -m MODEL
    7: ./schedule.py -v [{-s NAME INTERVAL COUNT | -c NAME }]


Part 2 of 3: Calibration:

    1: ./rtc.py -i -s -v 
    2: ./afe_calib -s AFE_SERIAL_NUMBER
    3: ./pt1000_calib.py -s -v
    4: ./afe_baseline.py -v -1 SN1_OFFSET -2 SN2_OFFSET -3 SN3_OFFSET -4 SN3_OFFSET


Part 3 of 3: Communication:

    1: ./host_id.py (may require superuser)
    2: ./system_id.py -d VENDOR_ID -m MODEL_ID -n MODEL_NAME -c CONFIG -s SYSTEM_SERIAL_NUMBER -v
    3: ./osio_api_auth.py -s ORG_ID API_KEY
    4: ./osio_client_auth.py.py -u USER_ID -l LAT LNG POSTCODE
    5: ./osio_host_project.py -v -s GROUP LOCATION_ID
    6: ./timezone.py -v -s ZONE

