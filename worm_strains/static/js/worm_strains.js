$(document).ready(function() {
	fixStrainsTopRow();
})

fixStrainsTopRow = function() {
	if ($(".strains").length) {
		var tableOffset = $(".strains").offset().top;
		var header = $(".strains > thead").clone();
		var fixedHeader = $("#table-thead-fixed").append(header);

		$(window).bind("scroll", function() {
			var offset = $(this).scrollTop();
			if (offset >= tableOffset && fixedHeader.is(":hidden")) {
				fixedHeader.show();
			} else if (offset < tableOffset) {
				fixedHeader.hide();
			}
		});
	}
}
