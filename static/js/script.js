//------ появление объектов при скролле -------

let animItems = document.querySelectorAll('._anim-items');

if (animItems.length > 0) {
    window.addEventListener('scroll', animOnScroll)

    function animOnScroll(params) {
        for (let index = 0; index < animItems.length; index++) {
            const animItem = animItems[index];
            const animItemHeight = animItem.offsetHeight;
            const animItemOffset = offset(animItem).top
            const animStart = 4;

            let animItemPoint = window.innerHeight - animItemHeight / animStart
            if (animItemPoint > window.innerHeight) {
                animItemPoint = window.innerHeight - window.innerHeight / animStart
            }

            if((pageYOffset > animItemOffset - animItemPoint) && pageYOffset < (animItemOffset + animItemHeight)) {
                animItem.classList.add('_active')
            }
            else {
                animItem.classList.remove('_active')
            }
        }
    }

    function offset(el) {
        const rect = el.getBoundingClientRect(),
            scrollLeft = window.pageXOffset || document.documentElement.scrollLeft,
            scrolTop = window.pageYOffset || document.documentElement.scrollTop;
        return { top: rect.top + scrolTop, left: rect.left + scrollLeft}
    }
    
    setTimeout(() => {
        animOnScroll();
    }, 300);
}

// ------------------

// -----parallax-----

let bg = document.querySelectorAll('.mouse-parallax-bg');

window.addEventListener('mousemove', para)

function para(e) {
    for (let index = 0; index < bg.length; index++) {
        let x = e.clientX / window.innerWidth;
        let y = e.clientY / window.innerHeight;  
        bg[index].style.transform = 'translate(-' + x * 20 + 'px, -' + y * 20 + 'px)';
    }
}


// Объявить переменную модального окна в текущей области видимости
var modal = document.getElementById('myModal');

// Переменная кнопки, открывающей модальное окно
let btns = document.querySelectorAll(".myBtn");

// Получение элемента <span>, который закрывает модальное окно
var span = document.getElementsByClassName("close")[0];

// Когда пользователь нажимает кнопку, открывается pop-up форма 
for (let btn of btns) {
    btn.onclick = function() {
        modal.style.display = "block";
    }
}
// Когда пользователь нажимает кнопку (x) <span>, закрывается окно формы
span.onclick = function() {
    modal.style.display = "none";
}
// Когда пользователь нажимает в любое место вне формы, закрыть окно формы
window.onclick = function(event) {
    if (event.target == modal) {
    modal.style.display = "none";
    }
}


//------------------

// -----движение объектов-----

// function positionTheDot() {


//     var cScroll = this.scrolTop,
//     p = cScroll * maxHP,
//     y = maxHP - p * 10,
//     x = maxHP;
//     path.offsetTop = y
//     path.offsetLeft = x
//   };

// var path = document.querySelector(".header-text"),
//  winHP = window.innerHeight / 100,
//  maxHP = 100 / (document.innerHeight - window.innerHeight + path.innerHeight * 2);

// window.addEventListener('scroll', positionTheDot);
