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
{"rec": "2021-10-06T11:27:48Z", "tag": "scs-be2-3", "ver": 1.0, "val": {"hostname": "scs-bbe-003",
"packs": {"scs_comms": {"repo": "scs_comms_ge910", "version": null}, "scs_core": {"repo": "scs_core",
"version": "1.0.32"}, "scs_dev": {"repo": "scs_dev", "version": "1.0.11"}, "scs_dfe": {"repo": "scs_dfe_eng",
"version": "1.0.10"}, "scs_exegesis": {"repo": "scs_exegesis", "version": null},
"scs_greengrass": {"repo": "scs_greengrass", "version": "1.0.3"}, "scs_host": {"repo": "scs_host_bbe_southern",
"version": "1.0.6"}, "scs_inference": {"repo": "scs_inference", "version": null}, "scs_mfr": {"repo": "scs_mfr",
"version": "1.0.14"}, "scs_ndir": {"repo": "scs_ndir", "version": null}, "scs_osio": {"repo": "scs_osio",
"version": null}, "scs_psu": {"repo": "scs_psu", "version": "1.0.10"}},
"afe-baseline": {"sn1": {"calibrated-on": "2021-08-22T12:46:44Z", "offset": 13, "env": {"hmd": 62.6, "tmp": 24.5,
"pA": 102.1}}, "sn2": {"calibrated-on": "2021-08-22T12:46:38Z", "offset": -7, "env": {"hmd": 62.7, "tmp": 24.5,
"pA": 102.1}}, "sn3": {"calibrated-on": "2021-08-22T12:46:46Z", "offset": 24, "env": {"hmd": 62.6, "tmp": 24.5,
"pA": 102.1}}, "sn4": {"calibrated-on": "2021-08-22T12:46:41Z", "offset": 9, "env": {"hmd": 62.6, "tmp": 24.5,
"pA": 102.1}}}, "afe-id": {"serial_number": "27-000001", "type": "810-0023-02", "calibrated_on": "2016-11-01",
"sn1": {"serial_number": "212060308", "sensor_type": "NO2A43F"}, "sn2": {"serial_number": "132950202",
"sensor_type": "CO A4"}, "sn3": {"serial_number": "134060009", "sensor_type": "SO2A4"},
"sn4": {"serial_number": "133910023", "sensor_type": "H2SA4"}},
"aws-api-auth": {"endpoint": "aws.southcoastscience.com", "api-key": "a04c-62d684d64a1f"},
"aws-client-auth": {"endpoint": "asrfh6e5j5ecz.iot.us-west-2.amazonaws.com", "client-id": "scs-bbe-003",
"cert-id": "cd505d98bf"}, "aws-group-config": {"group-name": "scs-bbe-003-group",
"time-initiated": "2021-01-29T11:52:25Z", "unix-group": 987, "ml": true},
"aws-project": {"location-path": "south-coast-science-dev/development/loc/1",
"device-path": "south-coast-science-dev/development/device"},
"csv-logger-conf": {"root-path": "/srv/removable_data_storage", "delete-oldest": true, "write-interval": 0},
"display-conf": null, "gas-baseline": {"NO2": {"calibrated-on": "2021-08-22T12:40:13Z", "offset": 3,
"env": {"hmd": 62.5, "tmp": 24.3, "pA": 102.0}}}, "gas-model-conf": {"uds-path": "pipes/lambda-gas-model.uds",
"model-interface": "vB"}, "gps-conf": {"model": "SAM8Q", "sample-interval": 10, "tally": 60,
"report-file": "/tmp/southcoastscience/gps_report.json", "debug": false}, "interface-conf": {"model": "DFE"},
"greengrass-identity": null, "mpl115a2-calib": {"calibrated-on": "2020-11-15T11:29:23Z", "c25": 510},
"mqtt-conf": {"inhibit-publishing": true, "report-file": null, "debug": false}, "ndir-conf": {"model": "t1f1",
"tally": 1, "raw": false}, "opc-conf": {"model": "N3", "sample-period": 10, "restart-on-zeroes": true,
"power-saving": false}, "opc-version": null, "pmx-model-conf": {"uds-path": "pipes/lambda-pmx-model.uds",
"model-interface": "s1"}, "pressure-conf": {"model": "ICP", "altitude": 101}, "psu-conf": {"model": "OsloV1",
"batt-model": null, "ignore-threshold": false, "reporting-interval": 20,
"report-file": "/tmp/southcoastscience/psu_status_report.json"}, "psu-version": null,
"pt1000-calib": {"calibrated-on": "2017-08-15T11:21:45Z", "v20": 0.320208},
"scd30-baseline": {"CO2": {"calibrated-on": "2021-08-22T12:40:15Z", "offset": 5, "env": {"hmd": 62.5, "tmp": 24.3,
"pA": 102.0}}}, "scd30-conf": null, "schedule": {"scs-climate": {"interval": 60.0, "tally": 1},
"scs-gases": {"interval": 10.0, "tally": 1}, "scs-status": {"interval": 60.0, "tally": 1}},
"shared-secret": {"key": "pYL7B1JcgJ2gy6MP"}, "sht-conf": {"int": "0x45", "ext": "0x45"},
"networks": {"eth0": {"kind": "ethernet", "state": "connected", "connection": "Ethernet eth0"},
"usb0": {"kind": "ethernet", "state": "unavailable", "connection": null}}, "modem": null, "sim": null,
"system-id": {"set-on": "2021-09-12T12:04:25Z", "vendor-id": "SCS", "model-id": "BE2", "model": "Alpha BB Eng",
"config": "V2", "system-sn": 3}, "timezone-conf": {"set-on": "2021-01-31T11:26:14Z", "name": "Europe/London"}}}

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
