# REANCloud CONFIDENTIAL
# __________________
#
#  (C) 2018 REANCloud LLC
#  All Rights Reserved.
#
# NOTICE: All information contained herein is, and remains
# the property of REANCloud LLC and its suppliers,
# if any. The intellectual and technical concepts contained
# herein are proprietary to REANCloud LLC and its suppliers
# and may be covered by U.S. and Foreign Patents,
# patents in process, and are protected by trade secret or copyright law.
# Dissemination of this information or reproduction of this material
# is strictly forbidden unless prior written permission is obtained
# from REANCloud LLC.
''' This module is used to create class objects dynimacally at runtime based on the resource type recieved for the MNC rule'''
import importlib

from common.common_utility import CommonUtility


class ClassUtility:
    """This class creates class objects common rules utilities"""

    @staticmethod
    def getclassObject(moduleName, serviceName, classType, eventParam):
        """
            This function creates class objects for various AWS Resource utilities
            Input Parameters:
                                moduleName = The MNC module name where the class file is located, eg: rules_common.aws_resources, utility
                                serviceName = The AWS service name, eg: ec2, ebs, etc
                                classType = Type of class, viz; utility, constant, etc etc
                                eventParam = The event parametes recieved for the rule
        """
        classModule = moduleName + "." + serviceName + "_" + classType
        evaluatorClassName = CommonUtility.snakeToCamelCase(serviceName + "_" + classType)
        module = importlib.import_module(classModule, "")
        evaluatorClass = getattr(module, evaluatorClassName)
        return evaluatorClass(eventParam)
