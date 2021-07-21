function touchClick(elements, callback) {
  elements = $(elements);

  let touchStartData = null;

  const onTouchstart = function(event) {
    const originalEvent = event.originalEvent;

    if (originalEvent.touches.length !== 1) {
      touchStartData = null;
      return;
    }

    touchStartData = {
      target: originalEvent.currentTarget,
      touch: originalEvent.changedTouches[0],
      timestamp: new Date().getTime()
    };
  };
  const onTouchEnd = function(event) {
    const originalEvent = event.originalEvent;

    if (
      !touchStartData ||
      originalEvent.changedTouches.length !== 1 ||
      originalEvent.changedTouches[0].identity !== touchStartData.touch.identity
    ) {
      return;
    }

    const timestamp = new Date().getTime();
    const touch = originalEvent.changedTouches[0];
    const distance = Math.abs(
      Math.sqrt(
        Math.pow(touchStartData.touch.screenX - touch.screenX, 2) +
          Math.pow(touchStartData.touch.screenY - touch.screenY, 2)
      )
    );

    if (
      touchStartData.target === originalEvent.currentTarget &&
      timestamp - touchStartData.timestamp < 500 &&
      distance < 10
    ) {
      callback(event);
    }
  };

  elements.on("touchstart", onTouchstart);
  elements.on("touchend", onTouchEnd);

  return function() {
    elements.off("touchstart", onTouchstart);
    elements.off("touchend", onTouchEnd);
  };
}

function CIndicator(element) {
  this.element = $(element);
  this.dropdown = this.element.find(".indicator__dropdown");
  this.button = this.element.find(".indicator__button");
  this.trigger = null;

  this.element.data("indicatorInstance", this);

  if (this.element.hasClass("indicator--trigger--hover")) {
    this.trigger = "hover";
  } else if (this.element.hasClass("indicator--trigger--click")) {
    this.trigger = "click";
  }

  this.onMouseenter = this.onMouseenter.bind(this);
  this.onMouseleave = this.onMouseleave.bind(this);
  this.onTransitionend = this.onTransitionend.bind(this);
  this.onClick = this.onClick.bind(this);
  this.onGlobalClick = this.onGlobalClick.bind(this);

  // add event listeners
  this.element.on("mouseenter", this.onMouseenter);
  this.element.on("mouseleave", this.onMouseleave);
  this.dropdown.on("transitionend", this.onTransitionend);
  this.button.on("click", this.onClick);
  $(document).on("click", this.onGlobalClick);
  touchClick(document, this.onGlobalClick);

  this.element.find(".drop-search__input").on("keydown", function(event) {
    const ESC_KEY_CODE = 27;

    if (event.which === ESC_KEY_CODE) {
      const instance = $(this)
        .closest(".indicator")
        .data("indicatorInstance");

      if (instance) {
        instance.close();
      }
    }
  });
}
CIndicator.prototype.toggle = function() {
  if (this.isOpen()) {
    this.close();
  } else {
    this.open();
  }
};
CIndicator.prototype.onMouseenter = function() {
  this.element.addClass("indicator--hover");

  if (this.trigger === "hover") {
    this.open();
  }
};
CIndicator.prototype.onMouseleave = function() {
  this.element.removeClass("indicator--hover");

  if (this.trigger === "hover") {
    this.close();
  }
};
CIndicator.prototype.onTransitionend = function(event) {
  if (
    this.dropdown.is(event.target) &&
    event.originalEvent.propertyName === "visibility" &&
    !this.isOpen()
  ) {
    this.element.removeClass("indicator--display");
  }
};
CIndicator.prototype.onClick = function(event) {
  if (this.trigger !== "click") {
    return;
  }

  if (event.cancelable) {
    event.preventDefault();
  }

  this.toggle();
};
CIndicator.prototype.onGlobalClick = function(event) {
  // check that the click was outside the element
  if (this.element.not($(event.target).closest(".indicator")).length) {
    this.close();
  }
};
CIndicator.prototype.isOpen = function() {
  return this.element.is(".indicator--open");
};
CIndicator.prototype.open = function() {
  this.element.addClass("indicator--display");
  this.element.width(); // force reflow
  this.element.addClass("indicator--open");
  this.element.find(".drop-search__input").focus();

  const dropdownTop = this.dropdown.offset().top - $(window).scrollTop();
  const viewportHeight = window.innerHeight;
  const paddingBottom = 20;

  this.dropdown.css(
    "maxHeight",
    viewportHeight - dropdownTop - paddingBottom + "px"
  );
};
CIndicator.prototype.close = function() {
  this.element.removeClass("indicator--open");
};
CIndicator.prototype.closeImmediately = function() {
  this.element.removeClass("indicator--open");
  this.element.removeClass("indicator--display");
};

