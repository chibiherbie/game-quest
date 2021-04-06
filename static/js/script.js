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
            // else {
            //     animItem.classList.remove('_active')
            // }
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
