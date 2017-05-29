import os.path
from os import mkdir

from jinja2 import ChoiceLoader, Environment, FileSystemLoader, PackageLoader


def render_template(networks, output_directory):
    # create output-directory if not exists
    if not os.path.exists(output_directory):
        mkdir(output_directory)

    template_loader = ChoiceLoader([
        PackageLoader(__package__, 'templates'),
        FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates'))
    ])
    environment = Environment(loader=template_loader)
    # render index
    index_location = os.path.join(output_directory, 'index.html')
    environment.get_template('index.jinja2')\
            .stream(networks=sorted(networks, key=lambda n: n.name)).dump(index_location, encoding='utf-8')
    # render networks and channel
    networks_path = os.path.join(output_directory, 'networks')
    if not os.path.exists(networks_path):
        mkdir(networks_path)
    for network in sorted(networks, key=lambda n: n.name):
        network_path = os.path.join(networks_path, network.name)
        if not os.path.exists(network_path):
            mkdir(network_path)
        # render network-index
        environment.get_template('network_index.jinja2')\
            .stream(network=network)\
            .dump(os.path.join(network_path, 'index.html'))
        # render channel
        for channel in sorted(network.channel, key=lambda c: c.name):
            channel_path = os.path.join(network_path, channel.name.lstrip('#'))
            if not os.path.exists(channel_path):
                mkdir(channel_path)
            # render channel-index
            environment.get_template('channel_index.jinja2')\
                .stream(channel=channel)\
                .dump(os.path.join(channel_path, 'index.html'))
            # render log
            for log in sorted(channel.logs, key=lambda l: l.date):
                log_path = os.path.join(channel_path, str(log.date.timestamp()))
                environment.get_template('log.jinja2')\
                    .stream(log=log).dump(log_path + '.html')
