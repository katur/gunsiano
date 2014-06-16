$(document).ready(function() {
  if ($("body#home").length) {
    // expandResearchAreaHeight();
    startWormAnimation();
    setScrollHandler();
  }
})

$(window).load(function() {
  if ($("body#home").length) {
    startHomepageScrollEffects();
  }
})

function setScrollHandler() {
  var previousScrollTop = 0;
  $(window).scroll(function(event){
    var currentScrollTop = $(this).scrollTop();
    var mouse = $("#mouse #drawing");

    if (currentScrollTop > previousScrollTop) {
      mouse.addClass("scrollingDown");
    } else {
      mouse.removeClass("scrollingDown");
    }
    previousScrollTop = currentScrollTop;
  });
}

function expandResearchAreaHeight() {
  var width = $(document).width();
  var minHeight = width / 4;

  var researchAreas = $(".research-area");
  researchAreas.each(function() {
    var currentArea = $(this);
    if (currentArea.height() < minHeight) {
      currentArea.height(minHeight);
    }
  });
}

function startWormAnimation() {
  var xStart = 131;
  var xEnd = 385;
  var yStart = 275;
  var radius = 5;
  var diameter = radius*2;

  var currentX = xStart;
  var currentY = yStart;
  var currentPosition = 0;
  var isMovingForward = true;

  var canvas = $("#world canvas")[0];

  if (canvas && canvas.getContext) {
    var context = canvas.getContext("2d");
    context.lineCap = "round";
    context.lineWidth = 3;
    setInterval(drawWorm, 200);
  }

  function drawWorm() {
    clearCanvas();
    context.beginPath();
    defineWormShape();
    context.stroke();
    updateCurrentState();

    function defineWormShape() {
      switch (currentPosition) {
        case 0:
          context.moveTo(currentX, currentY);
          context.arc(currentX + radius, currentY, radius, Math.PI, 0, false);

          context.moveTo(currentX + diameter, currentY);
          context.arc(currentX + diameter + radius, currentY, radius, Math.PI, 0,
              true);
          break;

        case 1:
          context.moveTo(currentX, currentY - radius);
          context.arc(currentX, currentY, radius, 3*Math.PI/2, 0, false);

          context.moveTo(currentX + radius, currentY);
          context.arc(currentX + diameter, currentY, radius, Math.PI, 0, true);

          context.moveTo(currentX + diameter + radius, currentY);
          context.arc(currentX + diameter*2, currentY, radius, Math.PI,
              3*Math.PI/2, false);
          break;

        case 2:
          context.moveTo(currentX, currentY);
          context.arc(currentX + radius, currentY, radius, Math.PI, 0, true);

          context.moveTo(currentX + diameter, currentY);
          context.arc(currentX + diameter + radius, currentY, radius, Math.PI, 0,
              false);
          break;

        case 3:
          context.moveTo(currentX, currentY + radius);
          context.arc(currentX, currentY, radius, Math.PI/2, 0, true);

          context.moveTo(currentX + radius, currentY);
          context.arc(currentX + diameter, currentY, radius, Math.PI, 0, false);

          context.moveTo(currentX + (radius*3), currentY);
          context.arc(currentX + diameter*2, currentY, radius, Math.PI,
              Math.PI/2, true);
          break;

        default:
          break;
      }
    }

    function updateCurrentState() {
      if (isMovingForward) {
        currentX += radius;
        currentPosition = (currentPosition + 1) % 4;
        if (currentX > xEnd) {
          isMovingForward = false;
        }

      } else {
        currentX -= radius;
        currentPosition -= 1;
        if (currentPosition <= -1) {
          currentPosition = 3;
        }

        if (currentX < xStart) {
          isMovingForward = true;
        }
      }
    }

    function clearCanvas() {
      context.save();

      // Use the identity matrix
      context.setTransform(1, 0, 0, 1, 0, 0);
      context.clearRect(0, 0, canvas.width, canvas.height);
      context.restore();
    }
  }
}

