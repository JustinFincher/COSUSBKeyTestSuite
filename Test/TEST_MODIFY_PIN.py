from Data.Test import *
from Controller.Helper import *
import pyDes
from Test.TEST_VALIDATE_PIN import *
from Controller.DeviceManager import  import *

class TEST_MODIFY_PIN(Test):


    def run(self,new_pin):
        pin = "1234"
        hexifiedPin = Helper().getMd5HashHex(new_pin)
        print(hexifiedPin)
        hexifiedPin.upper().replace("FF", "FE")
        print(hexifiedPin)

        randomMsg = Helper().getChallengeMsg()
        if randomMsg == None:
            print("TEST_MODIFY_PIN FALSE")
            return False

        m = hashlib.md5()
        m.update(new_pin.encode('utf-8'))
        h = m.hexdigest().lower()
        h.replace('ff', 'fe')
        h1 = '5500' + h
        h2 = str(hex(int(len(h1) / 2)))[2:] + h1
        k = pyDes.triple_des(bytes.fromhex('12345678214365871122aabb3344cdef'), pyDes.ECB, b"\0\0\0\0\0\0\0\0",
                             pad=None, padmode=pyDes.PAD_PKCS5)
        h3 = binascii.hexlify(k.encrypt(bytes.fromhex(h2))).decode('utf-8')
        h40 = '84F40900' + str(hex(int(len(h3) / 2)))[2:] + h3.upper()
        h41 = '84F40900' + str(hex(int(len(h3) / 2)))[2:] + h3.upper()
        keyL = '12345678214365871122aabb3344cdef'[0:16]
        keyR = '12345678214365871122aabb3344cdef'[-16:]
        if len(h41) % 16 != 0:
            h41 = h41 + '80'
        while (len(h41) % 16 != 0):
            h41 = h41 + '00'
        n = 16
        l = []
        for each in ([h41[i:i + n] for i in list(range(0, len(h41), n))]):
            l.append(each)
        xordata = self.XOR(l[0], randomMsg)
        for each in list(range(1, len(l))):
            xordata = self.XOR(l[each], xordata)

        k = pyDes.des(bytes.fromhex(keyL), pyDes.CBC, b"\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_NORMAL)
        m1 = binascii.hexlify(k.encrypt(bytes.fromhex(xordata))).decode('utf-8')

        k = pyDes.des(bytes.fromhex(keyR), pyDes.CBC, b"\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_NORMAL)
        m2 = binascii.hexlify(k.decrypt(bytes.fromhex(m1))).decode('utf-8')

        k = pyDes.des(bytes.fromhex(keyL), pyDes.CBC, b"\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_NORMAL)
        m3 = binascii.hexlify(k.encrypt(bytes.fromhex(m2))).decode('utf-8')[0:8]

        apdu = h40 + m3
        return_msg = DeviceManager.sendAPDUStr(apdu)
        if return_msg["statCode"].sw1 == '90' and return_msg["statCode"].sw2 == '00':
            print('TEST_MODIFY_PIN SUCCESS')
        else :
            print("TEST_MODIFY_PIN FALSE")
            return False



    def XOR(self,data_0, data_1):
        a = bytearray(bytes.fromhex(data_0))
        b = bytearray(bytes.fromhex(data_1))
        if int(len(a)) == int(len(b)):
            for i in range(len(a)):
                a[i] = a[i] ^ b[i]
        r = binascii.hexlify(a).decode('utf8')  # bytes --> 16进制字符串
        return r.upper()