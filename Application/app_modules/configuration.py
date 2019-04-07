import ConfigParser

config = ConfigParser.RawConfigParser()

config.read('config.ini')

CUCKOO_SERVER = config.get('locations', 'cuckoo_server')
SAMPLE_DIRECTORY = config.get('locations', 'sample_directory')
DATASET_DIRECTORY = config.get('locations', 'dataset_directory')
MODEL_DIRECTORY = config.get('locations', 'model_directory')
CUCKOO_EXPORT_DIRECTORY = config.get('locations', 'cuckoo_export_directory')
REPORTS_DIRECTORY = config.get('locations', 'reports_directory')

def reloadConfig():
    CUCKOO_SERVER = config.get('locations', 'cuckoo_server')
    SAMPLE_DIRECTORY = config.get('locations', 'sample_directory')
    DATASET_DIRECTORY = config.get('locations', 'dataset_directory')
    MODEL_DIRECTORY = config.get('locations', 'model_directory')
    CUCKOO_EXPORT_DIRECTORY = config.get('locations', 'cuckoo_export_directory')
    REPORTS_DIRECTORY = config.get('locations', 'reports_directory')
