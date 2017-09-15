from Data.Test import *
from Controller.Helper import *
import pyDes
from Test.TEST_VALIDATE_PIN import *
from Controller.DeviceManager import *


class TEST_MODIFY_PIN(Test):


    def run(self):

        # SELECT MF
        LogManager().addLogStr("WILL SELECT MF", LogType.Info, self.getTestType())
        dict = Helper().getSelectFileDict(FileLocationType.MF)
        if (dict != None) and ('statCode' in dict):
            statCode = dict["statCode"].statCode
            if statCode != StatCodeType.STAT_CODE_SUCCESS:
                return False

        # SELECT ADF
        LogManager().addLogStr("WILL SELECT ADF", LogType.Info, self.getTestType())
        dict = Helper().getSelectFileDict(FileLocationType.ADF)
        if (dict != None) and ('statCode' in dict):
            statCode = dict["statCode"].statCode
            if statCode != StatCodeType.STAT_CODE_SUCCESS:
                return False


        new_pin = "2345"
        pin = "1234"
        hexifiedPin = Helper().getMd5HashHex(new_pin)
        print(hexifiedPin)
        hexifiedPin = Helper().replaceFFWithFE(hexifiedPin)
        print(hexifiedPin)

        randomMsg = Helper().getChallengeMsg()
        if randomMsg == None:
            print("TEST_MODIFY_PIN FALSE")
            return False

        m = hashlib.md5()
        newPinUTF8 = new_pin.encode('utf-8')
        m.update(newPinUTF8)
        h = m.hexdigest().lower()
        h = Helper().replaceFFWithFE(h).lower()
        h1 = '5500' + h
        h2 = '{:02X}'.format(len(h1)) + h1
        k = pyDes.triple_des(bytes.fromhex('12345678214365871122aabb3344cdef'), pyDes.ECB, b"\0\0\0\0\0\0\0\0",
                             pad=None, padmode=pyDes.PAD_PKCS5)
        h3 = binascii.hexlify(k.encrypt(bytes.fromhex(h2))).decode('utf-8')
        h4 = "84F40900" + '{:02X}'.format(len(h3) + 4) + h3.upper()
        r = randomMsg

        #h40 = '84F40900' + str(hex(int(len(h3) / 2)))[2:] + h3.upper()
        #h41 = '84F40900' + str(hex(int(len(h3) / 2)))[2:] + h3.upper()

        mac = self.PBOC_3DES_MAC("12345678214365871122aabb3344cdef",r,h4)
        apdu = h4 + mac.upper()
        return_msg = DeviceManager().sendAPDUStr(apdu)
        if return_msg["statCode"].sw1 == '90' and return_msg["statCode"].sw2 == '00':
            print('TEST_MODIFY_PIN SUCCESS')
        else :
            print("TEST_MODIFY_PIN FALSE")
            return False

    def PBOC_3DES_MAC (self,Key,IV,data):
        # 把Key分成二半，前8字节KeyL和后8字节KeyR
        keyL = Key[0:16]
        keyR = Key[-16:]

        # 把data按8字节分组，如果最后一组不够8字节，在最后一组末尾补一个80和若干个00，直到8字节；
        if len(data) % 16 != 0:
            data = data + '80'
        while (len(data) % 16 != 0):
            data = data + '00'
        n = 16
        l = []
        for each in ([data[i:i + n] for i in list(range(0, len(data), n))]):
            l.append(each)
        xordata = self.XOR(l[0], IV)
        for each in list(range(1, len(l))):
            xordata = self.XOR(l[each], xordata)

        k = pyDes.des(bytes.fromhex(keyL), pyDes.CBC, b"\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_NORMAL)
        m1 = binascii.hexlify(k.encrypt(bytes.fromhex(xordata))).decode('utf-8')

        k = pyDes.des(bytes.fromhex(keyR), pyDes.CBC, b"\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_NORMAL)
        m2 = binascii.hexlify(k.decrypt(bytes.fromhex(m1))).decode('utf-8')

        k = pyDes.des(bytes.fromhex(keyL), pyDes.CBC, b"\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_NORMAL)
        m3 = binascii.hexlify(k.encrypt(bytes.fromhex(m2))).decode('utf-8')[0:8]

        return m3

    def XOR(self,data_0, data_1):
        a = bytearray(bytes.fromhex(data_0))
        b = bytearray(bytes.fromhex(data_1))
        if int(len(a)) == int(len(b)):
            for i in range(len(a)):
                a[i] = a[i] ^ b[i]
        r = binascii.hexlify(a).decode('utf8')  # bytes --> 16进制字符串
        return r.upper()

    @staticmethod
    def getInfo():
        return "测试修改 PIN"

    @staticmethod
    def getTestType():
        return TestType.TEST_MODIFY_PIN