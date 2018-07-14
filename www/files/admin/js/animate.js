document.addEventListener("DOMContentLoaded", function () {
    var anime = document.createElement('span');
    var h1 = document.createElement('h1');
    h1.innerHTML = 'Animate';
    h1.classList.className = 'animation';
    h1.style.display = 'inline';
    anime.appendChild(h1);
    anime.id = "image-animation";
    anime.style.display = 'inline-block';
    h1.style.display = 'inline-block';
    select = document.getElementById('id_animate');
    select.parentElement.appendChild(anime);
    function change() {
        anime.className = 'animated '+this.value;
    };
    select.onchange = change;
})