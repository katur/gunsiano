$(document).ready(function() {
  if ($("body#home").length) {
    expandResearchAreaHeight();
    startWormAnimation();
    startHomepageScrollEffects();
  }
})

function expandResearchAreaHeight() {
  var width = $(document).width();
  var minHeight = width / 4;

  var researchAreas = $(".research-area");
  researchAreas.each(function() {
    var currentArea = $(this);
    if (currentArea.height() < minHeight) {
      console.log(researchArea);
      console.log(currentArea.height());
      currentArea.height(minHeight);
      console.log(currentArea.height());
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
  rotateMolecule();
  new Network($("#network .layer-3"), 200, 4, 1);
  new Network($("#network .layer-2"), 100, 6, 1);
  new Network($("#network .layer-1"), 50, 8, 2);

  skrollr.init({
    smoothScrolling: false,
    forceHeight: false
  });

  function rotateMolecule() {
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
}

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

Network = (function() {
  function Network(canvasElement, numberOfNodes, nodeRadius, edgeThickness) {
    this.canvasElement = canvasElement;
    this.numberOfNodes = numberOfNodes;
    this.nodeRadius = nodeRadius;
    this.edgeThickness = edgeThickness;
    this.nodes = [];
    this.hubPercentage = 0.05;
    this.hubOutgoingEdges = 20;

    this.context = this.canvasElement.get(0).getContext("2d");
    this.initializeDimensions();
    this.setContextCanvasDimensions();
    this.createNodes();
    this.createAndDrawEdges();
    this.drawNodes();
  }

  Network.prototype.initializeDimensions = function() {
    this.width = this.canvasElement.width();
    this.height = this.canvasElement.height();
  }

  Network.prototype.setContextCanvasDimensions = function() {
    this.context.canvas.width = this.width;
    this.context.canvas.height = this.height;
  }

  Network.prototype.createNodes = function() {
    for (i = 0; i < this.numberOfNodes; i++) {
      var x = Math.floor(Math.random() * this.width);
      var y = Math.floor(Math.random() * this.height);
      var isHub = Math.random() < this.hubPercentage;
      var node = new Node(this.context, this.nodeRadius, x, y, isHub);
      this.nodes.push(node);
    }
  }

  Network.prototype.createAndDrawEdges = function() {
    for (i = 0; i < this.numberOfNodes; i++) {
      var node = this.nodes[i];
      if (node.isHub) {
        for (j = 0; j < this.hubOutgoingEdges; j++) {
          this.drawEdgeToAnotherNode(node);
        }
      } else {
        this.drawEdgeToAnotherNode(node);
      }
    }
  }

  Network.prototype.drawEdgeToAnotherNode = function(node) {
    var otherNodeIndex = Math.floor(Math.random() * this.numberOfNodes);
    var otherNode = this.nodes[otherNodeIndex];
    var edge = new Edge(this.context, this.edgeThickness, node, otherNode);
  },

  Network.prototype.drawNodes = function() {
    for (i = 0; i < this.numberOfNodes; i++) {
      var node = this.nodes[i];
      node.draw();
    }
  }

  return Network;
})();
