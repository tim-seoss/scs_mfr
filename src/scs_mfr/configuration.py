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
configuration.py [-s CONFIGURATION] [-x] [{ -i INDENT | -t }] [-v]

EXAMPLES
./configuration.py -i4 -s '{"timezone-conf": {"name": "Europe/London"}}'

DOCUMENT EXAMPLE
{
    "rec": "2023-02-28T12:25:24Z",
    "tag": "scs-bgx-431",
    "ver": 1.2,
    "val": {
        "hostname": "scs-bbe-431",
        "os": {
            "rel": "4.19.173-bone60",
            "vers": "#1buster PREEMPT Tue Feb 16 23:42:12 UTC 2021"
        },
        "packs": {
            "scs_core": {
                "repo": "scs_core",
                "version": "2.4.1"
            },
            "scs_dev": {
                "repo": "scs_dev",
                "version": "2.4.0"
            },
            "scs_dfe": {
                "repo": "scs_dfe_eng",
                "version": "2.4.0"
            },
            "scs_greengrass": {
                "repo": "scs_greengrass",
                "version": "2.4.0"
            },
            "scs_host": {
                "repo": "scs_host_bbe_southern",
                "version": "1.0.13"
            },
            "scs_mfr": {
                "repo": "scs_mfr",
                "version": "1.5.4"
            },
            "scs_psu": {
                "repo": "scs_psu",
                "version": "1.2.0"
            }
        },
        "afe-baseline": {
            "sn1": {
                "calibrated-on": "2023-02-08T12:52:39Z",
                "offset": 10,
                "env": {
                    "rec": "2023-02-08T02:40:00Z",
                    "hmd": 30.7,
                    "tmp": 20.3
                }
            },
            "sn2": {
                "calibrated-on": "2023-02-08T12:52:42Z",
                "offset": 48,
                "env": {
                    "rec": "2023-02-08T07:55:00Z",
                    "hmd": 31.3,
                    "tmp": 19.5
                }
            },
            "sn3": {
                "calibrated-on": "2023-02-08T12:52:37Z",
                "offset": 97,
                "env": {
                    "rec": "2023-02-07T17:05:00Z",
                    "hmd": 31.7,
                    "tmp": 23.1
                }
            },
            "sn4": {
                "calibrated-on": "2023-02-08T12:52:32Z",
                "offset": 142,
                "env": {
                    "rec": "2023-02-08T05:45:00Z",
                    "hmd": 31.0,
                    "tmp": 19.8
                }
            }
        },
        "afe-id": {
            "serial_number": "26-000595",
            "type": "810-0023-01",
            "calibrated_on": "2022-11-23",
            "sn1": {
                "serial_number": "212801359",
                "sensor_type": "NO2A43F"
            },
            "sn2": {
                "serial_number": "214801144",
                "sensor_type": "OXA431"
            },
            "sn3": {
                "serial_number": "130820459",
                "sensor_type": "NO A4"
            },
            "sn4": {
                "serial_number": "132800043",
                "sensor_type": "CO A4"
            }
        },
        "aws-group-config": {
            "group-name": "scs-bbe-431-group",
            "time-initiated": "2023-02-28T10:32:28Z",
            "unix-group": 987,
            "ml": "uE.1"
        },
        "aws-project": {
            "location-path": "ricardo/heathrow/loc/4",
            "device-path": "ricardo/heathrow/device"
        },
        "data-log": {
            "path": "/srv/removable_data_storage",
            "is-available": true,
            "on-root": false,
            "used": 6
        },
        "display-conf": null,
        "vcal-baseline": {
            "NO": {
                "calibrated-on": "2023-01-22T18:56:44Z",
                "offset": -15
            },
            "NO2": {
                "calibrated-on": "2023-01-22T08:45:53Z",
                "offset": 2
            }
        },
        "gas-baseline": null,
        "gas-model-conf": {
            "uds-path": "pipes/lambda-gas-model.uds",
            "model-interface": "vE",
            "model-compendium-group": "uE.1"
        },
        "gps-conf": {
            "model": "PAM7Q",
            "sample-interval": 10,
            "tally": 60,
            "report-file": "/tmp/southcoastscience/gps_report.json",
            "debug": false
        },
        "interface-conf": null,
        "mpl115a2-calib": {
            "calibrated-on": "2021-03-18T13:25:10Z",
            "c25": 506
        },
        "mqtt-conf": {
            "inhibit-publishing": false,
            "report-file": null,
            "debug": false
        },
        "ndir-conf": null,
        "opc-conf": {
            "model": "N3",
            "sample-period": 10,
            "restart-on-zeroes": true,
            "power-saving": false
        },
        "opc-version": {
            "serial": "177780318",
            "firmware": "OPC-N3 Iss1.1 FirmwareVer=1.17a...........................BS"
        },
        "pmx-model-conf": {
            "uds-path": "pipes/lambda-pmx-model.uds",
            "model-interface": "s2"
        },
        "pressure-conf": {
            "model": "ICP",
            "altitude": 25
        },
        "psu-conf": {
            "model": "OsloV1",
            "batt-model": null,
            "ignore-threshold": false,
            "reporting-interval": 10,
            "report-file": "/tmp/southcoastscience/psu_status_report.json"
        },
        "psu-version": {
            "id": "South Coast Science PSU Oslo",
            "tag": "2.2.5"
        },
        "pt1000-calib": {
            "calibrated-on": "2017-08-15T11:21:45Z",
            "v20": 0.320208
        },
        "scd30-baseline": {
            "CO2": {
                "calibrated-on": "2023-02-08T12:52:34Z",
                "offset": -7,
                "env": {
                    "hmd": 30.9,
                    "tmp": 20.0
                }
            }
        },
        "scd30-conf": {
            "sample-interval": 5,
            "temp-offset": 0.0
        },
        "schedule": {
            "scs-climate": {
                "interval": 60.0,
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
            "key": "0jZoQDiSJJ1Rl"
        },
        "sht-conf": {
            "int": "0x45",
            "ext": "0x45"
        },
        "networks": {
            "cdc-wdm0": {
                "kind": "gsm",
                "state": "connected",
                "connection": "EE M2M"
            },
            "eth0": {
                "kind": "ethernet",
                "state": "unavailable",
                "connection": null
            }
        },
        "modem": {
            "id": "e3f0ca1c313f4d586a9c47dc4fd6c1cb46e6",
            "imei": "866758042325619",
            "mfr": "QUALCOMM INCORPORATED",
            "model": "QUECTEL Mobile Broadband Module",
            "rev": "EC2506A03M4G"
        },
        "sim": {
            "imsi": "234301951432536",
            "iccid": "8944303382697124815",
            "operator-code": "23430",
            "operator-name": "EE"
        },
        "system-id": {
            "set-on": "2019-01-04T11:28:27Z",
            "vendor-id": "SCS",
            "model-id": "BGX",
            "model": "Praxis",
            "config": "BGX",
            "system-sn": 431
        },
        "timezone-conf": {
            "set-on": "2017-08-15T12:50:05Z",
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
            psu_version = PSUVersion.load(Host)         # a report will be present if psu_monitor is running
        except OSError:
            psu_version = None                          # PSU fault

    try:
        if cmd.save():
            conf = Configuration.construct_from_jstr(cmd.configuration)

            if conf is None:
                logger.error('invalid configuration: %s' % cmd.configuration)
                exit(2)

            try:
                conf.save(Host)
            except ValueError as ex:
                logger.error(repr(ex))
                exit(1)

        configuration = Configuration.load(Host, psu_version=psu_version, exclude_sim=cmd.exclude_sim)
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
