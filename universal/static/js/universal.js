$(document).ready(function() {
  setResizeHandler();
  createDropdown();
  positionFooter();
  hoverTags();
})

$(window).load(function() {
  positionFooter();
})

function setResizeHandler() {
  $(window).resize(function() {
    positionFooter();
  })
}

function createDropdown() {
  welcomeMessage = $("#welcome-message");
  dropdown = $("#dropdown");

  function activateDropdown() {
    welcomeMessage.addClass("active");
    dropdown.addClass("visible");
    dropdown.fadeIn(200);
  }

  function deactivateDropdown() {
    welcomeMessage.removeClass("active");
    dropdown.removeClass("visible");
    dropdown.fadeOut(200);
  }

  welcomeMessage.on("click", function() {
    if (dropdown.hasClass("visible")) {
      deactivateDropdown();
    } else {
      activateDropdown();
    }
  });

  $("body").on("click", function(e) {
    if ($(e.target).is(welcomeMessage)) {
      return;
    }

    if ($(e.target).closest("#dropdown").length) {
      return;
    }

    deactivateDropdown();
  });
}

function positionFooter() {
  footer = $("#wrap-footer");
  footerHeight = footer.outerHeight();
  windowHeight = $(window).height();
  contentHeight = $("html").height();

  // if footer is absolute, it is not included in the content height, so add it
  if (footer.css("position") == "absolute") {
    contentHeight += footerHeight;
  }

  // if content is smaller than window, position the footer at bottom of page
  // otherwise position it statically (necessary in case user resizes window)
  footer.css(
    (contentHeight < windowHeight) ? {
      position: "absolute",
      bottom: "0",
      left: "0"
    } : {
      position: "static"
    }
  )
}

window.hoverTags = function() {
  $('body').on('mouseover', '[data-hover-tag]', function(e) {
    var left_offset, name, old_title, pointer_styles, position, tag, tag_styles, target, top_offset;
    target = $(this).closest('[data-hover-tag]');
    old_title = target.attr('title');
    target.attr('title', '');
    name = unescape(target.data('hover-tag'));
    if (name === '') {
      name = old_title;
      target.data('hover-tag', old_title);
    }
    position = target.offset();
    if ($('.hover_tag').length === 0) {
      tag_styles = {
        position: 'absolute',
        display: 'none',
        padding: '4px 6px 2px',
        background: 'black',
        background: 'rgba(0,0,0,0.8)',
        color: 'white',
        fontSize: '13px',
        zIndex: 800,
        textShadow: 'none'
      };
      pointer_styles = {
        position: 'absolute',
        top: '-6px',
        left: '50%',
        marginLeft: '-3px',
        width: '8px',
        height: '6px',
        background: 'url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAgAAAAGCAYAAAD+Bd/7AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAElJREFUeNpiYEAFxVCMFRgD8RkoNoYJMkJpXiBeBsSSUP5zII4C4s/MUIFcILZEMg2kgR2IjzNCjZuJw9p0kILNSEajg+cAAQYA1jkKUj6WaH4AAAAASUVORK5CYII=) no-repeat'
      };
      $('body').append("        <div class='hover_tag'>          <div class='text'></div>          <div class='tag_pointer'></div>        </div>");
      $('.hover_tag').css(tag_styles);
      $('.hover_tag .tag_pointer').css(pointer_styles);
    }
    tag = $('.hover_tag');
    tag.find('.text').html(name);
    top_offset = 8;
    left_offset = 0;
    if (target.data('hover-tag-top')) {
      top_offset = target.data('hover-tag-top');
    }
    if (target.data('hover-tag-left')) {
      left_offset = target.data('hover-tag-left');
    }
    return tag.css({
      top: position.top + target.outerHeight() + top_offset,
      left: position.left - tag.outerWidth() / 2 + target.width() / 2 + left_offset
    }).show();
  });
  return $('body').on('mouseout', '[data-hover-tag]', function(e) {
    return $('.hover_tag').hide();
  });
};
