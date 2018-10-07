if(!$('.map').attr('width')){
    $('.map').css({"width":"80%", "height":"400px"});
}
ymaps.ready(function () {
    if (!$.isEmptyObject(maps)) {
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
            ),
            BalloonContentLayout = ymaps.templateLayoutFactory.createClass(
                '<address>' +
                '<strong>{{ properties.object }}</strong>' +
                '<br />' +
                '{{ properties.address }}' +
                '<br />' +
                '{{ properties.baloon|raw }}' +
                '</address>', {}
            );

        var flag;

        var sourcePoint,
            targetPoint;
        
        var currentRoute,
            currentRoutingMode;


        Object.keys(maps).forEach(function (key) {
            
            window[key + 'Map'] = new ymaps.Map(key, {
                center: maps[key][1]['coords'],
                zoom: 13,
                controls: [autoRouteItem, masstransitRouteItem, pedestrianRouteItem, exchangeRoute, zoomControl, geolocationControl],
            }, {
                searchControlResults: 1,
                searchControlNoCentering: true,
                buttonMaxWidth: 150
            });

            window[key+'Collection'] = new ymaps.GeoObjectCollection();

            if (key.length) {
                for (i = 1; i <= Object.keys(maps[key]).length; i++) {
                    var myPlacemark = new ymaps.Placemark([
                        maps[key][i]['coords'][0], maps[key][i]['coords'][1]], {
                            preset: 'islands#icon',
                            address: maps[key][i]['address'],
                            object: maps[key][i]['object'],
                            // baloon: maps[key][i]['baloon']
                        }, {
                            balloonContentLayout: BalloonContentLayout,
                            hintLayout: HintLayout,
                            hintPane: 'hint',
                            balloonPanelMaxMapArea: 'Infinity',
                            balloonAutoPan: false
                        }
                    );
                    if (maps[key][i]['baloon'].length) {
                        myPlacemark.properties.set('balloonContent', maps[key][i]['baloon']);
                    }
                    console.log(myPlacemark);
                    window[key + 'Collection'].add(myPlacemark)
                };
                window[key + 'Map'].geoObjects.add(window[key + 'Collection']);
                
                window[key + 'Map'].setBounds(window[key + 'Map'].geoObjects.getBounds(), { checkZoomRange: true }).then(function () { if (window[key + 'Map'].getZoom() > 13) window[key + 'Map'].setZoom(16); });
            };

            window[key + 'Collection'].events.add('click', function (e) {
                
                window[key + 'Collection'].each(function (e) {
                    e.options.set('preset', 'islands#blueIcon');
                });
                window[key + 'Map'].geoObjects.remove(targetPoint);
                if (targetPoint) {
                    if (e.get('target').geometry.getCoordinates()[0] == targetPoint[0] && e.get('target').geometry.getCoordinates()[1] == targetPoint[1]) {
                        targetPoint = null;
                        return;
                    }
                }
                e.get('target').options.set('preset', 'islands#greenIcon');
                targetPoint = [[e.get('target').geometry.getCoordinates()[0]], [e.get('target').geometry.getCoordinates()[1]]];
                createRoute();
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
            function reverseRoute(select) {
                if (sourcePoint)
                    if (select) {
                        sourcePoint.properties.set('iconContent', 'Сюда');
                    } else {
                        sourcePoint.properties.set('iconContent', 'Отсюда');
                    }
                if (currentRoutingMode) {
                    switch (currentRoutingMode) {
                        case 'auto': autoRouteItem.select(); autoRouteItem.events.fire('select'); return;
                        case 'masstransit': masstransitRouteItem.select(); masstransitRouteItem.events.fire('select'); return;
                        case 'pedestrian': pedestrianRouteItem.select(); pedestrianRouteItem.events.fire('select'); return;
                    }
                }
            }

            window[key + 'Map'].events.add('click', onMapClick);
            geolocationControl.events.add('locationchange', onGeolocate);

            function onMapClick(e) {
                clearSourcePoint();
                if (exchangeRoute._selected) {
                    sourcePoint = new ymaps.Placemark(e.get('coords'), { iconContent: 'Сюда' }, { preset: 'islands#greenStretchyIcon' });
                } else {
                    sourcePoint = new ymaps.Placemark(e.get('coords'), { iconContent: 'Отсюда' }, { preset: 'islands#greenStretchyIcon' });
                }
                window[key + 'Map'].geoObjects.add(sourcePoint);
                createRoute();
            }

            function onGeolocate(e) {
                clearSourcePoint();
                sourcePoint = e.get('geoObjects').get(0);
                if (currentRoutingMode) {
                    createRoute();
                } else {
                    autoRouteItem.select();
                    autoRouteItem.events.fire('select');
                }
            }

            function clearSourcePoint() {
                if (sourcePoint) {
                    window[key + 'Map'].geoObjects.remove(sourcePoint);
                    sourcePoint = null;
                }
            }
            
            function createRoute(routingMode) {
                if (!autoRouteItem._selected && !masstransitRouteItem._selected && !pedestrianRouteItem._selected) {
                    routingMode = currentRoutingMode;
                    clearRoute();
                    currentRoutingMode = routingMode;
                    return;
                }

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
                
                if (!sourcePoint) {
                    currentRoutingMode = routingMode;
                    if (targetPoint) {
                        if (!flag) {
                            geolocationControl.events.fire('press');
                        }
                        return;
                    } else {
                        flag = true;
                        ymaps.geolocation.get({}).then(function (result) {
                            flag = false;
                            sourcePoint = result.geoObjects.get(0).geometry.getCoordinates();
                            createRoute();
                            return;
                        });
                    }
                }

                if (sourcePoint && routingMode) {
                    if (exchangeRoute._selected) {
                        $('.reverse').css('display', 'inline-block');
                        $('.reverse').animate({ 'opacity': 1 }, 1500);
                        $('.reverse').animate({ 'opacity': 0 }, 1500, function (e) {
                            $(this).css('display', 'none');
                        });
                    } else {
                        $('.forward').css('display', 'inline-block');
                        $('.forward').animate({ 'opacity': 1 }, 1500);
                        $('.forward').animate({ 'opacity': 0 }, 1500, function (e) {
                            $(this).css('display', 'none');
                        });
                    }
                }
                
                clearRoute();

                currentRoutingMode = routingMode;
                
                if (targetPoint) {
                    if (exchangeRoute._selected) {
                        targetPoint = [sourcePoint, sourcePoint = targetPoint][0]
                    }
                    currentRoute = new ymaps.multiRouter.MultiRoute({
                        referencePoints: [sourcePoint, targetPoint],
                        params: { routingMode: routingMode }
                    }, {
                            boundsAutoApply: true
                        });
                    if (exchangeRoute._selected) {
                        targetPoint = [sourcePoint, sourcePoint = targetPoint][0]
                    }
                    window[key + 'Map'].geoObjects.add(currentRoute);
                }
            }

            function clearRoute() {
                window[key + 'Map'].geoObjects.remove(currentRoute);
                currentRoute = currentRoutingMode = null;
            }

            function showMessage() {

            }
        })
    }
});
