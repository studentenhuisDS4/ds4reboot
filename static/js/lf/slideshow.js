var slideIndex = 0;
var maxSlides = 0;
showSlides();

function showSlides() {
    var i;
    var slides = document.getElementsByClassName("mySlides");
    var dots = document.getElementsByClassName("dot");

    const slideshow_container = document.querySelector('.slideshow-container');
    if (slideshow_container === null) {
        return;
    }
    if ('slides' in slideshow_container.dataset) {
        maxSlides = slideshow_container.dataset.slides;
    } else {
        return;
    }

    for (i = 0; i < maxSlides; i++) {
        slides[i].style.display = "none";  
    }
    slideIndex++;
    if (slideIndex > maxSlides) {slideIndex = 1}    
    for (i = 0; i < maxSlides; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
    }
    slides[slideIndex-1].style.display = "block";  
    dots[slideIndex-1].className += " active";
    setTimeout(showSlides, 3000); // Change image every 2 seconds
}
