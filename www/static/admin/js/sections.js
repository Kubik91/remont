$(document).ready(function () {
    var items = {'Картинка': 'Картинки', 'Таблица': 'Таблицы', 'Карусель': 'Элементы карусели', 'Блок': 'Блоки', 'Фильтр': 'Элементы фильтра', 'Карта': 'Карты' };
    function del_other() {
        $('.changeform-tabs-item > a').each(function (indx, element) {
            if ($(element).text() != items[$('id_section_type').value()] || $(element).text() != 0) {
                $(element).css("display", "none");
            }
        });
    }
    del_other();
    $('id_section_type').change(del_other);
})
