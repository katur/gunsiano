$(document).ready(function() {
  if ($("body#strains").length) {
    fixStrainsTopRow();
  }
})

fixStrainsTopRow = function() {
  var strainTable = $("#strain-table");
  var tableOffset = $("body#strains table").offset().top;
  var header = $("body#strains table thead").clone();
  var fixedHeader = $("body#strains #table-thead-fixed").append(header);
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
    var tableWidth = $("#strain-table").outerWidth();
    fixedHeader.outerWidth(tableWidth);
  }
}
