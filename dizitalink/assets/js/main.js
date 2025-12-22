(function($) {
	'use strict';
	
	jQuery(document).on('ready', function(){

const dropdownIcon = document.querySelectorAll(".dropdown__container")
const dropdownMenu = document.querySelectorAll(".dropdown__container_menu")
dropdownIcon.forEach((ele, index) => {
    ele.addEventListener("click", () => {
        console.log("click")
        dropdownMenu.forEach((ele, id) => {
            if (index === id) {
                ele.classList.toggle("dropdown__container_menu-active")
            }
        })
    })
})

const menuIcon = document.querySelector(".menu__icon");
const bottomNavbar = document.querySelector(".header__bottom_navbar")
menuIcon.addEventListener("click", () => {
    bottomNavbar.classList.toggle("header__bottom_navbar-active")
})


function toggleOptions() {
    var options = document.getElementById('customSelect').getElementsByClassName('select-options')[0];
    options.style.display = options.style.display === 'none' ? 'block' : 'none';
}

function selectOption(option) {
    var selectedValue = option.innerText;
    var selectStyled = document.getElementById('customSelect').getElementsByClassName('select-styled')[0];
    selectStyled.innerText = selectedValue;
    toggleOptions();
}

// Close the dropdown if the user clicks outside of it
window.onclick = function (event) {
    if (!event.target.matches('.select-styled')) {
        var options = document.getElementById('customSelect').getElementsByClassName('select-options')[0];
        if (options.style.display === 'block') {
            options.style.display = 'none';
        }
    }
}

$('.testimonial__slides').slick({
    slidesToShow: 2,
    slidesToScroll: 1,
    autoplay: false,
    autoplaySpeed: 2000,
    arrows: true,
    dots: true,
    responsive: [
        {
            breakpoint: 1270,
            settings: {
                dots: false,
            }
        },
        {
            breakpoint: 991,
            settings: {
                slidesToShow: 1,
                dots: false,
            }
        }
    ],
    prevArrow: '<i class="fa-solid fa-arrow-right slide__nav prev-arrow"></i>',
    nextArrow: '<i class="fa-solid fa-arrow-left slide__nav next-arrow"></i>',
    customPaging: function (slider, i) {
        return `<div class="slide__dots" id=${i}> 0${i + 1} </div>`;
    },
});

$('.testimonial__slides_2').slick({
    slidesToShow: 1,
    slidesToScroll: 1,
    autoplay: false,
    autoplaySpeed: 2000,
    arrows: true,
    dots: true,
    responsive: [
        {
            breakpoint: 1270,
            settings: {
                dots: false,
            }
        },
        {
            breakpoint: 991,
            settings: {
                slidesToShow: 1,
                dots: false,
            }
        }
    ],
    prevArrow: '<i class="fa-solid fa-arrow-right slide__nav prev-arrow"></i>',
    nextArrow: '<i class="fa-solid fa-arrow-left slide__nav next-arrow"></i>',
    customPaging: function (slider, i) {
        return `<div class="slide__dots" id=${i}> 0${i + 1} </div>`;
    },
});


AOS.init();


/*START VIDEO JS*/
$('.video-play').magnificPopup({
    type: 'iframe'
});
/*END VIDEO JS*/

}); 

})(jQuery);