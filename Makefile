PYTHON=python
SRC_DIR=src
RAW_DATA_DIR=data/raw
PROCESSED_DATA_DIR=data/processed
ZIPS_DIR=data/zips
FEATURES_DIR=data/features

LANGUAGES=
DATA_SIZE=
FEATURES=

.PHONY: all download preprocess extract clean-zips list-languages

all:
	@echo "Available commands:"
	@echo "make download LANGUAGES=<languages> DATA_SIZE=<size_in_GB> [RAW_DATA_DIR=<path_to_save_raw_data>]" 
	@echo "make preprocess LANGUAGES=<languages> [RAW_DATA_DIR=<path_to_raw_data>] [PROCESSED_DATA_DIR=<path_to_preprocessed_data>]"
	@echo "make extract LANGUAGES=<languages> FEATURES=<feature_list> [PROCESSED_DATA_DIR=<path_to_preprocessed_data>] [FEATURES_DIR=<path_to_features>]"
	@echo "make clean-zips [ZIPS_DIR=<path_to_zip_files>]"
	@echo "make list-languages"

download:
	$(PYTHON) $(SRC_DIR)/download_data.py --languages $(LANGUAGES) --size $(DATA_SIZE) --destination $(RAW_DATA_DIR) --zips-dir $(ZIPS_DIR)

preprocess:
	$(PYTHON) $(SRC_DIR)/preprocess_data.py --languages $(LANGUAGES) --source $(RAW_DATA_DIR) --destination $(PROCESSED_DATA_DIR)

extract:
	$(PYTHON) $(SRC_DIR)/extract_features.py --languages $(LANGUAGES) --source $(PROCESSED_DATA_DIR) --destination $(FEATURES_DIR) --features $(FEATURES)

clean-zips:
	$(PYTHON) $(SRC_DIR)/download_data.py --clean-zips --zips-dir $(ZIPS_DIR)

list-languages:
	$(PYTHON) $(SRC_DIR)/download_data.py --list-languages

