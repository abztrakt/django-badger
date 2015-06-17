$(document).ready(function() {
    $('.tagopt').chosen();
    $('.chosen-choices').css('padding', 0);
    $('.chosen-results').css('padding', 0);
    $('.tagopt').trigger('chosen:activate');
    //keeps tag value when page is refreshed.
    var tags = '';
    $('.search-choice').each(function() {
        tags += $(this).text().trim() + ' ';
    });
    var $idtags = $('#id_tags');
    $idtags.val(tags);
    //takes tags from chosen and sets to hidden input
    //value to play nice with POST parameters.
    $('.tagopt').chosen().change(function(evt, params) {
      if (typeof params.deselected === "undefined") {
        tags += params.selected + ' ';
      } else {
        tags = tags.replace(params.deselected + ' ','');
      }
      $idtags.val(tags);
    });
});
