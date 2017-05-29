from configparser import ConfigParser

from znclogs.parser import collect_logs
from znclogs.render import render_template

if __name__ == '__main__':
    # read config
    config = ConfigParser()
    config.read('config.ini')
    networks = collect_logs(config['ZNC']['logdir'])
    render_template(networks, 'output')
