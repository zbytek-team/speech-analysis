# Constants for data download and processing
COMMONVOICE_API_URL = "https://commonvoice.mozilla.org/api/v1"
BYTES_PER_GB = 2**30

# Default directories
DEFAULT_RAW_DATA_DIR = "data/raw"
DEFAULT_PROCESSED_DATA_DIR = "data/processed"
DEFAULT_FEATURES_DIR = "data/features"
DEFAULT_ZIPS_DIR = "data/zips"

# Audio processing constants
DEFAULT_SILENCE_THRESHOLD = -16  # in dB
DEFAULT_MIN_SILENCE_LEN = 500    # in milliseconds

# Gender constants
GENDERS = ['male', 'female']

GENDER_MAP = {
    'male': 'male',
    'male_masculine': 'male',
    'female': 'female',
    'female_feminine': 'female'
}


