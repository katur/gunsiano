$(document).ready(function() {
  if (("body#publications").length) {
    togglePublications();
  }
})

togglePublications = function() {
  $("#pub-menu a").click(function() {
    // have only clicked menu item be active
    $("#pub-menu a").removeClass("active");
    $(this).addClass("active");

    // make counts and publications invisible
    $("#pub-count span").addClass("invisible");
    $(".pub-list").addClass("invisible");

    // make only the relevant count and publications display
    selector = $(this).attr("id");
    $("." + selector).removeClass("invisible");
  })
}
