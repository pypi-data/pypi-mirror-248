#!/usr/bin/python
"""
@Author  :  Lijiawei
@Date    :  2022/11/26 3:55 下午
@Desc    :  tools line.
"""
import os
import stat


def make_file_executable(file_path):
    """
    If the path does not have executable permissions, execute chmod +x
    :param file_path:
    :return:
    """
    if os.path.isfile(file_path):
        mode = os.lstat(file_path)[stat.ST_MODE]
        executable = True if mode & stat.S_IXUSR else False
        if not executable:
            os.chmod(file_path, mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        return True
    return False


def log2list(log_file: str):
    """
    转换日志文件为列表
    :param log_file:
    :return:
    """
    # 读取日志文件内容
    with open(log_file) as file:
        log_content = file.read()

    crash_entries = log_content.split("\n\n")

    # 用于存储所有崩溃信息的列表
    crashes = []

    for entry in crash_entries:
        # 提取崩溃信息
        crash_start = entry.find("crash:")
        crash_end = entry.find("crashend")
        crash_info = entry[crash_start:crash_end]

        # 提取崩溃时间
        date_start = crash_info.find("(dump time: ") + len("(dump time: ")
        date_end = crash_info.find(")", date_start)
        crash_time = crash_info[date_start:date_end].replace("\n", "").replace("\t", "")

        # 提取崩溃堆栈信息
        stack_trace_start = crash_info.find("Long Msg:") + len("Long Msg:")
        stack_trace = crash_info[stack_trace_start:].replace("\n", "").replace("\t", "")

        formatted_text_crash_time = [
            {"line" + str(i + 1): line.strip()}
            for i, line in enumerate(crash_time.split("// "))
        ]
        formatted_text_stack_trace = [
            {"line" + str(i + 1): line.strip()}
            for i, line in enumerate(stack_trace.split("// "))
        ]

        # 构造JSON对象并添加到列表中
        crash_data = {
            "crash_time": formatted_text_crash_time,
            "stack_trace": formatted_text_stack_trace,
        }
        crashes.append(crash_data)

    return crashes
