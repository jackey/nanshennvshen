/**
 *  Plugin which is applied on a list of img objects and calls
 *  the specified callback function, only when all of them are loaded (or errored).
 *  @author:  H. Yankov (hristo.yankov at gmail dot com)
 *  @version: 1.0.0 (Feb/22/2010)
 *	http://yankov.us
 */

(function($) {
$.fn.batchImageLoad = function(options) {
	var images = $(this);
	var originalTotalImagesCount = images.size();
	var totalImagesCount = originalTotalImagesCount;
	var elementsLoaded = 0;

	// Init
	$.fn.batchImageLoad.defaults = {
		loadingCompleteCallback: null, 
		imageLoadedCallback: null
	}
    var opts = $.extend({}, $.fn.batchImageLoad.defaults, options);
		
	// Start
	images.each(function() {
		// The image has already been loaded (cached)
		if ($(this)[0].complete) {
			totalImagesCount--;
			if (opts.imageLoadedCallback) opts.imageLoadedCallback(elementsLoaded, originalTotalImagesCount);
		// The image is loading, so attach the listener
		} else {
			$(this).load(function() {
				elementsLoaded++;
				
				if (opts.imageLoadedCallback) opts.imageLoadedCallback(elementsLoaded, originalTotalImagesCount);

				// An image has been loaded
				if (elementsLoaded >= totalImagesCount)
					if (opts.loadingCompleteCallback) opts.loadingCompleteCallback();
			});
			$(this).error(function() {
				elementsLoaded++;
				
				if (opts.imageLoadedCallback) opts.imageLoadedCallback(elementsLoaded, originalTotalImagesCount);
					
				// The image has errored
				if (elementsLoaded >= totalImagesCount)
					if (opts.loadingCompleteCallback) opts.loadingCompleteCallback();
			});
		}
	});

	// There are no unloaded images
	if (totalImagesCount <= 0)
		if (opts.loadingCompleteCallback) opts.loadingCompleteCallback();
};
})(jQuery);

(function ($) {
    function blocksIt() {
        $(".body .wrapper .bg .items").BlocksIt({
          numOfCol: 2
        });
    }
    $(window).load(function () {
        blocksIt();
        $(".body .wrapper ").infinitescroll({
            navSelector: "div.navigation",
            nextSelector: "div.navigation a:first",
            itemSelector: ".body .wrapper .bg .items",
            appendCallbackFn: function (data) {
              var data = $(".items .item", $(data));
              if (data.size()) {
                data.css("height", 1);
                $(".body .wrapper .bg .items").append(data);
                $(".body .wrapper .bg .items").find('img').batchImageLoad({
                        loadingCompleteCallback: function () {
                          data.css("height", "auto");
                          blocksIt();
                        }
                });
              }
            },
            animate: true,
            loading: {
                msgText: "  ",
                start: function (opts) {
                  $(opts.navSelector).hide();
                  opts.loading.msg
                  .appendTo(opts.loading.selector)
                  .show(opts.loading.speed, $.proxy(function() {
                                          this.beginAjax(opts);
                                  }, this));
                },
                finished: function (opts) {
                    opts.loading.msg.hide();
                }
            }
        }, function (newDom) {
            var page_link = $("div.navigation a:first");
            var link = $(page_link).attr("href");
            var searches = link.toString().match(/[0-9]+$/);
            var page_num = searches[0];
            link = link.replace(/[0-9]+$/, parseInt(page_num) + 1);
            $(page_link).attr("href", link);
        });
    });
})(jQuery);