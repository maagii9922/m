jQuery(function ($) {
  $('input[data-toggle="daterangepicker"]').daterangepicker({
    autoUpdateInput: false,
    locale: {
      format: "YYYY-MM-DD",
      cancelLabel: 'Цэвэрлэх',
      applyLabel: 'Шүүх'
    }
  });


  $('input[data-toggle="daterangepicker"]').on('apply.daterangepicker', function (ev, picker) {
    $(this).val(picker.startDate.format('YYYY-MM-DD') + ' - ' + picker.endDate.format('YYYY-MM-DD'));
  });

  $('input[data-toggle="daterangepicker"]').on('cancel.daterangepicker', function (ev, picker) {
    $(this).val('');
  });

  // $('input[data-toggle="daterangepicker"]').val("");
});