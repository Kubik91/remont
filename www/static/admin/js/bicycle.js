(function ($) {
    $(document).ready(function () {
        $('form').submit(function (e) {
            $('[id *= TOTAL_FORMS]').each(function () {
                $(this).val($(this).nextAll('.inline-related:not(.empty-form)').length);
            })
        })
    })
})(django.jQuery);