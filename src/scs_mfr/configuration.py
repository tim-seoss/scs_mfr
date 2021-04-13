#!/usr/bin/env python3

"""
Created on 29 Jan 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The configuration utility is used to marshal all of the device configuration settings into a single JSON document.
It is intended to be used as one component of a centralised estate management system.

The utility can be used to update a setting on the device. To do this, a JSON document containing at least one field
of the configuration document must be supplied on the command line. Any fields that are not named will not be updated.

Note that the hostname field cannot be updated by the configuration utility. If this field is included in the
update JSON specification, it is silently ignored.

SYNOPSIS
configuration.py [-s CONFIGURATION] [-i INDENT] [-v]

EXAMPLES
./configuration.py -i4 -s '{"timezone-conf": {"name": "Europe/London"}}'

DOCUMENT EXAMPLE
{
    "rec": "2021-02-04T17:08:17Z",
    "tag": "scs-be2-3",
    "val": {
        "hostname": "scs-bbe-003",
        "git-pull": {
            "pulled-on": "2021-02-27T08:37:09Z",
            "success": true,
            "installed": [
                "scs_core",
                "scs_dev",
                "scs_dfe_eng",
                "scs_host_cpc",
                "scs_mfr",
                "scs_psu"
            ],
            "pulled": [
                "scs_core",
                "scs_dev",
                "scs_dfe_eng",
                "scs_host_cpc",
                "scs_mfr",
                "scs_psu"
            ],
            "excluded": []
        },
        "afe-baseline": {
            "sn1": {
                "calibrated-on": null,
                "offset": 0,
                "env": null
            },
            "sn2": {
                "calibrated-on": null,
                "offset": 0,
                "env": null
            },
            "sn3": {
                "calibrated-on": null,
                "offset": 0,
                "env": null
            },
            "sn4": {
                "calibrated-on": null,
                "offset": 0,
                "env": null
            }
        },
        "afe-calib": {
            "serial_number": "27-000001",
            "type": "810-0023-02",
            "calibrated_on": "2016-11-01",
            "dispatched_on": null,
            "pt1000_v20": 1.0,
            "sn1": {
                "serial_number": "212060308",
                "sensor_type": "NO2A43F",
                "we_electronic_zero_mv": 309,
                "we_sensor_zero_mv": 3,
                "we_total_zero_mv": 312,
                "ae_electronic_zero_mv": 308,
                "ae_sensor_zero_mv": 1,
                "ae_total_zero_mv": 309,
                "we_sensitivity_na_ppb": -0.264,
                "we_cross_sensitivity_no2_na_ppb": -0.264,
                "pcb_gain": -0.73,
                "we_sensitivity_mv_ppb": 0.192,
                "we_cross_sensitivity_no2_mv_ppb": 0.192
            },
            "sn2": {
                "serial_number": "132950202",
                "sensor_type": "CO A4",
                "we_electronic_zero_mv": 249,
                "we_sensor_zero_mv": 62,
                "we_total_zero_mv": 311,
                "ae_electronic_zero_mv": 253,
                "ae_sensor_zero_mv": -1,
                "ae_total_zero_mv": 252,
                "we_sensitivity_na_ppb": 0.299,
                "we_cross_sensitivity_no2_na_ppb": "n/a",
                "pcb_gain": 0.8,
                "we_sensitivity_mv_ppb": 0.239,
                "we_cross_sensitivity_no2_mv_ppb": "n/a"
            },
            "sn3": {
                "serial_number": "134060009",
                "sensor_type": "SO2A4",
                "we_electronic_zero_mv": 266,
                "we_sensor_zero_mv": -1,
                "we_total_zero_mv": 265,
                "ae_electronic_zero_mv": 263,
                "ae_sensor_zero_mv": 2,
                "ae_total_zero_mv": 265,
                "we_sensitivity_na_ppb": 0.444,
                "we_cross_sensitivity_no2_na_ppb": "n/a",
                "pcb_gain": 0.8,
                "we_sensitivity_mv_ppb": 0.355,
                "we_cross_sensitivity_no2_mv_ppb": "n/a"
            },
            "sn4": {
                "serial_number": "133910023",
                "sensor_type": "H2SA4",
                "we_electronic_zero_mv": 245,
                "we_sensor_zero_mv": -12,
                "we_total_zero_mv": 233,
                "ae_electronic_zero_mv": 251,
                "ae_sensor_zero_mv": 13,
                "ae_total_zero_mv": 264,
                "we_sensitivity_na_ppb": 1.782,
                "we_cross_sensitivity_no2_na_ppb": "n/a",
                "pcb_gain": 0.8,
                "we_sensitivity_mv_ppb": 1.425,
                "we_cross_sensitivity_no2_mv_ppb": "n/a"
            }
        },
        "aws-api-auth": {
            "endpoint": "aws.southcoastscience.com",
            "api-key": "de92c5ff-b47a-4cc4-a04c-62d684d64a1f"
        },
        "aws-client-auth": {
            "endpoint": "asrfh6e5j5ecz.iot.us-west-2.amazonaws.com",
            "client-id": "scs-bbe-003",
            "cert-id": "cd505d98bf"
        },
        "aws-group-config": {
            "group-name": "scs-bbe-003-group",
            "time-initiated": "2021-01-29T11:52:25Z",
            "unix-group": 987,
            "ml": true
        },
        "aws-project": {
            "location-path": "south-coast-science-dev/development/loc/1",
            "device-path": "south-coast-science-dev/development/device"
        },
        "csv-logger-conf": {
            "root-path": "/srv/removable_data_storage",
            "delete-oldest": true,
            "write-interval": 0
        },
        "display-conf": null,
        "gas-baseline": {
            "NO2": {
                "calibrated-on": "2021-01-19T13:42:55Z",
                "offset": -3,
                "env": {
                    "hmd": 40.9,
                    "tmp": 25.0,
                    "pA": null
                }
            }
        },
        "gas-model-conf": {
            "uds-path": "pipes/lambda-gas-model.uds",
            "model-interface": "vB",
            "resource-names": {
                "NO2": "/trained-models/no2-vB-2020q13/xgboost-model"
            }
        },
        "gps-conf": {
            "model": "SAM8Q",
            "sample-interval": 10,
            "tally": 60,
            "report-file": "/tmp/southcoastscience/gps_report.json",
            "debug": false
        },
        "interface-conf": {
            "model": "DFE"
        },
        "greengrass-identity": null,
        "mpl115a2-calib": {
            "calibrated-on": "2020-11-15T11:29:23Z",
            "c25": 510
        },
        "mpl115a2-conf": null,
        "mqtt-conf": {
            "inhibit-publishing": false,
            "report-file": null,
            "debug": false
        },
        "ndir-conf": {
            "model": "t1f1",
            "tally": 1,
            "raw": false
        },
        "opc-conf": {
            "model": "N3",
            "sample-period": 10,
            "restart-on-zeroes": false,
            "power-saving": false
        },
        "pmx-model-conf": {
            "uds-path": "pipes/lambda-pmx-model.uds",
            "model-interface": "s1",
            "resource-names": {
                "pm1": "/trained-models/pm1/xgboost-model",
                "pm2p5": "/trained-models/pm2p5/xgboost-model",
                "pm10": "/trained-models/pm10/xgboost-model"
            }
        },
        "psu-conf": {
            "model": "OsloV1",
            "batt-model": null,
            "ignore-threshold": false,
            "reporting-interval": 20,
            "report-file": "/tmp/southcoastscience/psu_status_report.json"
        },
        "pt1000-calib": {
            "calibrated-on": "2017-08-15T11:21:45Z",
            "v20": 0.320208
        },
        "scd30-conf": {
            "sample-interval": 5,
            "temp-offset": 0.0
        },
        "schedule": {
            "scs-climate": {
                "interval": 10.0,
                "tally": 1
            },
            "scs-gases": {
                "interval": 10.0,
                "tally": 1
            },
            "scs-particulates": {
                "interval": 10.0,
                "tally": 1
            },
            "scs-status": {
                "interval": 60.0,
                "tally": 1
            }
        },
        "shared-secret": {
            "key": "pYL7B1JcgJ2gy6MP"
        },
        "sht-conf": {
            "int": "0x45",
            "ext": "0x45"
        },
        "sim": {
            "imsi": "234301951432538",
            "iccid": "8944303382697124831",
            "operator-code": "23430",
            "operator-name": "EE"
        },
        "system-id": {
            "vendor-id": "SCS",
            "model-id": "BE2",
            "model": "Alpha BB Eng",
            "config": "V2",
            "system-sn": 3
        },
        "timezone-conf": {
            "set-on": "2021-01-31T11:26:14Z",
            "name": "Europe/London"
        }
    }
}
"""

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONify

