$(document).ready(function() {
  if ($("body#strains").length) {
    fixStrainsTopRow();
  }
})

fixStrainsTopRow = function() {
  var tableOffset = $(".strains").offset().top;
  var header = $(".strains > thead").clone();
  var fixedHeader = $("#table-thead-fixed").append(header);

  $(window).bind("scroll", function() {
    var scrollDistance = $(this).scrollTop();
    if (scrollDistance >= tableOffset && fixedHeader.is(":hidden")) {
      fixedHeader.show();
    } else if ((scrollDistance < tableOffset) && fixedHeader.is(":visible")) {
      fixedHeader.hide();
    }
  });
}
