import json
import sys
import boto3
import botocore
from scs_core.data.path_dict import PathDict


# --------------------------------------------------------------------------------------------------------------------
def split_id_from_version_id(arn_type, combined):
    if arn_type == "core":
        split1 = combined.split("/cores/")
        res = split1[1].split("/versions/")
    if arn_type == "function":
        split1 = combined.split("/functions/")
        res = split1[1].split("/versions/")
    if arn_type == "logger":
        split1 = combined.split("/loggers/")
        res = split1[1].split("/versions/")
    if arn_type == "resources":
        split1 = combined.split("/resources/")
        res = split1[1].split("/versions/")
    if arn_type == "subscriptions":
        split1 = combined.split("/subscriptions/")
        res = split1[1].split("/versions/")
    return res


# --------------------------------------------------------------------------------------------------------------------

class AWSJsonReader:
    # ----------------------------------------------------------------------------------------------------------------
    def __init__(self, group_name):
        """
        Constructor
        """
        self.__client = boto3.client('greengrass')
        self.__groupinfo = PathDict()
        self.__groupinfo.append("GroupName", [group_name])
    # ----------------------------------------------------------------------------------------------------------------

    def get_group_info_from_name(self):
        try:
            response = self.__client.list_groups(
            )
        except botocore.exceptions.ClientError as error:
            if error.response['Error']['Code'] == 'BadRequestException':
                print("aws_json_reader: Invalid request.", file=sys.stderr)
            if error.response['Error']['Code'] == 'InternalServerErrorException':
                print("aws_json_reader: AWS server error.", file=sys.stderr)
            else:
                raise error

        d_groups = PathDict.construct_from_jstr(json.dumps(response))
        g_node = d_groups.node("Groups")
        name_node = self.__groupinfo.node("GroupName")
        for subnode in g_node:
            this_name = subnode["Name"]
            if this_name == self.__groupinfo.node("GroupName")[0]:
                self.__groupinfo.append("GroupID", subnode["Id"])
                self.__groupinfo.append("GroupLatestVersionID", subnode["LatestVersion"])
                self.__groupinfo.append("LastUpdated", subnode["LastUpdatedTimestamp"])
                break

    # ----------------------------------------------------------------------------------------------------------------

    def get_group_arns(self):
        response = self.__client.get_group_version(
            GroupId=self.__groupinfo.node("GroupID"),
            GroupVersionId=self.__groupinfo.node("GroupLatestVersionID")
        )
        v_group = PathDict.construct_from_jstr(json.dumps(response))
        sub_v_group = v_group.node("Definition")

        if "CoreDefinitionVersionArn" in sub_v_group:
            self.__groupinfo.append("CoreDefinitionVersionArn", sub_v_group["CoreDefinitionVersionArn"])
        if "FunctionDefinitionVersionArn" in sub_v_group:
            self.__groupinfo.append("FunctionDefinitionVersionArn", sub_v_group["FunctionDefinitionVersionArn"])
        if "LoggerDefinitionVersionArn" in sub_v_group:
            self.__groupinfo.append("LoggerDefinitionVersionArn", sub_v_group["LoggerDefinitionVersionArn"])
        if "ResourceDefinitionVersionArn" in sub_v_group:
            self.__groupinfo.append("ResourceDefinitionVersionArn", sub_v_group["ResourceDefinitionVersionArn"])
        if "SubscriptionDefinitionVersionArn" in sub_v_group:
            self.__groupinfo.append("SubscriptionDefinitionVersionArn", sub_v_group["SubscriptionDefinitionVersionArn"])

    # ----------------------------------------------------------------------------------------------------------------
    def output_current_info(self):
        if self.__groupinfo.has_path("CoreDefinitionVersionArn"):
            self.get_core_definition()
        if self.__groupinfo.has_path("LoggerDefinitionVersionArn"):
            self.get_logger_definition()
        if self.__groupinfo.has_path("ResourceDefinitionVersionArn"):
            self.get_resource_definition()
        if self.__groupinfo.has_path("FunctionDefinitionVersionArn"):
            self.get_function_definition()
        if self.__groupinfo.has_path("SubscriptionDefinitionVersionArn"):
            self.get_subscription_definition_version()

    # ----------------------------------------------------------------------------------------------------------------
    def get_core_definition(self):

        if not self.__groupinfo.has_path("CoreDefinitionVersionArn"):
            return
        if not self.__groupinfo.node("CoreDefinitionVersionArn"):
            return

        arn = split_id_from_version_id("core", self.__groupinfo.node("CoreDefinitionVersionArn"))
        response = self.__client.get_core_definition_version(
            CoreDefinitionId=arn[0],
            CoreDefinitionVersionId=arn[1]
        )
        print(json.dumps(response, indent=2))  # Dump to stdout?

    # ----------------------------------------------------------------------------------------------------------------
    def get_function_definition(self):

        if not self.__groupinfo.has_path("FunctionDefinitionVersionArn"):
            return
        if not self.__groupinfo.node("FunctionDefinitionVersionArn"):
            return

        arn = split_id_from_version_id("function", self.__groupinfo.node("FunctionDefinitionVersionArn"))
        response = self.__client.get_function_definition_version(
            FunctionDefinitionId=arn[0],
            FunctionDefinitionVersionId=arn[1]
        )
        print(json.dumps(response, indent=2))

    # ----------------------------------------------------------------------------------------------------------------

    def get_logger_definition(self):

        if not self.__groupinfo.has_path("LoggerDefinitionVersionArn"):
            return
        if not self.__groupinfo.node("LoggerDefinitionVersionArn"):
            return

        arn = split_id_from_version_id("logger", self.__groupinfo.node("LoggerDefinitionVersionArn"))
        response = self.__client.get_logger_definition_version(
            LoggerDefinitionId=arn[0],
            LoggerDefinitionVersionId=arn[1]
        )
        print(json.dumps(response, indent=2))

    # ----------------------------------------------------------------------------------------------------------------

    def get_resource_definition(self):

        if not self.__groupinfo.has_path("ResourceDefinitionVersionArn"):
            return
        if not self.__groupinfo.node("ResourceDefinitionVersionArn"):
            return

        arn = split_id_from_version_id("resources", self.__groupinfo.node("ResourceDefinitionVersionArn"))
        response = self.__client.get_resource_definition_version(
            ResourceDefinitionId=arn[0],
            ResourceDefinitionVersionId=arn[1]
        )
        print(json.dumps(response, indent=2))

    # ----------------------------------------------------------------------------------------------------------------

    def get_subscription_definition_version(self):

        if not self.__groupinfo.has_path("SubscriptionDefinitionVersionArn"):
            return
        if not self.__groupinfo.node("SubscriptionDefinitionVersionArn"):
            return

        arn = split_id_from_version_id("subscriptions", self.__groupinfo.node("SubscriptionDefinitionVersionArn"))
        response = self.__client.get_subscription_definition_version(
            SubscriptionDefinitionId=arn[0],
            SubscriptionDefinitionVersionId=arn[1]
        )
        print(json.dumps(response, indent=2))

    # ----------------------------------------------------------------------------------------------------------------
    def append_to_group_info(self, path, value):
        self.__groupinfo.append(path, value)

    # ----------------------------------------------------------------------------------------------------------------
    def retrieve_node(self, path):
        if self.__groupinfo.has_path(path):
            return self.__groupinfo.node(path)
        else:
            return "-"


