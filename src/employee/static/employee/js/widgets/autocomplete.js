$(function () {
  $(".select2").each(function () {
    var url = $(this).attr("data-ajax--url");
    $(this).select2({
      ajax: {
        url: url,
        data: function (params) {
          return {
            term: params.term,
            page: params.page
          };
        }
      }
      // width: "100%",
      // searchInputPlaceholder: "Search options"
    });
  });
});
