import os
from dotenv import load_dotenv
import yaml
import configparser


class Config(object):
    def __init__(self, config_dir, *args, **kwargs):        
        self.BASE_DIR = config_dir        
        self.yaml_file_data = self.read_yaml_file(self.BASE_DIR+'/config.yaml')
        self.ini_file_data = self.read_ini_file(self.BASE_DIR+'/config.ini')
        self.env_file_data = None #self.read_env_file(self.BASE_DIR+'/.env')
        self.env_data = os.environ


        if self.yaml_file_data:
            self.set_attributes(self.yaml_file_data)
        if self.ini_file_data:
            self.set_attributes(self.ini_file_data)
        if self.env_file_data:
            self.set_attributes(self.env_file_data)
        if self.env_data:
            self.set_attributes(self.env_data)

    def set_attributes(self, data):
        for key, value in dict(data).items():
            setattr(self, key, value)

    def read_yaml_file(self, yaml_file_path):
        try:
            with open(yaml_file_path, 'r') as stream:
                try:
                    return yaml.safe_load(stream)
                except yaml.YAMLError as exc:
                    print(exc)
                    return None
        except Exception as e:           
            return None       
            
    def read_ini_file(self, ini_file_path):
        try:
            config = configparser.ConfigParser()
            config.optionxform = str
            config.read(ini_file_path)
            return config
        except Exception as exc:            
            return None
        
    
    def read_env_file(self, env_file_path):
        try:
            load_dotenv(env_file_path)
            return os.environ
        except Exception as e:
            print(e)
            return None    
        
        

#config = Config()

#__all__ = ['config']