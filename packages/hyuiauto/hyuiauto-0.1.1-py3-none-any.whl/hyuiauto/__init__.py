version = '0.1.1'

from ppadb.client import Client
from ppadb.device import Device as PPDevice
import os,time,platform
from pprint import pprint 
import pathlib
from functools import cached_property

TOOLS_DIR =  pathlib.Path(__file__).parent/'tools'
ADB_EXE = (TOOLS_DIR/'android'/'adb.exe').resolve() if platform.system() == 'Windows' else 'adb'
IME_APK = (TOOLS_DIR/'android'/'ADBKeyboard.apk').resolve()

class DeviceCommon:

    # def __init__(self) -> None:
    #     self.ocr = None


    @cached_property
    def ocr(self):
        # Getting called means no custom OCR, use default OCR
        from .ocr import CFG
        return CFG.Default_OCR()


    def screenToText(self):
        return self.ocr.imgToText(self.screenCap())

    def screenToTexts(self, view=False):
        ret = self.ocr.imgToTexts(self.screenCap())
        if view:            
            pprint(ret, indent=2)

        return ret
    
        # return result as the following format
        '''
        [ 
            [ [[468.0, 933.0], [610.0, 933.0], [610.0, 974.0], [468.0, 974.0]],  
                ('表格', 0.9990993738174438)],
            [ [[812.0, 936.0], [979.0, 936.0], [979.0, 969.0], [812.0, 969.0]],  
                ('幻灯片', 0.999191403388977)],
            [ [[489.0, 2183.0], [591.0, 2183.0], [591.0, 2237.0], [489.0, 2237.0]],
                ('取消', 0.9738937616348267)]
        ]'''

    def textPosOnScreen(self, text:str, ocrRet=None):
        if ocrRet is None:
            ocrRet = self.screenToTexts() 

        for one in ocrRet:
            coordinates, ele = one
            name, confidence = ele
            if text == name.strip():
                x = (coordinates[0][0] + coordinates[1][0])/2
                y = (coordinates[0][1] + coordinates[2][1])/2
                return (x,y)
               
        return None
    
    def waitForTextOnScreen(self, text:str,timeout=10):
        startTime = time.time()

        while True:
            pos = self.textPosOnScreen(text)
            if pos:
                return pos

            time.sleep(0.5)
            curTime = time.time()
            if (curTime-startTime) > timeout:
                raise RuntimeError(f'`{text}` does not appear on screen in {timeout} seconds')
            
    def waitForTextNotOnScreen(self, text:str,timeout=10):
        startTime = time.time()

        while True:
            pos = self.textPosOnScreen(text)
            if not pos:
                return
        
            time.sleep(0.5)
            curTime = time.time()
            if (curTime-startTime) > timeout:
                raise RuntimeError(f'`{text}` remain on screen for {timeout} seconds')
            
    def tapTextOnScreen(self, text:str,ocrRet=None, exact=True):
        if ocrRet is None:
            ocrRet = self.screenToTexts() 

        # pprint(ocrRet, indent=2)
        # print('-------------------')
        for one in ocrRet:
            # print(one)
            coordinates, ele = one
            name, confidence = ele
            # print(name,coordinates)
            
            compareRet = text == name.strip() if exact else text in name.strip()
            if compareRet:
                x = (coordinates[0][0] + coordinates[1][0])/2
                y = (coordinates[0][1] + coordinates[2][1])/2
                print(f'click on { x,y }')
                self.tap(x,y)
                break
        else:
            raise RuntimeError(f'`{text}` not on screen')
    

class AndroidDevice(PPDevice, DeviceCommon):
    def __init__(self, device):
        # super().__init__(device.client, device.serial)        
        PPDevice.__init__(self, device.client, device.serial)
        DeviceCommon.__init__(self)

        self.tap = self.input_tap
        self.swipe = self.input_swipe
        self.keyEvent = self.input_keyevent

    def screenCap(self):
        scrPng = bytes(super().screencap())
        #with open('tmp.png','wb') as f:
        #    f.write(scrPng)
        return scrPng
        
    def openApp(self, packageName:str):
        self.shell(f'monkey -p {packageName} 1')

    def installInputApk(self):
        if self.shell('pm list packages com.android.adbkeyboard'):
                print('adbkeyboard IME already installed')
                # pass

        else:
            print('adbkeyboard IME not installed, install', IME_APK)
            self.install(IME_APK)
            time.sleep(1.5)

        self.shell('ime enable  com.android.adbkeyboard/.AdbIME')
        self.shell('ime set com.android.adbkeyboard/.AdbIME')

        time.sleep(1)
        
    def inputString(self, inStr, endWithOK=False):
        cmd = f'am broadcast -a ADB_INPUT_TEXT --es msg "{inStr}"'
        self.shell(cmd)

        if endWithOK:
            self.shell('am broadcast -a ADB_EDITOR_CODE --ei code 2')
            self.shell('am broadcast -a ADB_EDITOR_CODE --ei code 6')
            # https://developer.android.com/reference/android/view/KeyEvent
            # self.input_keyevent('input keyevent 66')



class AndroidConnector(Client):
    def __init__(self, host='127.0.0.1', port=5037):
        self.host = host
        self.port = port

        try:
            conn = self.create_connection(timeout=1)
        except: 
            # print('adb server not running, try to lauch it...',end='')
            os.system(f'"{ADB_EXE}" -a start-server')
            print('ok')
            
            try:
                conn = self.create_connection(timeout=1)
            except: 
                print('adb server start failed!')
                raise RuntimeError("ERROR: adb server start failed!")
            
        conn.close()
    
    def devices(self) -> list[AndroidDevice]:
        return [AndroidDevice(device) for device in super().devices()]
    
    def firstDevice(self, installInputApk=True) -> AndroidDevice:
        devices = self.devices()
        if not devices :
            return None
    
        if installInputApk:
            devices[0].installInputApk()
        
        return devices[0]


def showCurrentAppPackageName(debug=False,lines=1):
    import re
    pat = 'cmp=(?P<pack>.+)/(?P<act>.+)}'
    
    ac = AndroidConnector()
    device = ac.firstDevice(installInputApk=False)
    output = device.shell(f"dumpsys activity recents | grep 'intent={{' | head -n{lines}")
    for line in output.splitlines():
        if 'intent={' in line:
            if debug:
                print(line)
            for one in re.finditer(pat, line):
                print(f"package  : {one.group('pack')}\nactivity : {one.group('act')}")

            if lines > 1:
                print('\n-----------------\n')
