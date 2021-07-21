var settings = {
  headerTag: "h3",
  bodyTag: "section",
  autoFocus: true,
  titleTemplate:
    '<span class="number">#index#</span> <span class="title">#title#</span>',
  labels: {
    current: "current step:",
    pagination: "Pagination",
    finish: "Дуусгах",
    next: "Дараах",
    previous: "Өмнөх",
    loading: "Loading ..."
  },
  onFinished: function(event, currentIndex) {
    $("#advertisementForm").submit();
  }
};

$("#wizard1").steps(settings);

$('.implement-type input[type="radio"]').each(function() {
  var value = $(this).val();
  if ($(this).prop("checked")) {
    $("div.categoryDiv").hide();
    $("#show-" + value).show();
  }
});

$('.implement-type input[type="radio"]').click(function() {
  var value = $(this).val();
  $("div.categoryDiv").hide();
  $("#show-" + value).show();
});
