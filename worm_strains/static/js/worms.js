$(document).ready(function() {
  if ($("body#worms").length) {
    fixWormsTopRow();
  }
})

fixWormsTopRow = function() {
  var tableOffset = $("body#worms table").offset().top;
  var header = $("body#worms table thead").clone();
  var fixedHeader = $("body#worms #table-thead-fixed").append(header);
  setFixedHeaderSize();

  $(window).resize(setFixedHeaderSize);

  $(window).bind("scroll", function() {
    var scrollDistance = $(this).scrollTop();
    if (scrollDistance >= tableOffset && fixedHeader.is(":hidden")) {
      fixedHeader.show();
    } else if ((scrollDistance < tableOffset) && fixedHeader.is(":visible")) {
      fixedHeader.hide();
    }
  });

  function setFixedHeaderSize() {
    var tableWidth = $("#worm-table").outerWidth();
    fixedHeader.width(tableWidth);
  }
}
