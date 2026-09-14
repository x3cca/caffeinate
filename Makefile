BUNDLE_PATH = "caffeinate@x3cca.github.com.zip"
EXTENSION_DIR = "caffeine@patapon.info"
EXTENSION_UUID = "caffeinate@x3cca.github.com"

all: build install

.PHONY: build install clean translations lint lint-fix

build:
	rm -f $(BUNDLE_PATH)
	cd $(EXTENSION_DIR); \
	gnome-extensions pack --force --podir=locale \
	                      --extra-source=preferences/ \
	                      --extra-source=icons/ \
	                      --extra-source=lidInhibitor.js \
	                      --extra-source=mprisMediaPlayer2.js; \
	mv $(EXTENSION_UUID).shell-extension.zip ../$(BUNDLE_PATH)

install:
	gnome-extensions install $(BUNDLE_PATH) --force

clean:
	@rm -fv $(BUNDLE_PATH)
	@rm -fv $(EXTENSION_DIR)/schemas/gschemas.compiled

translations:
	@./update-locale.sh

lint:
	npx eslint $(EXTENSION_DIR)

lint-fix:
	npx eslint --fix $(EXTENSION_DIR)
