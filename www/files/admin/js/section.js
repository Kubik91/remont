(function ($) {
    $(document).ready(function () {
        var items = {'table': 'Таблицы', 'carusel': 'Элементы карусели', 'block': 'Блоки', 'filter': 'Элементы фильтра', 'map': 'Карты' };
        function del_other() {
            $('.changeform-tabs-item > a').each(function (indx, element) {
                if ($(element).text() != items[$('#id_section_type').val()] && indx != 0) {
                    $(element).css("display", "none");
                } else {
                    $(element).removeAttr("style");
                }
            });
            if ($('#id_section_type').val() == 'block' || ($('#id_section_type').val() == 'table' && $('#table-group .inline-navigation-item').length <= 2)) {
                $('.changeform-tabs-item > a:contains("Картинки")').removeAttr('style');
            }
        }
        del_other();
        $('#id_section_type').change(del_other);
    })
})(django.jQuery);
