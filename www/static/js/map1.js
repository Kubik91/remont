//if($('#img').)
/*$(document).ready(function(){
    $("#map").replaceWith(function(index, oldHTML){ 
        console.log($(this).attr('id'));
        console.log($(this).attr('style'));
    return $("<p>").attr({"id":$(this).attr('id'), "style":$(this).attr('style')}).html($(this).html());
});
})*/

/*if(!$('#map').attr('width')){
    $('#map').css({"width":"80%", "height":"400px"});
};*/

if(!$('.map').attr('width')){
    $('.map').css({"width":"80%", "height":"400px"});
}
ymaps.ready(function () {
    //$("#map").replaceWith(function(index, oldHTML){
    //    return $("<p>").attr({"id":$(this).attr('id'), "style":$(this).attr('style')}).html($(this).html())
    //})

    var points = [[53.863747, 27.614984]],//, [53.92, 27]],


        // Получаем ссылки на нужные элементы управления.
        geolocationControl = new ymaps.control.GeolocationControl({
            options: {
                layout: 'round#buttonLayout'
            }
        }),
        autoRouteItem = new ymaps.control.Button({
            data: {
                image: '//yastatic.net/maps-beta/_/Uo4J6sV9ZYd-qgkUDb7ckNaMaR0.svg',
                title: 'Автомобиль'
            },
            options: {
                layout: 'round#buttonLayout',
                maxWidth: 120
            }
        }, {
            selectOnClick: true
        }),
        masstransitRouteItem = new ymaps.control.Button({
            data: {
                image: '//yastatic.net/maps-beta/_/76k6qZ1sFLAb9Uyt1s3mlNR_ML0.svg',
                title: 'Общественный транспорт'
            },
            options: {
                layout: 'round#buttonLayout',
                maxWidth: 120
            }
        });
        pedestrianRouteItem = new ymaps.control.Button({
            data: {
                image: '//yastatic.net/maps-beta/_/yusExz8Yt-tnbA-LS5BCHEOnbJA.svg',
                title: 'Пешком'
            },
            options: {
                layout: 'round#buttonLayout',
                maxWidth: 120
            }
        }),
        exchangeRoute = new ymaps.control.Button({
            data: {
                image: '//yastatic.net/maps-beta/_/ri80iz_jyqqh_RP3Sji3VV1yLao.svg',
                title: 'Обратный путь',
            },
            options: {
                layout: 'round#buttonLayout',
                maxWidth: 120,
                float: 'right'
            }
        }),

        zoomControl = new ymaps.control.ZoomControl({
            options: {
                layout: 'round#zoomLayout'
            }
        }),
    HintLayout = ymaps.templateLayoutFactory.createClass(
        "<div class='my-hint'>" +
        "<b>{{ properties.object }}</b><br />" +
        "{{ properties.address }}" +
        "</div>", {
            // Определяем метод getShape, который
            // будет возвращать размеры макета хинта.
            // Это необходимо для того, чтобы хинт автоматически
            // сдвигал позицию при выходе за пределы карты.
            getShape: function () {
                var el = this.getElement(),
                    result = null;
                if (el) {
                    var firstChild = el.firstChild;
                    result = new ymaps.shape.Rectangle(
                        new ymaps.geometry.pixel.Rectangle([
                            [0, 0],
                            [firstChild.offsetWidth, firstChild.offsetHeight]
                        ])
                    );
                }
                return result;
            }
        }
    );
    
    var flag;

    var sourcePoint, // Метка для начальной точки маршрута.
        targetPoint; // Метка для конечной точки маршрута.

    // Переменные, в которых будут храниться ссылки на текущий маршрут.
    var currentRoute,
        currentRoutingMode;
    
    
    
    //myMap.controls.add(autoRouteItem);
    //myMap.controls.add(masstransitRouteItem);
    //myMap.controls.add(pedestrianRouteItem);
    //myMap.controls.add(exchangeRoute);
    //myMap.controls.add(zoomControl);
    
    //myMap.controls.add(geolocationControl);

    var myCollection = new ymaps.GeoObjectCollection();
    
    if(points.length){
    // Перебираем в цикле точки, которые надо добавить на карту
        for (i = 0; i < points.length; i++ ){
            var myPlacemark = new ymaps.Placemark([
                points[i][0], points[i][1]],{
                    //balloonContentHeader: "Балун метки",
                    balloonContentBody: [
                        '<address>',
                        '<strong>Ремонт бытовой и электронной техники</strong>',
                        '<br/>',
                        'Адрес: Минск, ул. Плеханова, 55',
                        '<br/>',
                        'Подробнее: <a href="http://t-save.by">ТехноSave</a>',
                        '</address>'
                    ].join(''),
                    //balloonContentFooter: "Подвал",
                    preset: 'islands#icon',
                    address: 'Минск, ул. Плеханова, 55',
                    object: 'Ремонт бытовой и элетронной техники',
                    //hintContent: "Хинт метки"
                },{
                    hintLayout: HintLayout,
                    hintPane: 'hint',
                    balloonPanelMaxMapArea: 'Infinity',
                    balloonAutoPan: false
                }
            );
            // Не забываем добавить точку в коллекцию -
            //  впоследствии мы добавим всю коллекцию на карту
            myCollection.add(myPlacemark)
        };
            // Добавляем точки на карту
            myMap.geoObjects.add(myCollection);
        
        // Вычисляем необходимые координаты краёв карты и
        //  устанавливаем их для нашего экземпляра карты	
        //myMap.setBounds( myCollection.getBounds())
        myMap.setBounds(myMap.geoObjects.getBounds(), {checkZoomRange:true}).then(function(){ if(myMap.getZoom() > 13) myMap.setZoom(16);});
    };

    myCollection.events.add('click', function(e){
        
        //myMap.geoObjects.remove(sourcePoint);
        myCollection.each(function(e){
            e.options.set('preset', 'islands#blueIcon');
        });
        //myMap.geoObjects.add(sourcePoint);
        myMap.geoObjects.remove(targetPoint);
        if(targetPoint){
            if(e.get('target').geometry.getCoordinates()[0] == targetPoint[0] && e.get('target').geometry.getCoordinates()[1]==targetPoint[1]){
                targetPoint = null;
                return;
            }
        }
        e.get('target').options.set('preset', 'islands#greenIcon');
        targetPoint = [[e.get('target').geometry.getCoordinates()[0]], [e.get('target').geometry.getCoordinates()[1]]];
        createRoute();
    });

    myMap.controls.add(exchangeRoute, {
        float: 'right'
    });
    myMap.controls.add(pedestrianRouteItem, {
        float: 'left'
    });
    myMap.controls.add(masstransitRouteItem, {
        float: 'left'
    });
    myMap.controls.add(autoRouteItem, {
        float: 'left'
    });
    
    autoRouteItem.events.add('select', function (e) { createRoute('auto'); });
    masstransitRouteItem.events.add('select', function (e) { createRoute('masstransit'); });
    pedestrianRouteItem.events.add('select', function (e) { createRoute('pedestrian'); });

    exchangeRoute.events.add('select', function (e) {
        reverseRoute(true);
     });
    exchangeRoute.events.add('deselect', function (e) {
        reverseRoute();
     });
    function reverseRoute(select){
        if(sourcePoint)
            if(select){
                sourcePoint.properties.set('iconContent', 'Сюда');
            }else{
                sourcePoint.properties.set('iconContent', 'Отсюда');
            }
        if(currentRoutingMode){
            switch(currentRoutingMode){
                case 'auto':autoRouteItem.select();autoRouteItem.events.fire('select');return;
                case 'masstransit':masstransitRouteItem.select();masstransitRouteItem.events.fire('select');return;
                case 'pedestrian':pedestrianRouteItem.select();pedestrianRouteItem.events.fire('select');return;
            }
        }
     }

    // Подписываемся на события, информирующие о трёх типах выбора начальной точки маршрута:
    // клик по карте, отображение результата поиска или геолокация.
    myMap.events.add('click', onMapClick);
    geolocationControl.events.add('locationchange', onGeolocate);

    /*
     * Следующие функции реагируют на нужные события, удаляют с карты предыдущие результаты,
     * переопределяют точку отправления и инициируют перестроение маршрута.
     */

    function onMapClick (e) {
        clearSourcePoint();
        if(exchangeRoute._selected){
            sourcePoint = new ymaps.Placemark(e.get('coords'), { iconContent: 'Сюда' }, { preset: 'islands#greenStretchyIcon' });
        }else{
            sourcePoint = new ymaps.Placemark(e.get('coords'), { iconContent: 'Отсюда' }, { preset: 'islands#greenStretchyIcon' });
        }
        myMap.geoObjects.add(sourcePoint);
        createRoute();
    }

    function onGeolocate (e) {
        clearSourcePoint();
        sourcePoint = e.get('geoObjects').get(0);
        if(currentRoutingMode){
            createRoute();
        }else{
            autoRouteItem.select();
            autoRouteItem.events.fire('select');
        }   
    }

    function clearSourcePoint () {
        if (sourcePoint) {
            myMap.geoObjects.remove(sourcePoint);
            sourcePoint = null;
        }
    }

    /*
     * Функция, создающая маршрут.
     */
    function createRoute (routingMode) {
        if(!autoRouteItem._selected && !masstransitRouteItem._selected && !pedestrianRouteItem._selected){
            routingMode = currentRoutingMode;
            clearRoute();
            currentRoutingMode = routingMode;
            return;
        }

        // Если `routingMode` был передан, значит вызов происходит по клику на пункте выбора типа маршрута,
        // следовательно снимаем выделение с другого пункта, отмечаем текущий пункт и закрываем список.
        // В противном случае — перестраиваем уже имеющийся маршрут или ничего не делаем.
        if (routingMode) {
            if (routingMode == 'auto') {
                masstransitRouteItem.deselect();
                pedestrianRouteItem.deselect();
            } else if (routingMode == 'masstransit') {
                autoRouteItem.deselect();
                pedestrianRouteItem.deselect();
            } else if (routingMode == 'pedestrian') {
                autoRouteItem.deselect();
                masstransitRouteItem.deselect();
            }
        } else if (currentRoutingMode) {
            routingMode = currentRoutingMode;
        } else {
            return;
        }

        // Если начальная точка маршрута еще не выбрана, ничего не делаем.
        if (!sourcePoint) {
            currentRoutingMode = routingMode;
            if(targetPoint){
                if(!flag){
                    geolocationControl.events.fire('press');
                }
                return;
            }else{
                flag = true;
                ymaps.geolocation.get({}).then(function (result) {
                    flag = false;
                    sourcePoint = result.geoObjects.get(0).geometry.getCoordinates();
                    createRoute();
                    return;
                });
            }
        }

        if(sourcePoint && routingMode){
            if(exchangeRoute._selected){
                $('.reverse').css('display', 'inline-block');
                $('.reverse').animate({'opacity': 1}, 1500);
                $('.reverse').animate({'opacity': 0}, 1500, function(e){
                    $(this).css('display', 'none');
                });
            }else{
                $('.forward').css('display', 'inline-block');
                $('.forward').animate({'opacity': 1}, 1500);
                $('.forward').animate({'opacity': 0}, 1500, function(e){
                    $(this).css('display', 'none');
                });
            }
        }
        
        // Стираем предыдущий маршрут.
        clearRoute();

        currentRoutingMode = routingMode;

        // Создаём маршрут нужного типа из начальной в конечную точку.
        if(targetPoint){
            //Если выбран обратный маршрут меняем значение начальной и конечной точек
            if(exchangeRoute._selected){
                targetPoint = [sourcePoint, sourcePoint = targetPoint][0]
            }
            currentRoute = new ymaps.multiRouter.MultiRoute({
                referencePoints: [sourcePoint, targetPoint],
                params: { routingMode: routingMode }
            }, {
                boundsAutoApply: true
            });
            if(exchangeRoute._selected){
                targetPoint = [sourcePoint, sourcePoint = targetPoint][0]
            }
            // Добавляем маршрут на карту.
            myMap.geoObjects.add(currentRoute);
        }
    }

    function clearRoute () {
        myMap.geoObjects.remove(currentRoute);
        currentRoute = currentRoutingMode = null;
    }
    
    function showMessage(){
        
    }

    // Инициализируем карту.
    var myMap = new ymaps.Map('map_2', {
        center: points[0],
        zoom: 13,
        controls: [autoRouteItem, masstransitRouteItem, pedestrianRouteItem, exchangeRoute, zoomControl, geolocationControl],
        geoObjects: myCollection
    }, {
            // Ограничиваем количество результатов поиска.
            searchControlResults: 1,

            // Отменяем автоцентрирование к найденным адресам.
            searchControlNoCentering: true,

            // Разрешаем кнопкам нужную длину.
            buttonMaxWidth: 150
        });
});
