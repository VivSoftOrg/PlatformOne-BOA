# eventParam.awsPartitionName = 'aws'
# eventParam.accNo = '107339370656' 
import unittest
from utility.tag_utility import TagUtility


SOURCE_TAG_LIST = sourceTagList = [{'key': 'Project', 'value': 'MNC-Test'}, {'key': 'Owner', 'value': 'vaibhav.menkudale'}, {'key': 'ExpirationDate', 'value': '2018-10-25'}, {'key': 'Name', 'value': 'vaibhavCopyTestNAMETag'}]
DESTINATION_TAG_LIST = [{'key': 'Project', 'value': 'MNC'}, {'key': 'Group', 'value': 'Website'}]
EXCLUDE_TAG_KEYS = ['Environment', 'Owner']
RESPONSE_ONE_CHECK_WITH_KEY_NAMES_ONLY = [{'key': 'ExpirationDate', 'value': '2018-10-25'}, {'key': 'Name', 'value': 'vaibhavCopyTestNAMETag'}]
RESPONSE_TWO_CHECK_WO_EXCLUDE_TAG_KEYS =[{'key': 'Owner', 'value': 'vaibhav.menkudale'}, {'key': 'ExpirationDate', 'value': '2018-10-25'}, {'key': 'Name', 'value': 'vaibhavCopyTestNAMETag'}]
RESPONSE_THREE_WITH_CHECK_VALUES = [{'key': 'Project', 'value': 'MNC-Test'}, {'key': 'ExpirationDate', 'value': '2018-10-25'}, {'key': 'Name', 'value': 'vaibhavCopyTestNAMETag'}]

class TestTagUtility(unittest.TestCase):

    def testGetMissingTagsListWithhValuesFirst(self):
        return_value=TagUtility.getMissingTagListWithValues(sourceTagList=SOURCE_TAG_LIST, destinationTagList=DESTINATION_TAG_LIST, excludeTagKeys=EXCLUDE_TAG_KEYS)
        assert return_value == RESPONSE_ONE_CHECK_WITH_KEY_NAMES_ONLY

    def testGetMissingTagsListWithhValuesSecondWithoutExcludeTagKeys(self):
        return_value=TagUtility.getMissingTagListWithValues(sourceTagList=SOURCE_TAG_LIST, destinationTagList=DESTINATION_TAG_LIST)
        assert return_value == RESPONSE_TWO_CHECK_WO_EXCLUDE_TAG_KEYS

    def testGetMissingTagsListWithhValuesThree(self):
        return_value=TagUtility.getMissingTagListWithValues(sourceTagList=SOURCE_TAG_LIST, destinationTagList=DESTINATION_TAG_LIST, excludeTagKeys=EXCLUDE_TAG_KEYS, checkValues=True)
        assert return_value == RESPONSE_THREE_WITH_CHECK_VALUES