from scs_core.estate.configuration import Configuration

from scs_core.sample.sample import Sample

from scs_core.sys.logging import Logging
from scs_core.sys.system_id import SystemID

from scs_dfe.interface.interface_conf import InterfaceConf

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_configuration import CmdConfiguration

from scs_psu.psu.psu_conf import PSUConf


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdConfiguration()

    # logging...
    Logging.config('configuration', verbose=cmd.verbose)
    logger = Logging.getLogger()

    logger.info(cmd)


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    system_id = SystemID.load(Host)

    if system_id is None:
        logger.error('SystemID not available.')
        exit(1)

    logger.info(system_id)

    interface_conf = InterfaceConf.load(Host)
    interface = None if interface_conf is None else interface_conf.interface()

    psu_conf = None if interface is None else PSUConf.load(Host)
    psu = None if psu_conf is None else psu_conf.psu(Host, interface)

    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.save():
        conf = Configuration.construct_from_jstr(cmd.configuration)

        if conf is None:
            logger.error('invalid configuration: %s' % cmd.configuration)
            exit(2)

        try:
            conf.save(Host)
        except ValueError as ex:
            logger.error(ex)
            exit(1)

    sample = Sample(system_id.message_tag(), LocalizedDatetime.now(), values=Configuration.load(Host, psu))
    print(JSONify.dumps(sample, indent=cmd.indent))
