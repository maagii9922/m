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
  onStepChanging: function(event, currentIndex, newIndex) {
    if (currentIndex < newIndex) {
      // Step 1 form validation
      if (currentIndex === 0) {
        var name = $("#id_name").parsley();
        var dates = $("#id_dates").parsley();

        if (name.isValid() && dates.isValid()) {
          return true;
        } else {
          name.validate();
          dates.validate();
        }
      }

      // Step 2 form validation
      if (currentIndex === 1) {
        var promotion_type = $("#id_promotion_type").parsley();
        var product = $("#id_product").parsley();
        var percent_1 = $("#id_percent_1").parsley();
        if (
          promotion_type.isValid() &&
          product.isValid() &&
          percent_1.isValid()
        ) {
          return true;
        } else {
          promotion_type.validate();
          product.validate();
          percent_1.validate();
        }
      }

      if (currentIndex === 2) {
        return true;
      }
      // Always allow step back to the previous step even if the current step is not valid.
    } else {
      return true;
    }
  },
  onFinished: function(event, currentIndex) {
    $("#promotionForm").submit();
  }
};

$("#wizard").steps(settings);

$('.promotion-type input[type="radio"]').each(function() {
  var value = $(this).val();
  if ($(this).prop("checked")) {
    $("div.promotionDiv").hide();
    $("#show-" + value).show();
  }
});

$("#id_promotion_type").change(function() {
  var value = $(this).val();
  $("div.promotionDiv").hide();
  $("#show-" + value).show();
  $("#show-" + value).find("#id_product", function() {
    alert(this);
  });
});

const onChange1 = val => {
  if (val === "1") {
    document.getElementById("id_percent_1").readOnly = false;
    document.getElementById("id_price_1").readOnly = true;
    document.getElementById("id_above_the_number_1").readOnly = true;
    document.getElementById("id_above_the_number_percent_1").readOnly = true;
  } else if (val === "2") {
    document.getElementById("id_percent_1").readOnly = true;
    document.getElementById("id_price_1").readOnly = false;
    document.getElementById("id_above_the_number_1").readOnly = true;
    document.getElementById("id_above_the_number_percent_1").readOnly = true;
  } else if (val === "3") {
    document.getElementById("id_percent_1").readOnly = true;
    document.getElementById("id_price_1").readOnly = true;
    document.getElementById("id_above_the_number_1").readOnly = false;
    document.getElementById("id_above_the_number_percent_1").readOnly = false;
  }
};

const onChange3 = val => {
  if (val === "1") {
    document.getElementById("id_percent_3").readOnly = false;
    document.getElementById("id_price_3").readOnly = true;
    document.getElementById("id_above_the_number_3").readOnly = true;
    document.getElementById("id_above_the_number_percent_3").readOnly = true;
  } else if (val === "2") {
    document.getElementById("id_percent_3").readOnly = true;
    document.getElementById("id_price_3").readOnly = false;
    document.getElementById("id_above_the_number_3").readOnly = true;
    document.getElementById("id_above_the_number_percent_3").readOnly = true;
  } else if (val === "3") {
    document.getElementById("id_percent_3").readOnly = true;
    document.getElementById("id_price_3").readOnly = true;
    document.getElementById("id_above_the_number_3").readOnly = false;
    document.getElementById("id_above_the_number_percent_3").readOnly = false;
  }
};

$('.implement-type input[type="radio"]').each(function() {
  var value = $(this).val();
  if ($(this).prop("checked")) {
    $("div.implementDiv").hide();
    $("#showImplementType-" + value).show();
  }
});

$("#id_implement_type").change(function() {
  var value = $(this).val();
  $("div.implementDiv").hide();
  $("#showImplementType-" + value).show();
});

$(function() {
  $(".formset_row").formset({
    addText: "Бүтээгдэхүүн нэмэх",
    deleteText: "Устгах",
    prefix: "promotion_products",
    added: function(row) {
      $(row.find(".select2")).each(function() {
        url = $(this).attr("data-ajax--url");
        $(this).select2({
          ajax: {
            url: url,
            data: function(params) {
              return {
                term: params.term,
                page: params.page
              };
            }
          },
          width: "100%"
        });
      });
    }
  });

  $(".acc_buy_row").formset({
    addText: "Бүтээгдэхүүн нэмэх",
    deleteText: "Устгах",
    prefix: "buy",
    added: function(row) {
      $(row.find(".select2")).each(function() {
        url = $(this).attr("data-ajax--url");
        $(this).select2({
          ajax: {
            url: url,
            data: function(params) {
              return {
                term: params.term,
                page: params.page
              };
            }
          },
          width: "100%"
        });
      });
    }
  });

  $(".give_formset_row").formset({
    addText: "Бүтээгдэхүүн нэмэх",
    deleteText: "Устгах",
    prefix: "sell",
    added: function(row) {
      $(row.find(".select2")).each(function() {
        url = $(this).attr("data-ajax--url");
        $(this).select2({
          ajax: {
            url: url,
            data: function(params) {
              return {
                term: params.term,
                page: params.page
              };
            }
          },
          width: "100%"
        });
      });
    }
  });
});
