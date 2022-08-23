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
configuration.py [-s CONFIGURATION] [{ -i INDENT | -t }] [-v]

EXAMPLES
./configuration.py -i4 -s '{"timezone-conf": {"name": "Europe/London"}}'

DOCUMENT EXAMPLE
{
    "rec": "2022-03-21T11:51:46Z",
    "tag": "scs-be2-3",
    "ver": 1.0,
    "val": {
        "hostname": "scs-bbe-003",
        "packs": {
            "scs_comms": {
                "repo": "scs_comms_ge910",
                "version": null
            },
            "scs_core": {
                "repo": "scs_core",
                "version": "1.1.18"
            },
            "scs_dev": {
                "repo": "scs_dev",
                "version": "1.1.10"
            },
            "scs_dfe": {
                "repo": "scs_dfe_eng",
                "version": "1.1.4"
            },
            "scs_exegesis": {
                "repo": "scs_exegesis",
                "version": null
            },
            "scs_greengrass": {
                "repo": "scs_greengrass",
                "version": "2.1.9"
            },
            "scs_host": {
                "repo": "scs_host_bbe_southern",
                "version": "1.0.10"
            },
            "scs_inference": {
                "repo": "scs_inference",
                "version": null
            },
            "scs_mfr": {
                "repo": "scs_mfr",
                "version": "1.1.14"
            },
            "scs_ndir": {
                "repo": "scs_ndir",
                "version": null
            },
            "scs_psu": {
                "repo": "scs_psu",
                "version": "1.0.10"
            }
        },
        "afe-baseline": {
            "sn1": {
                "calibrated-on": "2022-03-21T11:46:43Z",
                "offset": -1,
                "env": {
                    "rec": "2022-03-16T07:45:00Z",
                    "hmd": 51.6,
                    "tmp": 21.8
                }
            },
            "sn2": {
                "calibrated-on": "2022-03-21T11:46:48Z",
                "offset": 44,
                "env": {
                    "rec": "2022-03-16T06:15:00Z",
                    "hmd": 48.1,
                    "tmp": 22.0
                }
            },
            "sn3": {
                "calibrated-on": null,
                "offset": 0,
                "env": null
            },
            "sn4": {
                "calibrated-on": "2022-03-21T11:46:37Z",
                "offset": 174,
                "env": {
                    "rec": "2022-03-16T06:30:00Z",
                    "hmd": 48.2,
                    "tmp": 21.9
                }
            }
        },
        "afe-id": {
            "serial_number": "26-000063",
            "type": "810-0023",
            "calibrated_on": "2017-04-27",
            "sn1": {
                "serial_number": "212560016",
                "sensor_type": "NO2A43F"
            },
            "sn2": {
                "serial_number": "214690108",
                "sensor_type": "OXA431"
            },
            "sn3": null,
            "sn4": {
                "serial_number": "132930028",
                "sensor_type": "CO A4"
            }
        },
        "aws-api-auth": {
            "endpoint": "aws.southcoastscience.com",
            "api-key": "south-coast-science-dev"
        },
        "aws-group-config": {
            "group-name": "scs-bbe-003-group",
            "time-initiated": "2022-03-08T11:30:36Z",
            "unix-group": 987,
            "ml": "uE.1"
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
        "vcal-baseline": {
            "NO2": {
                "calibrated-on": "2022-03-21T11:46:45Z",
                "offset": -31,
                "env": {
                    "rec": "2022-03-16T05:10:00Z",
                    "hmd": 48.3,
                    "tmp": 22.4
                }
            }
        },
        "gas-baseline": null,
        "gas-model-conf": {
            "uds-path": "pipes/lambda-gas-model.uds",
            "model-interface": "vE",
            "model-compendium-group": "uE.1"
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
        "greengrass-identity": {
            "core-name": "scs-bbe-003-core",
            "group-name": "scs-bbe-003-group"
        },
        "mpl115a2-calib": {
            "calibrated-on": "2020-11-15T11:29:23Z",
            "c25": 510
        },
        "mqtt-conf": {
            "inhibit-publishing": true,
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
            "restart-on-zeroes": true,
            "power-saving": false
        },
        "opc-version": {
            "serial": "177510317",
            "firmware": "OPC-N3 Iss1.1 FirmwareVer=1.17a...........................BS"
        },
        "pmx-model-conf": {
            "uds-path": "pipes/lambda-pmx-model.uds",
            "model-interface": "s2"
        },
        "pressure-conf": {
            "model": "ICP",
            "altitude": 101
        },
        "psu-conf": {
            "model": "OsloV1",
            "batt-model": null,
            "ignore-threshold": false,
            "reporting-interval": 20,
            "report-file": "/tmp/southcoastscience/psu_status_report.json"
        },
        "psu-version": null,
        "pt1000-calib": {
            "calibrated-on": "2017-08-15T11:21:45Z",
            "v20": 0.320208
        },
        "scd30-baseline": {
            "CO2": {
                "calibrated-on": "2021-06-02T13:11:31+01:00",
                "offset": -123,
                "env": null
            }
        },
        "scd30-conf": null,
        "schedule": {
            "scs-climate": {
                "interval": 60.0,
                "tally": 1
            },
            "scs-gases": {
                "interval": 10.0,
                "tally": 1
            },
            "scs-status": {
                "interval": 10.0,
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
        "networks": {
            "eth0": {
                "kind": "ethernet",
                "state": "connected",
                "connection": "Ethernet eth0"
            },
            "usb0": {
                "kind": "ethernet",
                "state": "unavailable",
                "connection": null
            }
        },
        "modem": null,
        "sim": null,
        "system-id": {
            "set-on": "2022-03-08T11:29:20Z",
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

SEE ALSO
scs_mfr/modem
"""

import sys

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONify

from scs_core.estate.configuration import Configuration

from scs_core.psu.psu_version import PSUVersion

from scs_core.sample.configuration_sample import ConfigurationSample

from scs_core.sys.logging import Logging
from scs_core.sys.system_id import SystemID

from scs_dfe.interface.interface_conf import InterfaceConf

from scs_host.lock.lock_timeout import LockTimeout
from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_configuration import CmdConfiguration

try:
    from scs_psu.psu.psu_conf import PSUConf
except ImportError:
    from scs_core.psu.psu_conf import PSUConf


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    psu_version = None

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdConfiguration()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    # logging...
    Logging.config('configuration', verbose=cmd.verbose)
    logger = Logging.getLogger()

    logger.info(cmd)


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # SystemID...
    system_id = SystemID.load(Host)

    if system_id is None:
        logger.error('SystemID not available.')
        exit(1)

    logger.info(system_id)

    # PSU...
    interface_conf = InterfaceConf.load(Host)
    interface_model = None if interface_conf is None else interface_conf.model

    psu_conf = None if interface_model is None else PSUConf.load(Host)
    psu = None if psu_conf is None else psu_conf.psu(Host, interface_model)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if psu:
        try:
            psu.open()
            psu_version = psu.version()
        except LockTimeout:
            psu_version = PSUVersion.load(Host)     # a report will be present if psu_monitor is running

    try:
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

        configuration = Configuration.load(Host, psu_version=psu_version)
        sample = ConfigurationSample(system_id.message_tag(), LocalizedDatetime.now().utc(), configuration)

        if cmd.table:
            for row in sample.as_table():
                print(row)

        elif cmd.indent is not None:
            print(JSONify.dumps(sample, indent=cmd.indent))

        else:
            print(JSONify.dumps(sample, separators=(',', ':')))         # maximum compactness

    finally:
        if psu:
            psu.close()
