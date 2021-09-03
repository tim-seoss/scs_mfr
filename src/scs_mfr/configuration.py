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
    "tag": "scs-opc-1",
    "rec": "2021-09-03T11:03:52Z",
    "val": {
        "hostname": "scs-cube-001",
        "packs": {
            "scs_core": {
                "repo": "scs_core",
                "version": "1.0.27"
            },
            "scs_dev": {
                "repo": "scs_dev",
                "version": "1.0.10"
            },
            "scs_dfe": {
                "repo": "scs_dfe_eng",
                "version": "1.0.9"
            },
            "scs_greengrass": {
                "repo": "scs_greengrass",
                "version": "1.0.3"
            },
            "scs_host": {
                "repo": "scs_host_cpc",
                "version": "1.0.5"
            },
            "scs_inference": {
                "repo": "scs_inference",
                "version": null
            },
            "scs_mfr": {
                "repo": "scs_mfr",
                "version": "1.0.12"
            },
            "scs_ndir": {
                "repo": "scs_ndir",
                "version": null
            },
            "scs_psu": {
                "repo": "scs_psu",
                "version": "1.0.9"
            }
        },
        "afe-baseline": {
            "sn1": {
                "calibrated-on": "2021-08-05T11:29:35Z",
                "offset": 135,
                "env": {
                    "hmd": 51.8,
                    "tmp": 26.5,
                    "pA": null
                }
            },
            "sn2": {
                "calibrated-on": "2021-06-28T10:25:13Z",
                "offset": 0,
                "env": null
            },
            "sn3": {
                "calibrated-on": "2021-06-28T10:25:13Z",
                "offset": 0,
                "env": null
            },
            "sn4": {
                "calibrated-on": "2021-06-28T10:25:13Z",
                "offset": 0,
                "env": null
            }
        },
        "afe-id": {
            "serial_number": null,
            "type": "DSI",
            "calibrated_on": "2021-01-01",
            "sn1": {
                "serial_number": "354931395",
                "sensor_type": "PID"
            }
        },
        "aws-api-auth": {
            "endpoint": "aws.southcoastscience.com",
            "api-key": "de92c5ff-b47a-4cc4-a04c-62d684d64a1f"
        },
        "aws-client-auth": {
            "endpoint": "asrfh6e5j5ecz.iot.us-west-2.amazonaws.com",
            "client-id": "scs-bbe-500",
            "cert-id": "075e2e999f"
        },
        "aws-group-config": {
            "group-name": "scs-cube-001-group",
            "time-initiated": "2021-02-08T16:38:55Z",
            "unix-group": 984,
            "ml": true
        },
        "aws-project": {
            "location-path": "south-coast-science-dev/cube/loc/1",
            "device-path": "south-coast-science-dev/cube/device"
        },
        "csv-logger-conf": {
            "root-path": "/srv/removable_data_storage",
            "delete-oldest": true,
            "write-interval": 0
        },
        "display-conf": null,
        "gas-baseline": {
            "NO2": {
                "calibrated-on": "2021-08-05T11:29:30Z",
                "offset": 11,
                "env": {
                    "hmd": 51.8,
                    "tmp": 26.5,
                    "pA": null
                }
            }
        },
        "gas-model-conf": {
            "uds-path": "pipes/lambda-gas-model.uds",
            "model-interface": "vB"
        },
        "gps-conf": {
            "model": "SAM8Q",
            "sample-interval": 10,
            "tally": 60,
            "report-file": "/tmp/southcoastscience/gps_report.json",
            "debug": false
        },
        "interface-conf": {
            "model": "OPCubeT1"
        },
        "greengrass-identity": {
            "core-name": "scs-cube-001-core",
            "group-name": "scs-cube-001-group"
        },
        "mpl115a2-calib": null,
        "mqtt-conf": {
            "inhibit-publishing": false,
            "report-file": "/tmp/southcoastscience/mqtt_queue_report.json",
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
            "serial": "177336702",
            "firmware": "OPC-N3 Iss1.1 FirmwareVer=1.17a...........................BS"
        },
        "pmx-model-conf": {
            "uds-path": "pipes/lambda-pmx-model.uds",
            "model-interface": "s1"
        },
        "pressure-conf": null,
        "psu-conf": {
            "model": "OPCubeV1",
            "batt-model": "PackV2",
            "ignore-threshold": true,
            "reporting-interval": 5,
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
            "key": "Ytzglk6oYpzJY0FB"
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
                "state": "connected",
                "connection": "giffgaff"
            }
        },
        "modem": {
            "id": "3f07553c31ce11715037ac16c24ceddcfb6f7a0b",
            "imei": "867962041294151",
            "mfr": "QUALCOMM INCORPORATED",
            "model": "QUECTEL Mobile Broadband Module",
            "rev": "EC21EFAR06A01M4G"
        },
        "sim": {
            "imsi": "234104886708667",
            "iccid": "8944110068256270054",
            "operator-code": "23410",
            "operator-name": "O2 - UK"
        },
        "system-id": {
            "vendor-id": "SCS",
            "model-id": "OPC",
            "model": "Praxis/OPCube",
            "config": "v1",
            "system-sn": 1
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
from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONify

from scs_core.estate.configuration import Configuration

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

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdConfiguration()

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
        except LockTimeout:
            psu = None

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

        configuration = Configuration.load(Host, psu=psu)
        sample = ConfigurationSample(system_id.message_tag(), LocalizedDatetime.now().utc(), configuration)

        print(JSONify.dumps(sample, indent=cmd.indent))

    finally:
        if psu:
            psu.close()
