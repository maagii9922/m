(function ($) {
  "use strict";

  $(document).on("click", "#productAddButton", function () {
    const modal = $("#productAddModal");
    $.ajax({
      url: "/ajax/product/",
      success: function (data) {
        modal.find(".modal-content").html(data);
        modal.modal("show");
      }
    });
  });

  $("#id_warehouse").on("change", function () {
    var val = $(this).val();
    var url = "/ajax/warehouse/change/" + val + "/";
    Swal.fire({
      title: "Итгэлтэй байна уу?",
      type: "question",
      text: "Агуулах солиход сагсанд байгаа бүх бүтээгдэхүүн устах болно.",
      showCancelButton: true,
      confirmButtonText: "Тийм",
      cancelButtonText: "Үгүй"
    }).then(result => {
      if (result.value) {
        window.location = url;
      }
    });
  });

  var products = {};

  $(document).on("click", "#tbody tr", "[name='product']", function () {
    if (event.target.type !== "checkbox") {
      $(":checkbox", this).trigger("click");
      if ($(":checkbox", this).is(":checked")) {
        products[$(":checkbox", this).val()] = $(":checkbox", this).val();
      } else {
        delete products[$(":checkbox", this).val()];
      }
      $("#productCount").html(Object.keys(products).length);
      $("#hidden").val(JSON.stringify(products));
    }
  });

  $(document).on("change", ":checkbox", function () {
    if ($(this).is(":checked")) {
      products[$(this).val()] = $(this).val();
    } else {
      delete products[$(this).val()];
    }
    $("#productCount").html(Object.keys(products).length);
    $("#hidden").val(JSON.stringify(products));
  });

  $(document).on("click", ".orderProductRemove", function () {
    var url = $(this).attr("data-href");
    window.location = url;
  });

  $(document).on("change", "[name='quantity']", function () {
    const cart_header = $("#cart-header");
    const url = $(this).attr("data-href");
    const val = $(this).val();

    $.ajax({
      url: url,
      data: { quantity: val },
      success: function (data) {
        cart_header.load("/cart/header/ajax/", function () {
          $(".indicator").each(function () {
            new CIndicator(this);
          });
        });

        if ($("#order_cart").length > 0) {
          $("#order_cart").load("/ajax/cart/load/", function () {
            $(".input-number").customNumber();
          });
        }

        $(".input-number").customNumber();
      }
    });
  });

  $(document).on("click", "#alertOrder", function () {
    Swal.fire({
      type: "warning",
      title: "Нөөц хүрэхгүй байна!",
      text: "Сагсан дахь барааны нөөц хүрэхгүй байна."
      // confirmButtonText: "Тийм"
    });
  });

  $(document).on("click", "#alertEmptyOrder", function () {
    Swal.fire({
      type: "warning",
      title: "Сагс хоосон байна!",
      text: "0 дүнтэй захиалга хийх боломжгүй."
      // confirmButtonText: "Тийм"
    });
  });

  $(document).on("click", "#createOrder", function () {
    Swal.fire({
      title: "Итгэлтэй байна уу?",
      type: "question",
      text: "Бүтээгдэхүүний захиалгыг үүсгэх болно.",
      showCancelButton: true,
      confirmButtonText: "Тийм",
      cancelButtonText: "Үгүй"
    }).then(result => {
      if (result.value) {
        $("#order_cart").addClass("cart--loading");
        $(this).addClass("btn-loading");
        $(this).attr("disabled", true);
        $.ajax({
          url: "/ajax/create/order/",
          success: function (data) {
            console.log(data);

            if (data.status == "error" && "data" in data) {
              const message = data.data.message;
              var alertMessage =
                '<div class="alert alert-danger alert-lg mb-3 alert-dismissible fade show">\
              ' +
                message +
                '<button\
                type="button"\
                class="close"\
                data-dismiss="alert"\
                aria-label="Close">&times</button>\
              </div>';
              $("#alertMessage").html(alertMessage);
            } else if (data.status == "error" && data.error_code == 16) {
              var alertMessage =
                '<div class="alert alert-danger alert-lg mb-3 alert-dismissible fade show">\
                  Системд алдаа гарлаа! Та түр хүлээгээд дахин оролдоно уу!<button\
                  type="button"\
                  class="close"\
                  data-dismiss="alert"\
                  aria-label="Close">&times</button>\
                </div>';
              $("#alertMessage").html(alertMessage);
            } else if (data.status == "success") {
              window.location = "/track-order/";
            }
            $("#createOrder").removeClass("btn-loading");
            $("#createOrder").attr("disabled", false);
          },
          done: function (data) { }
        });
      }
    });
  });
})(jQuery);
