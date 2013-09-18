$(document).ready(function() {
	togglePublications();
})

togglePublications = function() {
	$("#pub-menu a").click(function() {
		// have only clicked menu item be active
		$("#pub-menu a").removeClass("active");
		$(this).addClass("active");

		// make counts and publications invisible
		$("#pub-count span").addClass("invisible");
		$(".publications").addClass("invisible");

		// make only the relevant count and publications display
		selector = $(this).attr("id");
		$("." + selector).removeClass("invisible");
	})
}
