// Visible plugin

(function($){

    var items = [];
    
    function winPos(win) {
        return { x: 0, y: 0, x2: win.width() - 1, y2: win.height() - 1 };
    }
   
    function pos(win, el) {
        var p = el.offset();
        var x = p.left - win.scrollLeft();
        var y = p.top - win.scrollTop();
        return { x: x, y: y, x2: x + el.width() -1, y2: y + el.height() - 1 };
    }
    
    function intersects(a, b) {
        return !(a.x2 < b.x || a.x > b.x2 || a.y2 < b.y || a.y > b.y2);
    }
    
    function check(win, w, item) {
        var p = pos(win, $(item.el));
        var s = intersects(w, p);
        if (s != item.shown) {
            item.shown = s;
            if(s){
                if(item.show){
                    item.show.call(item.el);
                }
            }else{
                if(item.hide){
                    item.hide.call(item.el);
                }
            }
            //(s ? item.show : item.hide).call(item.el);
        }
    }

    $.fn.visible = function(show, hide){
        var win = $(window), w = winPos(win);
        return this.each(function(i, el){
            var item = { el: el, show: show, hide: hide, shown: false };
            items.push(item);
            check(win, w, item);
        });
    };
    
    $(window).on('scroll resize', function(e){
        var win = $(window), w = winPos(win);
        for (var i = 0; i < items.length; i++) {
            check(win, w, items[i]);
        }
    });

})(jQuery);

// Usage
//$('.section > .title').addClass('before');
function animate(){
    if($(this).hasClass('before')){
        $(this).addClass('animated').removeClass('before');
    }
}
$('.section > .title').visible(animate);
