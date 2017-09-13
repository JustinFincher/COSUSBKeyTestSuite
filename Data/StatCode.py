import os
#
# from enum import Enum
# class InstructorType(Enum):

from enum import Enum

class StatCodeType(Enum):
    NON_DEFINED = 0
    STAT_CODE_SUCCESS = 1
    STAT_CODE_PIN_VALIDATE_FAILURE_REMAIN_TRY_COUNT = 2
    STAT_CODE_OUTPUT_RULE_NOT_MEET = 3
    STAT_CODE_WRITE_FAILURE = 4
    STAT_CODE_DATE_LENGTH_ERR = 5
    STAT_CODE_SAFETY_STATS_NOT_MEET = 6
    STAT_CODE_PIN_LOCKED = 7
    STAT_CODE_RANDOM_NUM_NOT_FOUND_OBJECT_NOT_FOUND = 8
    STAT_CODE_USE_RULE_NOT_MEET = 9
    STAT_CODE_NOT_SELECT_EF = 10
    STAT_CODE_CAL_MAC_NOT_RIGHT = 11
    STAT_CODE_DATA_FIELD_PARAMETER_NOT_RIGHT = 12
    STAT_CODE_FUNCTION_NOT_SUPPORTED = 13
    STAT_CODE_FILE_NOT_FOUND = 14
    STAT_CODE_P1_P2_NOT_RIGHT = 15
    STAT_CODE_DF_NOT_FOUND = 16
    STAT_CODE_ADDRESS_OFFEST_BEYOUND_FILE = 17
    STAT_CODE_INS_NOT_SUPPORTED = 18
    STAT_CODE_CLA_NOT_SUPPORTED = 19



class StatCode:

    _sw1 = None
    _sw2 = None

    statCode = StatCodeType.NON_DEFINED

    def __init__(self):
        pass

    def __init__(self,osw1,osw2):
        self.sw1 = osw1
        self.sw2 = osw2

    @property
    def sw1(self):
        return self._sw1

    @sw1.setter
    def sw1(self, value):
        self._sw1 = value
        self.statCodeCheck()

    @sw1.deleter
    def sw1(self):
        del self._sw1


    @property
    def sw2(self):
        return self._sw2

    @sw2.setter
    def sw2(self, value):
        self._sw2 = value
        self.statCodeCheck()

    @sw2.deleter
    def sw2(self):
        del self._sw2


    def statCodeCheck(self):
        if (self.sw1 == None or self.sw2 == None):
            return

        if self.sw1 == '90':
            self.statCode = StatCodeType.STAT_CODE_SUCCESS
        elif self.sw1 == '63':
            self.statCode = StatCodeType.STAT_CODE_PIN_VALIDATE_FAILURE_REMAIN_TRY_COUNT
        elif self.sw1 == '64':
            self.statCode = StatCodeType.STAT_CODE_OUTPUT_RULE_NOT_MEET
        elif self.sw1 == '65':
            self.statCode = StatCodeType.STAT_CODE_WRITE_FAILURE
        elif self.sw1 == '67':
            self.statCode = StatCodeType.STAT_CODE_DATE_LENGTH_ERR



        pass
