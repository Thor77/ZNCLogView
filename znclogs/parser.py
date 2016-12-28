import os
from collections import namedtuple
from datetime import datetime

Network = namedtuple('Network', ['name', 'channel'])
Channel = namedtuple('Channel', ['name', 'logs'])
Log = namedtuple('Log', ['date', 'content'])
logfile_datetime_format = '%Y-%m-%d.log'


def collect_logs(log_path):
    '''
    Collect all log-files in `log_path`

    :param log_path: path to moddata of log (without seperator-suffix)
    '''
    networks = [
        Network(network_directory.name, [
            Channel(channel_directory.name, [
                Log(
                    datetime.strptime(log_file.name, logfile_datetime_format),
                    open(log_file.path).read()
                )
                for log_file in
                os.scandir(channel_directory.path)
            ])
            for channel_directory in
            os.scandir(network_directory.path)
        ])
        for network_directory in
        os.scandir(log_path)
    ]
    return networks
