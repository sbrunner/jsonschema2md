# Babel configuration
DOMAIN = messages
SOURCE_DIR = jsonschema2md
LOCALES_DIR = jsonschema2md/locales
POT_FILE = $(LOCALES_DIR)/messages.pot

# Extract messages
extract:
	pybabel extract \
		--output-file=$(POT_FILE) \
		--sort-by-file \
		--add-comments=TL \
		--project=jsonschema2md \
		--keywords=t \
		$(SOURCE_DIR)

# Initialize a new language catalog (e.g., LANG=fr)
init:
	pybabel init \
		--domain=$(DOMAIN) \
		--input-file=$(POT_FILE) \
		--output-dir=$(LOCALES_DIR) \
		--locale=$(LANG)

# Update the existing catalogs
update:
	pybabel update \
		--domain=$(DOMAIN) \
		--input-file=$(POT_FILE) \
		--output-dir=$(LOCALES_DIR) \
		--ignore-obsolete

# Compile the catalogs
compile:
	pybabel compile \
		--domain=$(DOMAIN) \
		--directory=$(LOCALES_DIR) \
		--use-fuzzy

# Default tasks
all: extract update compile

# Clean
clean:
	rm -f $(POT_FILE)
	find $(LOCALES_DIR) -name "*.mo" -delete

.PHONY: extract init update compile all clean
