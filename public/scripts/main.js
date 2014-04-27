(function ($) {
  $(window).load(function () {
    $("#shen-container").waterfall({
      isResizable:true,
      columnCount: 2,
      selector: ".item"
    });
  });
})(jQuery);