import os
from collections import namedtuple

Network = namedtuple('Network', ['name', 'channel'])
Channel = namedtuple('Channel', ['name', 'logs'])


def collect_logs(log_path):
    '''
    Collect all log-files in `log_path`

    :param log_path: path to moddata of log (without seperator-suffix)
    '''
    networks = [
        Network(network_directory.name, [
            Channel(channel_directory.name, [
                log_file.path
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