function startHomepageScrollEffects() {
  initializeWormLayers();
  initializePhylogenyMask();
  initializeRotatingRNA();
  createNetworkLayers();
  initializeMouse();

  var width = $(window).width();
  if (width > 500) {
    skrollr.init({
      smoothScrolling: false,
      forceHeight: false
    });
  } else {
    $("#evolution #mask").hide();
    $("#mouse #drawing").hide();
    $("#network canvas").css("top", "-50%");
  }

  function initializePhylogenyMask() {
    var mask = $("#evolution #mask");
    mask.attr("data-center-top", "height: 100%");
    mask.attr("data-center-center", "height: 0%");
  }

  function initializeMouse() {
    var footerHeight = $("#wrap-footer").outerHeight();
    var mouseDivHeight = $("#mouse").outerHeight();
    var mouseWrapper = $("#mouse #drawing-wrapper");
    var mouseHeight = mouseWrapper.outerHeight();
    var startScroll = footerHeight + mouseDivHeight - mouseHeight;
    var endScroll = footerHeight;

    mouseWrapper.attr("data-start", "right: -500%");
    mouseWrapper.attr("data-" + (startScroll+1) + "-end", "right: -500%");

    mouseWrapper.attr("data-" + startScroll + "-end", "right: -50%");
    mouseWrapper.attr("data-" + endScroll + "-end", "right: 100%");
    var mouse = $("#mouse #drawing");
    var numberOfSteps = 40;
    var stepSize = (startScroll - endScroll) / numberOfSteps;
    for (var i = 0; i < numberOfSteps; i++) {
      var scrollDistance = endScroll + i * stepSize;
      var position = 0;
      if (i % 2) {
        position = -380;
      }
      mouse.attr("data-" + scrollDistance + "-end",
          "background-position:!" + position + "px 0px");
    }
  }

  function initializeRotatingRNA() {
    var moleculeFrameHeight = 722;
    var moleculeFrameWidth = 678;
    var moleculeFrameCount = 20;
    var molecule = $("#molecule");

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

  function initializeWormLayers() {
    var viewportHeight = $(window).height();

    var layer1 = $("#gi .layer-1");
    var layer2 = $("#gi .layer-2");
    var layer3 = $("#gi .layer-3");

    var scrollFactor1 = 1.5;
    var scrollFactor2 = 1.0;
    var scrollFactor3 = .5;

    layer1.attr("data-bottom-top", "background-position: 0px 0px");
    layer1.attr("data-top-bottom", "background-position: 0px -" +
        viewportHeight * scrollFactor1 + "px");
    layer2.attr("data-bottom-top", "background-position: 0px 0px");
    layer2.attr("data-top-bottom", "background-position: 0px -" +
        viewportHeight * scrollFactor2 + "px");
    layer3.attr("data-bottom-top", "background-position: 0px 0px");
    layer3.attr("data-top-bottom", "background-position: 0px -" +
        viewportHeight * scrollFactor3 + "px");
  }

  function createNetworkLayers() {
    new Network($("#network .layer-1"), 2.5, 80000, 8, 2);
    new Network($("#network .layer-2"), 1.0, 40000, 6, 1);
    new Network($("#network .layer-3"), .5, 20000, 4, 1);
  }
}

Network = (function() {
  function Network(canvasElement, scrollFactor, pixelsPerNode, nodeRadius, edgeThickness) {
    this.canvasElement = canvasElement;
    this.scrollFactor = scrollFactor;
    this.pixelsPerNode = pixelsPerNode;
    this.nodeRadius = nodeRadius;
    this.edgeThickness = edgeThickness;

    this.viewportHeight = $(window).height();
    this.viewportWidth = $(window).width();
    this.verticalPadding = this.viewportWidth * 0.2;
    // this.elementHeight = $("#network").height();
    this.setDimensions();

    this.context = this.canvasElement.get(0).getContext("2d");
    this.setContextCanvasDimensions();

    this.nodes = [];
    this.setNumberOfNodes();
    this.createNodes();
    this.createAndDrawEdges();
    this.drawNodes();
    this.setSkrollrSettings();
  }

  Network.prototype.setSkrollrSettings = function() {
    var bottomTop = this.verticalPadding;
    var topBottom = bottomTop + this.viewportHeight * this.scrollFactor;
    this.canvasElement.attr("data-bottom-top", "top: -" + bottomTop + "px");
    this.canvasElement.attr("data-top-bottom", "top: -" + topBottom + "px");
  }

  Network.prototype.setDimensions = function() {
    this.height = this.viewportHeight * (1 + this.scrollFactor) +
        this.verticalPadding * 2;
    this.canvasElement.height(this.height);

    // Canvas width set in css
    this.width = this.canvasElement.width();

    this.area = this.height * this.width;
  }

  Network.prototype.setContextCanvasDimensions = function() {
    this.context.canvas.width = this.width;
    this.context.canvas.height = this.height;
  }

  Network.prototype.setNumberOfNodes = function() {
    this.numberOfNodes = Math.floor(this.area / this.pixelsPerNode);
  }

  Network.prototype.createNodes = function() {
    var hubPercentage = 0.10;
    for (i = 0; i < this.numberOfNodes; i++) {
      var x = Math.floor(Math.random() * this.width);
      var y = Math.floor(Math.random() * this.height);
      var isHub = Math.random() < hubPercentage;
      var node = new Node(this.context, this.nodeRadius, x, y, isHub);
      this.nodes.push(node);
    }
  }

  Network.prototype.createAndDrawEdges = function() {
    var hubOutgoingEdges = 10;
    for (i = 0; i < this.numberOfNodes; i++) {
      var node = this.nodes[i];
      if (node.isHub) {
        for (j = 0; j < hubOutgoingEdges; j++) {
          this.drawEdgeToAnotherNode(node);
        }
      } else {
        // this.drawEdgeToAnotherNode(node);
      }
    }
  }

  Network.prototype.drawEdgeToAnotherNode = function(node) {
    var otherNodeIndex = Math.floor(Math.random() * this.numberOfNodes);
    var otherNode = this.nodes[otherNodeIndex];
    var edge = new Edge(this.context, this.edgeThickness, node, otherNode);
  }

  Network.prototype.drawNodes = function() {
    for (i = 0; i < this.numberOfNodes; i++) {
      var node = this.nodes[i];
      node.draw();
    }
  }

  return Network;
})();

Node = (function() {
  function Node(context, radius, x, y, isHub) {
    this.context = context;
    this.radius = radius;
    this.x = x;
    this.y = y;
    this.isHub = isHub;
    this.color = "#FFEC8B";
  }

  Node.prototype.draw = function() {
    this.context.fillStyle = this.color;
    this.context.beginPath();
    this.context.arc(this.x, this.y, this.radius, 0, 2*Math.PI);
    this.context.fill();
  }

  return Node;
})();

Edge = (function() {
  function Edge(context, thickness, nodeA, nodeB) {
    this.context = context;
    this.thickness = thickness;
    this.nodeA = nodeA;
    this.nodeB = nodeB;
    this.color = "#8B6969";
    this.draw();
  }

  Edge.prototype.draw = function() {
    this.context.strokeStyle = this.color;
    this.context.lineWidth = this.thickness;

    this.context.beginPath();
    this.context.moveTo(this.nodeA.x, this.nodeA.y);
    this.context.lineTo(this.nodeB.x, this.nodeB.y);
    this.context.stroke();
  }

  return Edge;
})();
