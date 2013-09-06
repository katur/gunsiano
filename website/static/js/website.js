$(document).ready(function() {
	positionFooter();
})

positionFooter = function() {
	windowHeight = $(window).height();
	contentHeight = $("html").height();
	
	if (contentHeight < windowHeight) {
		$("#wrap-footer").css({
			position: "absolute",
			bottom: "0",
			left: "0"
		})
	}
}
