# -*    coding: utf-8 -*-

import subprocess
import platform
import time


class AdbUtils:

    def __init__(self, adb_path="", adb_device_id="", encoding="", line_char=""):
        system = platform.system()
        self.__adbPath = adb_path
        
        if (adb_device_id == ""):
            self.__adb_deviceID = ""
        else:
            self.__adb_deviceID = "-s %s" % adb_device_id
        
        if line_char != "":
            self.__linechar = line_char
        elif system == "Windows":
            self.__linechar = "\r\n"
        elif system == "Linux":
            self.__linechar = "\n"
        elif system == "MacOS":
            self.__linechar = "\r"
        else:
            self.__linechar = "\n"
            
        if encoding != "":
            self.__encoding = encoding
        elif system == "Windows":
            self.__encoding = "ansi"
        else:
            self.__encoding = "utf8"

    @property
    def adbPath(self):
        """ adbPath 属性 读"""
        return self.__adbPath

    @adbPath.setter
    def adbPath(self, adb_path):
        """ adbPath 属性 写"""
        self.__adbPath = adb_path

    @property
    def adbDeviceID(self):
        """ adbDeviceID 属性 读"""
        return self.__adb_deviceID

    @adbDeviceID.setter
    def adbDeviceID(self, device_id):
        """ adbDeviceID 属性 写"""
        self.__adb_deviceID = device_id

    def __findAll(self, line_txt, find_txt):
        line_txt = line_txt.split(self.__linechar)
        find_ok = []
        for i in line_txt:
            if i.find(find_txt) >= 0:
                find_ok.append(i)
        return find_ok

    def adbCmd(self, args):
        """ adb 命令 """
        cmd = "%s %s" % (self.__adbPath, str(args))
        pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = str(pipe.stdout.read(), encoding=self.__encoding)
        return result

    def adb(self, args):
        """ adb 带 deviceID 命令 """
        return self.adbCmd("%s %s" % (self.__adb_deviceID, str(args)))

    def shell(self, args):
        """ adb shell 带 deviceID 命令 """
        return self.adbCmd("%s shell %s" % (self.__adb_deviceID, str(args)))

    def startServer(self):
        """ 启动 adb 服务 """
        return self.adbCmd("start-server")

    def killServer(self):
        """ 停止 adb 服务 """
        return self.adbCmd("kill-server")

    def deviceState(self):
        """ 获取设备状态： offline | bootloader | device """
        return self.adb("get-state")

    def deviceID(self):
        """ 获取设备id号，return serialNo """
        return self.adb("get-serialno")

    def deviceList(self):
        """ 获取设备列表 """
        devs = self.__findAll(self.adbCmd("devices"), "\t")
        result = []
        for i in devs:
            dev = []
            a = i.split("\t")
            dev.append(a[0])
            dev.append(a[1])
            result.append(dev)
        return result

    def setListenPort(self, port):
        """ 设置设备中的监听端口 ，通过无线连接调试模式设置为 5555 """
        return self.shell("tcpip %s" % (str(port)))

    def connectDevice(self, ip):
        """
        通过 IP 地址连接设备
        设备的 IP 地址，一般能在[设置]-[关于手机]-[状态信息]-[IP地址]找到
        """
        return self.adbCmd("connect %s" % ip)

    def disconnectDevice(self, ip):
        """ 断开无线连接的设备 """
        return self.adbCmd("disconnect %s" % ip)

    def androidVersion(self):
        """ 获取设备中的Android版本号，如4.2.2 """
        return self.shell("getprop ro.build.version.release")

    def sdkVersion(self):
        """ 获取设备SDK版本号 """
        return self.shell("getprop ro.build.version.sdk")

    def deviceModel(self):
        """ 获取设备型号 """
        return self.shell("getprop ro.product.model")

    def reboot(self):
        """ 重启设备 """
        self.adb("reboot")

    def fastboot(self):
        """ 进入fastboot模式 """
        self.adb("reboot bootloader")

    def __packageList(self, args):
        packages = self.__findAll(self.shell(args), "package")
        apps = []
        for i in packages:
            s = i.split(":") 
            apps.append(s[1])
        return apps

    def systemAppList(self):
        """ 获取设备中安装的系统应用包名列表 """   
        return self.__packageList("pm list packages -s")

    def thirdAppList(self):
        """ 获取设备中安装的第三方应用包名列表 """
        return self.__packageList("pm list packages -3")

    def matchAppList(self, keyword):
        """
        模糊查询与 keyword 匹配的应用包名列表
        例子: matchAppList("qq")
        """
        return self.__packageList("pm list packages %s" % keyword)

    def appStartTotalTime(self, component):
        """
        获取启动应用所花时间
        例子: appStartTotalTime("com.android.settings/.Settings")
        """
        time = self.shell("am start -W %s " % (component))
        return time

    def installApp(self, appFile):
        """
        安装app，app名字不能含中文字符
        例子: installApp("d:\\qq.apk")
        """
        return self.adb("install %s" % appFile)

    def isInstall(self, packageName):
        """
        判断应用是否安装，已安装返回True，否则返回False
        例子: isInstall("com.android.settings")
        """
        return len(self.matchAppList(packageName)) != 0

    def removeApp(self, packageName):
        """
        卸载应用
        packageName: 应用包名，非apk名
        """
        return self.adb("uninstall %s" % packageName)

    def clearAppData(self, packageName):
        """
        清除应用用户数据
        packageName: 应用包名，非apk名
        """
        return self.shell("pm clear %s" % packageName)

    def startActivity(self, component):
        """
        启动一个Activity
        例子: startActivity("com.tencent.mm/.ui.LauncherUI")，表示调起微信主界面
        """
        return self.shell("am start -n %s" % component)

    def __currentPackageAndActivity(self, pack_tcti):
        dump = self.shell("dumpsys window w")
        str_line = dump.split(self.__linechar)
        pa = []
        for i in str_line:
            if (i.find("mCurrentFocus=Window") >= 0):
                pa = i.split(" ")
        if (len(pa) > 4):
            pa = pa[4].split("}")[0]
        result_list = pa.split("/")
        result = ""
        if (len(result_list) > pack_tcti):
            result = result_list[pack_tcti]
        return result

    def currentPackage(self):
        """ 获取当前运行应用的 package """
        return self.__currentPackageAndActivity(0)   

    def currentActivity(self):
        """ 获取当前运行应用的 activity """
        return self.__currentPackageAndActivity(1)

    def startWebpage(self, url):
        """
        例子系统默认浏览器打开一个网页
        例子: startWebpage("http://www.baidu.com")
        """
        return self.shell("am start -a android.intent.action.VIEW -d %s" % url)

    def callPhone(self, number):
        """
        启动拨号器拨打电话
        例子: callPhone(10010)
        """
        self.shell("am start -a android.intent.action.CALL -d tel:%s" % str(number))

    def screenResolution(self):
        """
        获取设备屏幕分辨率，返回：width, high
        """
        a = self.__findAll(self.shell("dumpsys display"), "mStableDisplaySize")
        s = a[0]
        result = []
        size = s.split(",")
        result.append(size[0].split("(")[-1])
        result.append(size[1].split(")")[0])
        result[1] = result[1].split(" ")[-1]
        return result

    def batteryInfo(self, args):
        """
        Args args（字符串）：
        status：获取电池充电状态
        health：健康状态
        level：电池电量百分比
        temperature：温度
        
        获取电池充电状态
        1：未知状态
        2：充电状态
        3：放电状态
        4：未充电
        5：充电已满
        
        例子: batteryInfo("level")
        """
        a = self.__findAll(self.shell("dumpsys battery"), args)
        val = 0
        if len(a) > 0:
            val = a[0].split(": ")[-1]
        return val

    def pressKey(self, keycode):
        """
        发送一个按键事件
        keycode: http://developer.android.com/reference/android/view/KeyEvent.html
        例子: pressKey(keycode.HOME)
        """
        self.shell("input keyevent %s" % str(keycode))
        time.sleep(0.5)

    def longPressKey(self, keycode):
        """
        发送一个按键长按事件，Android 4.4以上
        keycode: http://developer.android.com/reference/android/view/KeyEvent.html
        例子: longPressKey(keycode.HOME)
        """
        self.shell("input keyevent --longpress %s" % str(keycode))
        time.sleep(0.5)

    def touch(self, x, y):
        """
        点击屏幕的某个坐标位置
        """
        self.shell("input tap %s %s" % (str(x), str(y)))
        time.sleep(0.5)

    def swipe(self, start_x, start_y, end_x, end_y, duration=""):
        """
        滑动事件，Android 4.4以上可选 duration(ms)(持续时间)
        例子:  swipe(800, 500, 200, 500)
        """
        self.shell("input swipe %s %s %s %s %s" % (str(start_x), str(start_y), str(end_x), str(end_y), str(duration)))
        time.sleep(0.5)

    def longTouch(self, x, y, duration=1000):
        """
        长按屏幕的某个坐标位置，duration(ms)(持续时间)
        """
        self.swipe(x, y, x, y, duration)

    def sendText(self, txt):
        """
        发送一段文本
        例子: sendText("i am unique")
        """
        self.shell("input text %s" % txt)
        time.sleep(0.5)

    def screencapToPhone(self, file_name):
        """截屏到手机"""
        self.shell("screencap -p %s" % file_name)

    def screencapToPc(self, file_name):
        """截屏到电脑"""
        self.shell("screencap -p > %s" % file_name)
        
