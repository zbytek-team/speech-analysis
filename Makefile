PYTHON=python3
SRC_DIR=src
RAW_DATA_DIR=data/raw
ZIPS_DIR=data/zips
FEATURES_DIR=data/features

LANGUAGES=
DATA_SIZE=
FEATURES=

.PHONY: all download preprocess extract download_and_extract list-languages

all:
	@echo "Available commands:"
	@echo "make download LANGUAGES=<languages> DATA_SIZE=<size_in_GB> [RAW_DATA_DIR=<path_to_save_raw_data>]" 
	@echo "make extract LANGUAGES=<languages> [FEATURES=<feature_list>] [PROCESSED_DATA_DIR=<path_to_preprocessed_data>] [FEATURES_DIR=<path_to_features>]"
	@echo "make download_and_extract LANGUAGES=<languages> DATA_SIZE=<size_in_GB> [FEATURES=<feature_list>] [RAW_DATA_DIR=<path_to_save_raw_data>] [FEATURES_DIR=<path_to_features>]"
	@echo "make list-languages"
	@echo "make list-features"

download:
	$(PYTHON) $(SRC_DIR)/download_data.py --languages $(LANGUAGES) --size $(DATA_SIZE) --destination $(RAW_DATA_DIR) --zips-dir $(ZIPS_DIR)

extract:
	$(PYTHON) $(SRC_DIR)/extract_features.py --languages $(LANGUAGES) --source $(RAW_DATA_DIR) --destination $(FEATURES_DIR) --features $(FEATURES)

list-languages:
	$(PYTHON) $(SRC_DIR)/download_data.py --list-languages

list-features:
	$(PYTHON) $(SRC_DIR)/extract_features.py --list-features

download_and_extract:
	$(PYTHON) $(SRC_DIR)/download_data.py --languages $(LANGUAGES) --size $(DATA_SIZE) --destination $(RAW_DATA_DIR) --zips-dir $(ZIPS_DIR)
	$(PYTHON) $(SRC_DIR)/extract_features.py --languages $(LANGUAGES) --source $(RAW_DATA_DIR) --destination $(FEATURES_DIR) --features $(FEATURES)