(function($) {
  "use strict";

  /*
  // quickview
  */
  const quickview = {
    cancelPreviousModal: function() {},
    clickHandler: function() {
      const modal = $("#productDetailModal");
      const button = $(this);
      const url = $(this).attr("data-href");
      const doubleClick = button.is(".product-card__quickview--preload");

      quickview.cancelPreviousModal();

      if (doubleClick) {
        return;
      }

      button.addClass("product-card__quickview--preload");

      let xhr = null;
      // timeout ONLY_FOR_DEMO!
      const timeout = setTimeout(function() {
        xhr = $.ajax({
          url: url,
          success: function(data) {
            quickview.cancelPreviousModal = function() {};
            button.removeClass("product-card__quickview--preload");

            modal.find(".modal-content").html(data);
            modal.find(".quickview__close").on("click", function() {
              modal.modal("hide");
            });
            modal.modal("show");
          }
        });
      }, 1000);

      quickview.cancelPreviousModal = function() {
        button.removeClass("product-card__quickview--preload");

        if (xhr) {
          xhr.abort();
        }

        // timeout ONLY_FOR_DEMO!
        clearTimeout(timeout);
      };
    }
  };

  $(function() {
    const modal = $("#productDetailModal");

    modal.on("shown.bs.modal", function() {
      // modal.find(".product").each(function() {
      //   const gallery = $(this).find(".product-gallery");

      //   if (gallery.length > 0) {
      //     initProductGallery(gallery[0], $(this).data("layout"));
      //   }
      // });

      $(".input-number", modal).customNumber();
    });

    $(".product-card__quickview").on("click", function() {
      quickview.clickHandler.apply(this, arguments);
    });
  });

  $(function() {
    $(".indicator").each(function() {
      new CIndicator(this);
    });
  });

  $(function() {
    /*
    // cart add
    */
    $(document).on("click", ".product-card__addtocart", function() {
      const button = $(this);
      const cart_header = $("#cart-header");

      button.addClass("btn-loading");

      const url = $(this).attr("data-href");

      setTimeout(function() {
        $.ajax({
          url: url,
          success: function(data) {
            button.removeClass("btn-loading");

            cart_header.load("/cart/header/ajax/", function() {
              $(".indicator").each(function() {
                new CIndicator(this);
              });
            });

            if ($("#order_cart").length > 0) {
              $("#order_cart").load("/ajax/cart/load/");
            }

            var cart_header_indicator = new CIndicator(cart_header);
            cart_header_indicator.open();

            setTimeout(function() {
              if (cart_header_indicator.isOpen()) {
                cart_header_indicator.close();
              }
            }, 2000);
          }
        });
      }, 500);
    });

    /*
    // cart remove
    */
    $(document).on("click", ".dropcart__product-remove", function() {
      const url = $(this).attr("data-href");
      $(this)
        .parents(".dropcart__product")
        .hide();

      $.ajax({
        url: url,
        success: function(data) {
          $(this)
            .closest(".dropcart__product")
            .hide();

          $(".cart_length").each(function() {
            $(this).html(data.cart_length);
          });

          $(".cart_total").each(function() {
            $(this).html(data.cart_total);
          });

          if ($(".dropcart__product:visible").length == 0) {
            $(".dropcart__products-list").html("Сагс хоосон байна");
          }

          if ($("#order_cart").length > 0) {
            $("#order_cart").load("/ajax/cart/load/", function() {
              $(".input-number").customNumber();
            });
          }
        }
      });
    });
  });
})(jQuery);
