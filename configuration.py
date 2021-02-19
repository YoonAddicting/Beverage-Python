import configparser
from pathlib import Path


def open_config_file(filename: Path):
    config = configparser.ConfigParser()
    config.read(filename.absolute())

    return config


def create_default_config(filename: Path):
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'Fullscreen': 'False',
                         'PasswordEnabled': 'False',
                         'Password': 'b\'$2b$12$jg7IfKUyAsYuTazdeQb2ZesmxByGzkUwAsVybpNaPh8Vcn5WPSsLu\'',
                         'DatabaseFileName': 'database.sqlite',
                         'DatabaseBackupEnabled': 'False',
                         'DatabaseBackupLocation': './Backups'
                         }
    with filename.open('w') as configfile:
        config.write(configfile)
    return config
