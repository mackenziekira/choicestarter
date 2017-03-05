var Main = {

	initialize: function() {
		// Fade in the page
		// document.getElementsByTagName("body")[0].classList.add('fade-in');

		// Bind stuff
		this._bindMethods();

		// Defaults
		this.defaults = {
			type: 'async',
			start: 'autostart',
			duration: 100,
			delay: '20',
			forceRender: false,
			dashGap: 200
		};

		// Options
		var options = this.overrideOptions({type: 'oneByOne', start: 'inViewport'});

		// Create Animations
		this.logoGraphic = this.createAnimation('logo-graphic', this.defaults, 'text-logo');
		// this.codeGraphic = this.createAnimation('code-graphic', options, 'text-code');
		// this.chaiGraphic = this.createAnimation('chai-graphic', options, 'text-chai');
	},

	createAnimation: function(svgEl, options, textEl) {
		return new Vivus(svgEl, options, function() {
			// this._setAnimateClass(textEl)
		}.bind(this));
	},

	overrideOptions: function(overrides) {
		var options = Object.assign( this._cloneObject(this.defaults), overrides);

		return options;
	},

	_bindMethods: function() {
		this.createAnimation = this.createAnimation.bind(this);
		this._cloneObject = this._cloneObject.bind(this);
		this.overrideOptions = this.overrideOptions.bind(this);
	},


	_setAnimateClass: function(animateId) {
		var animateEl = document.getElementById(animateId);
		animateEl.classList.add('animate-in');
	},

	_cloneObject: function(obj) {
	    if (obj === null || typeof obj !== 'object') {
	        return obj;
	    }

	    var options = obj.constructor(); // give options the original obj's constructor
	    for (var key in obj) {
	        options[key] = this._cloneObject(obj[key]);
	    }

	    return options;
	}

};

Main.initialize();


window.onbeforeunload = function() {
	window.scrollTo(0,0);
};
