$(document).ready(function() {
	draw();
	togglePublications();
	homepageScrollEffects();
})

draw = function() {
	function clearCanvas() {
		ctx.save(); // store current transformation matrix

		// Use the identity matrix while clearing the canvas
		ctx.setTransform(1, 0, 0, 1, 0, 0);
		ctx.clearRect(0, 0, canvas.width, canvas.height);

		ctx.restore(); // restore transform
	}

	function drawWorm(position, x, y) {
		ctx.beginPath();
		if (position==0) {
			ctx.moveTo(x, y);
			// arc(x, y, radius, startAngle, endAngle, anticlockwise);
			ctx.arc(x+5, y, 5, Math.PI, 0, false); // left half
			ctx.moveTo(x+10, y);
			ctx.arc(x+15, y, 5, Math.PI, 0, true); // right half
		} else if (position==1) {
			ctx.moveTo(x+5, y-5);
			ctx.arc(x+5, y, 5, 3*Math.PI/2, 0, false); // left half
			ctx.moveTo(x+10, y);
			ctx.arc(x+15, y, 5, Math.PI, 0, true); // right half
			ctx.moveTo(x+20, y);
			ctx.arc(x+25, y, 5, Math.PI, 3*Math.PI/2, false); // right half
		} else if (position==2) {
			ctx.moveTo(x+10, y);
			ctx.arc(x+15, y, 5, Math.PI, 0, true); // left half
			ctx.moveTo(x+20, y);
			ctx.arc(x+25, y, 5, Math.PI, 0, false); // right half
		} else if (position==3) {
			ctx.moveTo(x+15, y+5);
			ctx.arc(x+15, y, 5, Math.PI/2, 0, true); // left half
			ctx.moveTo(x+20, y);
			ctx.arc(x+25, y, 5, Math.PI, 0, false); // right half
			ctx.moveTo(x+30, y);
			ctx.arc(x+35, y, 5, Math.PI, Math.PI/2,true); // right half
		}
		ctx.stroke();
	}

	function drawWormCycle(t, x, y) {
		d = 200;
		setTimeout( function(){clearCanvas(); drawWorm(0, x, y)}, t );
		setTimeout( function(){clearCanvas(); drawWorm(1, x, y)}, t+=d );
		setTimeout( function(){clearCanvas(); drawWorm(2, x, y)}, t+=d );
		setTimeout( function(){clearCanvas(); drawWorm(3, x, y)}, t+=d );
	}

	var canvas = document.getElementById("world-worms");
	if (canvas && canvas.getContext) {
		var ctx = canvas.getContext("2d");
		ctx.lineCap="round";
		ctx.lineWidth=3;

		var startTime = 0;
		var xStart = 128;
		var x = 0;
		var y = 275;

		for (i=0; i<1000; i++) {
			drawWormCycle(startTime, xStart + x, y);
			startTime += 800;
			x = (x + 20) % 260;
		}
	}
}

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

homepageScrollEffects = function() {
	if ($('body#home').length) {
		rotateMolecule();
		skrollr.init({
			smoothScrolling: false,
			forceHeight: false
		});
	}
}

var moleculeFrameHeight = 722;
var moleculeFrameWidth = 678;
var moleculeFrameCount = 20;

rotateMolecule = function() {
	var molecule = $("#rna-image");
	var step = 100 / moleculeFrameCount;

	var viewportHeight = $(window).height();
	var stepsInViewport = viewportHeight / step;

	var totalSteps = moleculeFrameCount + stepsInViewport;

	molecule.attr("data-bottom-top", "background-position:!0px 0px");

	var spritePosition;
	for (var i = 1; i < totalSteps; i++) {
		spritePosition = moleculeFrameWidth * i * -1;
		molecule.attr("data--" +  (step * i) + "p-bottom-top",
				"background-position:!" + spritePosition + "px 0px");
	}
}
