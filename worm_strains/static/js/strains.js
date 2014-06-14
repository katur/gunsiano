$(document).ready(function() {
  if ($("body#strains").length) {
    fixStrainsTopRow();
  }
})

fixStrainsTopRow = function() {
  var tableOffset = $("body#strains table").offset().top;
  var header = $("body#strains table thead").clone();
  var fixedHeader = $("body#strains #table-thead-fixed").append(header);

  $(window).bind("scroll", function() {
    var scrollDistance = $(this).scrollTop();
    if (scrollDistance >= tableOffset && fixedHeader.is(":hidden")) {
      var tableWidth = $("#strain-table").outerWidth();
      fixedHeader.width(tableWidth);
      console.log(tableWidth);
      fixedHeader.show();
    } else if ((scrollDistance < tableOffset) && fixedHeader.is(":visible")) {
      fixedHeader.hide();
    }
  });
}
