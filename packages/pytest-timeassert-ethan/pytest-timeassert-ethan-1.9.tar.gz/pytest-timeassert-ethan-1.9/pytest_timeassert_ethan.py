# -*- coding: utf-8 -*-
# Author : Ethan
# Time : 2023/12/11 11:04
import time
import pytest
def pytest_configure(config):  # noqa
    config.addinivalue_line(
        "markers", "timeassert: run timeout"
    )

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    global time_value
    time_value = float('inf')

    if "timeassert" in item.keywords:
        timeout = item.keywords.get('timeassert', None)
        if timeout:
            time_value = timeout.args[0]
        else:
            time_value = float('inf')
    else:pass

    # print('------------测试开始执行，有三这个步骤------------------------')
    # 获取钩子方法的调用结果，返回一个result对象
    out = yield
    # print('用例执行结果', out)
    # 从钩子方法的调用结果中获取测试报告
    report = out.get_result()

    if report.when == "call":
        execution_time = call.stop - call.start
        if report.outcome == "passed" and execution_time >= time_value:
            report.outcome = "failed"
        else:pass
    else:pass


