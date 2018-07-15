(function ($) {
    $(document).ready(function () {
        $('[name *= "animate"]').parent().append('<span class="image-animation" style="display: inline-block;"><h1 style="display: inline-block;">Animate</h1></span>');
        function changed() {
            $('.image-animation').removeAttr("class").addClass('image-animation animated ' + this.value); 
        };
        $('#content').on('change', '[name *= "animate"]', changed);
    })
})(django.jQuery);