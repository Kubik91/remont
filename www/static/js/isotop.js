var isotope = $('filter').isotope({"layoutMode": "packery","itemSelector":".grid-item"});
$('.filters-button-group').on('click', 'button', function () {
    var filterValue = $(this).attr('data-filter');
    $('.filters-button-group>.button').removeClass('is-checked');
    $(this).addClass('is-checked');
    isotope_w1.isotope({ filter: filterValue });
});