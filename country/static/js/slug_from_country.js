function initSlugAutoPopulateFromCountry() {
    var slugFollowsTitle = false;

    $('#id_country').on('focus', function() {
        /* slug should only follow the title field if its value matched the title's value at the time of focus */
        var currentSlug = $('#id_slug').val();
        // If select value is not empty we get current selection's label.
        var value = this.value !== '' ? this.options[this.selectedIndex].innerHTML : '';
        var slugifiedTitle = cleanForSlug(value, true);
        slugFollowsTitle = (currentSlug == slugifiedTitle);
    });

    $('#id_country').on('change', function() {
        if (slugFollowsTitle) {
            var label = this.options[this.selectedIndex].innerHTML;
            var slugifiedTitle = cleanForSlug(label, true);
            $('#id_slug').val(slugifiedTitle);
        }
    });
}

$(function() {
  /* Only non-live pages should auto-populate the slug from the title */
  if (!$('body').hasClass('page-is-live')) {
      initSlugAutoPopulateFromCountry();
  }
});