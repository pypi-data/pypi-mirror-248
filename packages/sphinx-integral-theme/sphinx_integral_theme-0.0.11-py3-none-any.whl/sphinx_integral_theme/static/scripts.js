$(document).ready(function() {
  var caption = "#pytorch-left-menu p.caption";
  var collapseAdded = $(this).not("checked");
  var collapsedSections = [];
  var openArrow = '<svg width="12" height="12" viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4 10L8 6.12121L4 2" stroke="#8D93A1" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  var closeArrow = '<svg width="12" height="12" viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M2 4L5.87879 8L10 4" stroke="#8D93A1" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  $(caption).each(function () {
    var menuName = this.innerText.replace(/[^\w\s]/gi, "").trim();
    $(this).find("span").addClass("checked");

    if (collapsedSections.includes(menuName) == true && collapseAdded && sessionStorage.getItem(menuName) !== "expand" || sessionStorage.getItem(menuName) == "collapse") {
      $(this.firstChild).before("<span class='expand-menu'>" + openArrow + "</span>");
      $(this.firstChild).before("<span class='hide-menu collapse'>" + closeArrow + "</span>");
      $(this).next("ul").hide();
    } else if (collapsedSections.includes(menuName) == false && collapseAdded || sessionStorage.getItem(menuName) == "expand") {
      $(this.firstChild).before("<span class='expand-menu collapse'>" + openArrow + "</span>");
      $(this.firstChild).before("<span class='hide-menu'>" + closeArrow + "</span>");
    }
  });

  $(".expand-menu").on("click", function () {
    $(this).prev(".hide-menu").toggle();
    $(this).parent().next("ul").toggle();
    var menuName = $(this).parent().text().replace(/[^\w\s]/gi, "").trim();
    if (sessionStorage.getItem(menuName) == "collapse") {
      sessionStorage.removeItem(menuName);
      collapsedSections = collapsedSections.filter(section => section != menuName);
    }
    sessionStorage.setItem(menuName, "expand");
    collapsedSections.push(menuName);
    toggleList(this);
  });

  $(".hide-menu").on("click", function () {
    $(this).next(".expand-menu").toggle();
    $(this).parent().next("ul").toggle();
    var menuName = $(this).parent().text().replace(/[^\w\s]/gi, "").trim();
    if (sessionStorage.getItem(menuName) == "expand") {
      sessionStorage.removeItem(menuName);
      collapsedSections.push(menuName);
    }
    sessionStorage.setItem(menuName, "collapse");
    collapsedSections = collapsedSections.filter(section => section != menuName);
    toggleList(this);
  });

  function toggleList(menuCommand) {
    $(menuCommand).toggle();
  }
});