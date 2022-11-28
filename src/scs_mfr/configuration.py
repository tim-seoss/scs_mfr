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
    "rec": "2022-11-25T11:33:58Z",
    "tag": "scs-opc-1",
    "ver": 1.0,
    "val": {
        "hostname": "scs-cube-001",
        "packs": {
            "scs_core": {
                "repo": "scs_core",
                "version": "1.4.18"
            },
            "scs_dev": {
                "repo": "scs_dev",
                "version": "2.1.6"
            },
            "scs_dfe": {
                "repo": "scs_dfe_eng",
                "version": "2.1.3"
            },
            "scs_greengrass": {
                "repo": "scs_greengrass",
                "version": "2.3.1"
            },
            "scs_host": {
                "repo": "scs_host_cpc",
                "version": "1.0.12"
            },
            "scs_mfr": {
                "repo": "scs_mfr",
                "version": "1.4.8"
            },
            "scs_ndir": {
                "repo": "scs_ndir",
                "version": null
            },
            "scs_psu": {
                "repo": "scs_psu",
                "version": "1.1.4"
            }
        },
        "afe-baseline": {
            "sn1": {
                "calibrated-on": "2022-11-16T15:14:30Z",
                "offset": 272,
                "env": {
                    "rec": "2022-11-15T21:40:00Z",
                    "hmd": 58.9,
                    "tmp": 20.6
                }
            },
            "sn2": {
                "calibrated-on": "2022-11-15T13:12:54Z",
                "offset": 0,
                "env": null
            },
            "sn3": {
                "calibrated-on": "2022-11-15T13:12:54Z",
                "offset": 0,
                "env": null
            },
            "sn4": {
                "calibrated-on": "2022-11-15T13:12:54Z",
                "offset": 0,
                "env": null
            }
        },
        "afe-id": {
            "serial_number": null,
            "type": "DSI",
            "calibrated_on": "2022-01-01",
            "sn1": {
                "serial_number": "212060325",
                "sensor_type": "NO2A43F"
            }
        },
        "aws-group-config": {
            "group-name": "scs-cube-001-group",
            "time-initiated": "2022-11-15T13:20:17Z",
            "unix-group": 984,
            "ml": "oE.1"
        },
        "aws-project": {
            "location-path": "south-coast-science-dev/cube/loc/1",
            "device-path": "south-coast-science-dev/cube/device"
        },
        "data-log": {
            "path": "/srv/removable_data_storage",
            "available": true,
            "on-root": false
        },
        "display-conf": null,
        "vcal-baseline": {
            "NO2": {
                "calibrated-on": "2022-11-16T15:04:46Z",
                "offset": 206,
                "env": null
            }
        },
        "gas-baseline": null,
        "gas-model-conf": {
            "uds-path": "pipes/lambda-gas-model.uds",
            "model-interface": "vE",
            "model-compendium-group": "oE.1"
        },
        "gps-conf": null,
        "interface-conf": {
            "model": "OPCubeT1"
        },
        "greengrass-identity": null,
        "mpl115a2-calib": null,
        "mqtt-conf": null,
        "ndir-conf": null,
        "opc-conf": {
            "model": "N3",
            "sample-period": 10,
            "restart-on-zeroes": true,
            "power-saving": false
        },
        "opc-version": {
            "serial": "177336702",
            "firmware": "OPC-N3 Iss1.1 FirmwareVer=1.17a...........................BS"
        },
        "pmx-model-conf": {
            "uds-path": "pipes/lambda-pmx-model.uds",
            "model-interface": "s2"
        },
        "pressure-conf": null,
        "psu-conf": {
            "model": "OPCubeV1",
            "batt-model": "PackV2",
            "ignore-threshold": false,
            "reporting-interval": 10,
            "report-file": "/tmp/southcoastscience/psu_status_report.json"
        },
        "psu-version": {
            "id": "SCS OPCube Controller type 1 firmware 1",
            "tag": "001.001.003",
            "c-date": null,
            "c-time": null
        },
        "pt1000-calib": null,
        "scd30-baseline": null,
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
            "key": "IuIIGqwQWX5c7Z0Z"
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
            "cdc-wdm0": {
                "kind": "gsm",
                "state": "unavailable",
                "connection": null
            }
        },
        "modem": {
            "id": "3f07553c31ce11715037ac16c247a0b",
            "imei": null,
            "mfr": "QUALCOMM INCORPORATED",
            "model": "QUECTEL Mobile Broadband Module",
            "rev": "EC26A01M4G"
        },
        "sim": null,
        "system-id": {
            "set-on": "2022-11-15T13:17:28Z",
            "vendor-id": "SCS",
            "model-id": "OPC",
            "model": "Praxis/OPCube",
            "config": "v1",
            "system-sn": 1
        },
        "timezone-conf": {
            "set-on": "2022-11-15T13:46:10Z",
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
