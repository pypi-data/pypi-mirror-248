==============
pytest-timeassert-ethan: pytest plugin
==============


**This pytest plugin will assert the execution time of the use case.**


Usage
=====

从github源码安装

   pip install git+https://github.com/AomiEthan/pytest-timeassert-ethan.git



demo
====

先写pytest用例test_demo.py

    @pytest.mark.timeassert(1)
    def test_01():
        time.sleep(1)

    @pytest.mark.timeassert(2)
    def test_02():
        time.sleep(1)
执行结果如下:

    def pytest_runtest_call(item):
        timeout = item.keywords.get('timeassert', None)
        if timeout:
            time_value = timeout.args[0]
            start_time = time.time()
            item.runtest()  # 执行测试用例
            end_time = time.time()
            assert end_time - start_time < float(time_value), "Test execution time exceeded the threshold"
            AssertionError: Test execution time exceeded the threshold
            assert (1702283295.8840106 - 1702283294.8729131) < 1.0
            +  where 1.0 = float(1)

