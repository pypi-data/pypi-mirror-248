import logging
import logging.config
import yaml
import os


current_dir = os.getcwd()

with open(current_dir+'/velib/logging.yaml', 'r') as file:
    config = yaml.safe_load(file.read())
    logging.config.dictConfig(config)

log = logging.getLogger('app')




