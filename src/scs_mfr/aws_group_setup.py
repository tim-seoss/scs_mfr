import sys

from scs_host.sys.host import Host
from scs_mfr.aws_group_configurator import AWSGroupConfigurator
from scs_mfr.aws_json_reader import AWSJsonReader
from scs_mfr.cmd.cmd_aws_group_setup import CmdAWSGroupSetup

# --------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdAWSGroupSetup()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("aws_group_setup: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()
    # ----------------------------------------------------------------------------------------------------------------
    # run...
    if not cmd.is_valid():
        print("aws_group_setup: Invalid options ", file=sys.stderr)
        cmd.print_help(sys.stderr)
        exit(1)
    unix_group = cmd.unix_group if cmd.unix_group else 0
    use_ml = True if cmd.use_ml else False
    aws_group = cmd.aws_group_name

    # ClientAuth...
    awsGroupConf = AWSGroupConfigurator.load(Host)

    if cmd.set():
        if awsGroupConf:
            user_choice = input("Group configuration already exists. Type Yes to update: ")
            print("")
            if not user_choice.lower() == "yes":
                print("Operation cancelled")
                exit()

        aws_configurator = AWSGroupConfigurator(aws_group, unix_group, use_ml)
        aws_configurator.collect_information()
        aws_configurator.define_aws_group_resources()
        aws_configurator.define_aws_group_functions()
        aws_configurator.define_aws_group_subscriptions()
        aws_configurator.create_aws_group_definition()
        aws_configurator.save(Host)

    if cmd.show_current:
        aws_json_reader = AWSJsonReader(aws_group)
        aws_json_reader.get_group_info_from_name()
        aws_json_reader.get_group_arns()
        aws_json_reader.output_current_info()

    # ----------------------------------------------------------------------------------------------------------------
