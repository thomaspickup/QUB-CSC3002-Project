import ConfigParser, os
config = ConfigParser.RawConfigParser()
config.read('config.ini')

# Used if the existing config file doesn't fit or if there isn't an existing config file
def createDefault():
    numberSection_expected = len(expected_sections)
    numberSection_settings = len(expected_settings)
    numberSection_default = len(default_values)
    sumCheck = numberSection_default + numberSection_expected + numberSection_settings

    # Checks to see if there is the same amount of sections in each
    if sumCheck / 3 == numberSection_default:
        for s in range(numberSection_expected):
            config.add_section(expected_sections[s])

            numberOfValues = len(expected_settings[s])

            for v in range(numberOfValues):
                config.set(expected_sections[s], expected_settings[s][v], default_values[s][v])

    writeConfig()

def errorCorrect():
    numberSection_expected = len(expected_sections)
    numberSection_settings = len(expected_settings)
    numberSection_default = len(default_values)
    sumCheck = numberSection_default + numberSection_expected + numberSection_settings
    hasError = False

    # Checks to see if there is the same amount of sections in each
    if sumCheck / 3 == numberSection_default:
        for s in range(numberSection_expected):
            numberOfValues = len(expected_settings[s])
            hasSection = config.has_section(expected_sections[s])

            if not hasSection:
                config.add_section(expected_sections[s])
                hasError = True

            for v in range(numberOfValues):
                hasOption = config.has_option(expected_sections[s], expected_settings[s][v])
                if not hasOption:
                    config.set(expected_sections[s], expected_settings[s][v], default_values[s][v])
                    hasError = True

    if hasError:
        writeConfig()

def writeConfig():
    with open('config.ini', 'w') as config_file:
        config.write(config_file)

expected_sections = ['locations', 'program']
expected_settings = [['cuckoo_server', 'cuckoo_server_port', 'sample_directory',
'dataset_directory', 'model_directory', 'cuckoo_export_directory',
'reports_directory'], ['r_location']]
default_values = [['localhost', '8090', r'C:\Sample',
r'C:\Dataset', r'C:\Model', r'C:\Cuckoo\Storage\Analyses',
r'C:\Reports'], [r'C:\Program Files\R\R-3.5.3\bin']]

# First Check if config.ini actually exists
configExists = os.path.isfile('config.ini')

if configExists:
    # Goes through and checks for errors and if there is add the default
    errorCorrect()

# if it doesn't then create a blank config file with the section locations
else:
    # Creates the default as file doesn't exist
    createDefault()

CUCKOO_SERVER = config.get('locations', 'cuckoo_server')
CUCKOO_SERVER_PORT = config.get('locations', 'cuckoo_server_port')
SAMPLE_DIRECTORY = config.get('locations', 'sample_directory')
DATASET_DIRECTORY = config.get('locations', 'dataset_directory')
MODEL_DIRECTORY = config.get('locations', 'model_directory')
CUCKOO_EXPORT_DIRECTORY = config.get('locations', 'cuckoo_export_directory')
REPORTS_DIRECTORY = config.get('locations', 'reports_directory')
R_LOCATION = config.get('program', 'r_location')
