
import configparser
from collections import OrderedDict


def read_config(file):
    config = configparser.ConfigParser()
    config.read('config.ini')
    nodes = {'mnode': ['mnode', ''], 'node': OrderedDict(), 'xnode': {}}
    for i in config['DEFAULT']['nodes'].split(','):
        node = i.split()
        color = node[1] if len(node) > 1 else ''
        if node[0][0] == 'm':
            nodes['mnode'] = [node[0][1:13].zfill(12), color]
        elif node[0][0] == 'x':
            nodes['xnode'][node[0][1:13].zfill(12)] = color
        else:
            nodes['node'][node[0][:12].zfill(12)] = {'color': color}

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    cfg = config['DEFAULT']
    nodes = cfg['nodes']
    print(cfg['port'])
