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
""" Module for constants """


class SnapshotConstants:
    """ Class for snapshot constants """
    SNAPSHOT_ENCRYPTED = "encrypted"
    SNAPSHOTS = "snapshots"
    SNAPSHOT_ID = "snapshotid"
    SNAPSHOT_DESCRIPTION = "description"
    VOLUME_ID = "volumeid"
    TAGS = 'tags'
    TAG_KEY = 'key'
    TAG_VALUE = 'value'
    NAME_TAG = 'Name'
    VALUES_TAG = 'Values'
    DESCRIBE_SNAPSHOTS_METHOD_REFERENCE = "describe_snapshots"
    OWNER_IDS_REFERENCE = "OwnerIds"
    SELF_KEYWORD = "self"

    def __setattr__(self, attr, value):
        if hasattr(self, attr):
            raise Exception("Attempting to alter read-only value")

        self.__dict__[attr] = value
