#!/usr/bin/python
"""
@Author  :  Lijiawei
@Date    :  2022/11/26 4:15 下午
@Desc    :  core line.
"""
import json
import os

from airtest.core.android.adb import ADB
from airtest.core.api import connect_device
from airtest.core.api import device
from airtest.core.api import install
from airtest.core.api import stop_app
from airtest.core.assertions import assert_equal
from airtest.core.error import AdbShellError
from airtest.core.helper import log

from macaque.tools import log2list

STATIC_PATH = os.path.dirname(os.path.realpath(__file__))
jar = os.path.join(STATIC_PATH, "jar")
libs = os.path.join(STATIC_PATH, "libs")


def prepare(
    udid, duration, package, throttle=800, whitelist=None, widget=None, ime=False
):
    """

    :param udid:
    :param duration:
    :param package:
    :param throttle:
    :param whitelist:
    :param widget:[{"bounds": "0.1,0.87,1,0.95"}]
    :param ime:
    :return:
    """
    connect_device(
        f"Android:///{udid}?cap_method=MINICAP&&ori_method=MINICAPORI&&touch_method=MAXTOUCH"
    )

    if ime:
        install(filepath="./ADBKeyBoard.apk", install_options="-g")

    serialno = device().serialno
    adb = ADB(serialno=serialno)
    # 静音
    log(arg="adb shell media volume --set 0", desc="macaque setup")
    try:
        adb.shell("media volume --set 0")
    except AdbShellError:
        pass
    # 推送 macaque 文件
    for j in os.listdir(jar):
        adb.push(os.path.join(jar, j), "/sdcard")

    # 推送 libs 文件
    for lib in os.listdir(libs):
        adb.push(os.path.join(libs, lib), "/data/local/tmp/")

    # bounds 边界设置
    if widget and not "":
        log(arg=widget, desc="自定义 macaque 屏蔽区域")
        with open(
            file=os.path.join(STATIC_PATH, "max.widget.black"),
            mode="w",
            encoding="utf-8",
        ) as f:
            widget_value = json.dumps([{"bounds": widget}])
            f.write(widget_value)
        # 推送 max.widget.black 到设备上
        adb.push(
            os.path.join(STATIC_PATH, "max.widget.black"), "/sdcard/max.widget.black"
        )

    # --act-whitelist-file /sdcard/awl.strings
    if whitelist and not "":
        log(arg=whitelist, desc="自定义 macaque 白名单")
        with open(
            file=os.path.join(STATIC_PATH, "awl.strings"), mode="w", encoding="utf-8"
        ) as f:
            for white in str(whitelist).split(","):
                f.write(white + "\n")
        # 推送 whitelist 到设备上
        adb.push(os.path.join(STATIC_PATH, "awl.strings"), "/sdcard/awl.strings")
        cmd = f"CLASSPATH=/sdcard/macaque.jar:/sdcard/framework.jar:/sdcard/macaque-thirdpart.jar exec app_process /system/bin com.android.commands.monkey.Monkey -p {package} --agent reuseq --running-minutes {duration} --throttle {throttle} -v -v --act-whitelist-file /sdcard/awl.strings --bugreport"
    else:
        cmd = f"CLASSPATH=/sdcard/macaque.jar:/sdcard/framework.jar:/sdcard/macaque-thirdpart.jar exec app_process /system/bin com.android.commands.monkey.Monkey -p {package} --agent reuseq --running-minutes {duration} --throttle {throttle} -v -v --bugreport"

    log(arg=cmd, desc="macaque 命令")

    os.system(f"{ADB.builtin_adb_path()} -s {udid} shell {cmd}")

    flag = 0
    oom = "/sdcard/oom-traces.log"
    crash = "/sdcard/crash-dump.log"
    if adb.exists_file(oom):
        flag = 1
        adb.pull(oom, STATIC_PATH)
        oom_log = log2list(os.path.join(STATIC_PATH, "oom-traces.log"))
        log(arg=oom_log, desc="存在 oom 异常")
        adb.shell(f"rm {oom}")
    else:
        log(f"不存在异常：{oom}")

    if adb.exists_file(crash):
        flag = 1
        adb.pull(crash, STATIC_PATH)
        crash_log = log2list(os.path.join(STATIC_PATH, "crash-dump.log"))
        for c in crash_log:
            crash_title = c.get("crash_time")[0].get("line1")
            log(arg=c, desc=f"crash: {crash_title}")
        adb.shell(f"rm {crash}")
    else:
        log(f"不存在异常：{crash}")

    # teardown
    if whitelist and not "":
        adb.shell(f"rm /sdcard/awl.strings")

    if widget and not "":
        adb.shell(f"rm /sdcard/max.widget.black")

    log(arg="rm /sdcard/macaque*", desc="macaque teardown")
    stop_app(package)

    if flag > 0:
        msg = "存在异常请检查 oom 或者 crash 日志"
    else:
        msg = "本次运行检测不存在异常"

    assert_equal(0, flag, msg)
