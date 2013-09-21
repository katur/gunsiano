$(document).ready(function() {
	draw();
	togglePublications();
})

draw = function() {
	function clearCanvas() {
		// Store the current transformation matrix
		ctx.save();

		// Use the identity matrix while clearing the canvas
		ctx.setTransform(1, 0, 0, 1, 0, 0);
		ctx.clearRect(0, 0, canvas.width, canvas.height);

		// Restore the transform
		ctx.restore();
	}

	function drawPosition(position, x, y) {
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

	function drawCycle(t, x, y) {
		d = 200;
		setTimeout( function(){clearCanvas(); drawPosition(0, x, y)}, t );
		setTimeout( function(){clearCanvas(); drawPosition(1, x, y)}, t+=d );
		setTimeout( function(){clearCanvas(); drawPosition(2, x, y)}, t+=d );
		setTimeout( function(){clearCanvas(); drawPosition(3, x, y)}, t+=d );
	}

	var canvas = document.getElementById("world-worms");
	if (canvas.getContext) {
		var ctx = canvas.getContext("2d");
		var startTime = 0;
		var x = -50;
		var x = 0;
		var y = 250;

		for (var i=0; i<30; i++) {
			drawCycle(startTime, x, y);
			startTime += 800;
			x+=20;
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
