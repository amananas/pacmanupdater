#!/usr/bin/env python3
import json
import os
import argparse
import pacmanupdater.main

parser = argparse.ArgumentParser()
parser.add_argument('packagesList', nargs='*')
parser.add_argument('-d', '--debug', action='store_true', default=False)
args = parser.parse_args()

with open(os.path.expanduser('~/.pacmanupdater/pacmanupdater.conf.json'), encoding='utf-8') as configFile:
    config = json.load(configFile)

pacmanupdater.main.configure(config['packages'],
                             includes=args.packagesList,
                             excludes=config['excludes'],
                             configDebug=args.debug)
pacmanupdater.main.run()
