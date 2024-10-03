# Constants
PYTHON=python
SRC_DIR=src
DEST_DIR=data/raw
ZIPS_DIR=data/zips
FEATURES_DIR=data/features

# Variables that must be provided as arguments
LANGUAGES=
DATA_SIZE=
FEATURES=

.PHONY: all download preprocess extract clean-zips list-languages

# Show available commands
all:
	@echo "Available commands:"
	@echo "make download LANGUAGES=<languages> DATA_SIZE=<size_in_GB> DEST_DIR=<path_to_save_data>"
	@echo "make preprocess LANGUAGES=<languages> DEST_DIR=<path_to_preprocessed_data>"
	@echo "make extract LANGUAGES=<languages> FEATURES=<feature_list> DEST_DIR=<path_to_features>"
	@echo "make list-languages"
	@echo "make clean-zips"

# Download datasets
download:
	$(PYTHON) $(SRC_DIR)/download_data.py --languages $(LANGUAGES) --size $(DATA_SIZE) --destination $(DEST_DIR) --zips-dir $(ZIPS_DIR)

# Preprocess the data
preprocess:
	$(PYTHON) $(SRC_DIR)/preprocess_data.py --languages $(LANGUAGES) --source $(DEST_DIR) --destination $(DEST_DIR)

# Extract features
extract:
	$(PYTHON) $(SRC_DIR)/extract_features.py --languages $(LANGUAGES) --source $(DEST_DIR) --destination $(FEATURES_DIR) --features $(FEATURES)

# Clean up zip files
clean-zips:
	$(PYTHON) $(SRC_DIR)/download_data.py --clean-zips --zips-dir $(ZIPS_DIR)

# List available languages
list-languages:
	$(PYTHON) $(SRC_DIR)/download_data.py --list-languages

