THEME_PATH = `/usr/bin/env python -c "import os, pinax_theme_bootstrap; print(os.path.dirname(pinax_theme_bootstrap.__file__))"`
THEME_STATIC_PATH = $(THEME_PATH)/static
BOOTSTRAP_JS_PATH = $(THEME_STATIC_PATH)/bootstrap/js
LESS_INCLUDE_PATH = $(THEME_STATIC_PATH)
LESS_COMPRESSOR ?= `which lessc`
SITE_LESS = ./less/site.less
JS_OUTPUT_PATH = ./js
JS_OUTPUT_FILENAME = $(JS_OUTPUT_PATH)/bootstrap.min.js
CSS_OUTPUT_FILENAME = site.css

#
# BUILD SITE STATIC
# npm install uglify-js less
#

build:
	mkdir -p js
	cat ${BOOTSTRAP_JS_PATH}/bootstrap-transition.js ${BOOTSTRAP_JS_PATH}/bootstrap-alert.js ${BOOTSTRAP_JS_PATH}/bootstrap-button.js ${BOOTSTRAP_JS_PATH}/bootstrap-carousel.js ${BOOTSTRAP_JS_PATH}/bootstrap-collapse.js ${BOOTSTRAP_JS_PATH}/bootstrap-dropdown.js ${BOOTSTRAP_JS_PATH}/bootstrap-modal.js ${BOOTSTRAP_JS_PATH}/bootstrap-tooltip.js ${BOOTSTRAP_JS_PATH}/bootstrap-popover.js ${BOOTSTRAP_JS_PATH}/bootstrap-scrollspy.js ${BOOTSTRAP_JS_PATH}/bootstrap-tab.js ${BOOTSTRAP_JS_PATH}/bootstrap-typeahead.js ${BOOTSTRAP_JS_PATH}/bootstrap-affix.js > ${JS_OUTPUT_PATH}/bootstrap.js
	rm -f ${JS_OUTPUT_FILENAME}
	echo "/*!\n* Bootstrap.js by @fat & @mdo\n* Copyright 2012 Twitter, Inc.\n* http://www.apache.org/licenses/LICENSE-2.0.txt\n*/" > ${JS_OUTPUT_FILENAME}
	uglifyjs ${JS_OUTPUT_PATH}/bootstrap.js -nc >> ${JS_OUTPUT_FILENAME}
	rm -f ${JS_OUTPUT_PATH}/bootstrap.js
	mkdir -p css
	lessc --yui-compress --include-path=${LESS_INCLUDE_PATH} ${SITE_LESS} > css/${CSS_OUTPUT_FILENAME}
