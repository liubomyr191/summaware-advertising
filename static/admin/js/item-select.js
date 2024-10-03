$(document).ready(function () {
  $('.item-select-container').each(function () {
    var $container = $(this);

    $container.find('.btnRight').click(function (e) {
      var selectedOpts = $container.find('.lstBox1 option:selected');
      if (selectedOpts.length == 0) {
        alert('Nothing to move.');
        e.preventDefault();
        return;
      }

      $container.find('.lstBox2').append($(selectedOpts).clone());
      $(selectedOpts).remove();
      e.preventDefault();
    });

    $container.find('.btnLeft').click(function (e) {
      var selectedOpts = $container.find('.lstBox2 option:selected');
      if (selectedOpts.length == 0) {
        alert('Nothing to move.');
        e.preventDefault();
        return;
      }

      $container.find('.lstBox1').append($(selectedOpts).clone());
      $(selectedOpts).remove();
      e.preventDefault();
    });
  });
});
