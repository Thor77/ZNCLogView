# -*- coding: utf-8 -*-
import datetime
import os
from shutil import rmtree

import pytest

from znclogs.parser import Channel, Log, Network, collect_logs

test_logpath = 'znclogs/tests/znclogs'


@pytest.fixture
def logpath(request):
    def cleanup():
        rmtree(test_logpath)
    request.addfinalizer(cleanup)
    # create log-root
    os.makedirs(test_logpath)
    # create one network
    network1_path = os.path.join(test_logpath, 'network1')
    os.mkdir(network1_path)
    # create two channel
    channel1_path = os.path.join(network1_path, 'channel1')
    channel2_path = os.path.join(network1_path, 'channel2')
    os.mkdir(channel1_path)
    os.mkdir(channel2_path)
    # create log-files
    logfile_name = '2017-01-1.log'
    open(os.path.join(channel1_path, logfile_name), 'w').close()
    open(os.path.join(channel2_path, logfile_name), 'w').close()
    return test_logpath


def test_collect_logs(logpath):
    assert collect_logs(logpath) == [
        Network(
            name='network1',
            channel=[
                Channel(
                    name='channel1',
                    logs=[
                        Log(
                            date=datetime.datetime(2017, 1, 1, 0, 0),
                            content=''
                        )
                    ]
                ),
                Channel(
                    name='channel2',
                    logs=[
                        Log(
                            date=datetime.datetime(2017, 1, 1, 0, 0),
                            content=''
                        )
                    ]
                )
            ]
        )
    ]
