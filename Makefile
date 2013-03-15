JS     	= $(filter-out gitdeployed/static/js/app.min.js, \
		  $(wildcard gitdeployed/static/js/*.js))
JS_MIN 	= gitdeployed/static/js/app.min.js
LESS   	= gitdeployed/static/css/app.less
CSS    	= gitdeployed/static/css/app.min.css

all: less js

less: $(CSS)

js: $(JS_MIN)

$(CSS): $(LESS)
	lessc -x $< $@

$(JS_MIN): $(JS)
	cat > $@ $^

clean:
	rm gitdeployed/static/js/app.min.js \
	   gitdeployed/static/css/app.min.css
