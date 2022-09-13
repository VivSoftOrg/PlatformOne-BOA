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
"""This module has methods for the tags."""

from rules_common.aws_resource_utility.rules_constants import TagsConstants


class TagUtility():
    """This module has methods for the tags."""

    @staticmethod
    def getMissingTagListWithValues(sourceTagList, destinationTagList, excludeTagKeys=None, checkValues=False):
        """
        This is case sensitive method.
        This method will check that tags in sourceTagList are present in destinationTagList or not.
        If not, tags key will be check in excludeTagKeys, if it is not present in excludeTagKeys it will be added to missingTagsList
        If value of checkValues is 'True' it will compare tag's kay and tag's value both else it will only check tag's key are present or not

        input examples - These exmples are only used to reference datatype and structure of input arguments only

            sourceTagList = [{'key': 'Project', 'value': 'MNC'}, {'key': 'Owner', 'value': 'vaibhav.menkudale'},
             {'key': 'ExpirationDate', 'value': '2018-10-25'}, {'key': 'Name', 'value': 'vaibhavCopyTestNAMETag'}]

            destinationTagList = [{'key': 'Project', 'value': 'MNC'}, {'key': 'Group', 'value': 'Website'}]
            excludeTagKeys = ['Environment', 'Project']
            checkValues = (True/False)

            expected return value = [{'key': 'Owner', 'value': 'vaibhav.menkudale'}, {'key': 'ExpirationDate', 'value': '2018-10-25'},
                            {'key': 'Name', 'value': 'vaibhavCopyTestNAMETag'}]
        """
        missingTagsList = []
        if not excludeTagKeys:  # Modifying data type of variable (None to array) because assigning a default value as [] is dangerous in python also it throughs pylint error
            excludeTagKeys = []
        if checkValues:
            for sourceTag in sourceTagList:
                if sourceTag not in destinationTagList and sourceTag['key'] not in excludeTagKeys:
                    missingTagsList.append(sourceTag)
        else:
            destinationTagKeys = [tag['key'] for tag in destinationTagList]
            for sourceTag in sourceTagList:
                if sourceTag['key'] not in destinationTagKeys and sourceTag['key'] not in excludeTagKeys:
                    missingTagsList.append(sourceTag)

        return missingTagsList

    @staticmethod
    def fetchTagListAsDictionary(tagsData):
        """ Function to convert the tags data format to dict type (if not dict already) and return """
        if isinstance(tagsData, dict):
            return tagsData
        elif isinstance(tagsData, list):
            tagsHash = {}
            for tag in tagsData:
                tagsHash.update({tag[TagsConstants.TAG_KEY_REFERENCE]: tag[TagsConstants.TAG_VALUE_REFERENCE]})
            return tagsHash
