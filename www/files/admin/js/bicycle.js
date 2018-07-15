(function ($) {
    $(document).ready(function () {
        $('form').submit(function (e) {
            $('[id *= TOTAL_FORMS]').val($('.inline-related:not(.empty-form)').length);
        })
    })
})(django.jQuery);