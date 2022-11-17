
/**
 * WEBSITE: https://themefisher.com
 * TWITTER: https://twitter.com/themefisher
 * FACEBOOK: https://www.facebook.com/themefisher
 * GITHUB: https://github.com/themefisher/
 */
$(document).ready(function () {
    starbucks();
})

// 커피별 GET 함수
function ediya() {
    $.ajax({
        type: 'GET',
        url: '/ediya',
        data: {},
        success: function (response) {
            $('#wrap').empty()
            let rows = response['ediya']
            for (let i = 0; i < rows.length; i++) {
                let id = rows[i]['coffee_id']
                let name = rows[i]['coffee_name']
                let url = rows[i]['coffee_image']
                let favorites = rows[i]['favorites']
                let temp_html = `<div class="col-lg-4 col-6 mb-4 shuffle-item"  data-groups="[&quot;design&quot;,&quot;illustration&quot;]">
                            <div class="position-relative inner-box">
                            <div class="image position-relative ">
                            <h3><span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger"
                            style="margin-top: 9px; opacity: 1; z-index: 1; transform: scale(1.1);" >⭐ ${favorites}</span></h3>
                            <img src="${url}" alt="portfolio-image" class="img-fluid w-100 d-block">
                            <div class="overlay-box">
                            <div class="overlay-inner">
                            <a class="overlay-content">
                            <h5 class="mb-0">${name}</h5>
                            <p class="test" onclick="send_id(${id})" style="cursor: pointer">즐겨찾기 등록</p>
                            <p onclick="location.href='/coffee/${id}'" style="cursor: pointer">상세페이지 이동</p>
                            </a>
                            </div>
                            </div>
                            </div>
                            </div>
                            </div>`
                $('#wrap').append(temp_html)
            }
        }
    })
}

function starbucks() {
    $.ajax({
        type: 'GET',
        url: '/starbucks',
        data: {},
        success: function (response) {
            $('#wrap').empty()
            let rows = response['starbucks']
            for (let i = 0; i < rows.length; i++) {
                let id = rows[i]['coffee_id']
                let name = rows[i]['coffee_name']
                let url = rows[i]['coffee_image']
                let favorites = rows[i]['favorites']
                let temp_html = `<div class="col-lg-4 col-6 mb-4 shuffle-item"  data-groups="[&quot;design&quot;,&quot;illustration&quot;]">
                            <div class="position-relative inner-box">
                            <div class="image position-relative ">
                            <h3><span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger"
                            style="margin-top: 9px; opacity: 1; z-index: 1; transform: scale(1.1);" >⭐ ${favorites}</span></h3>
                            <img src="${url}" alt="portfolio-image" class="img-fluid w-100 d-block">
                            <div class="overlay-box">
                            <div class="overlay-inner">
                            <a class="overlay-content">
                            <h5 class="mb-0">${name}</h5>
                            <p class="test" onclick="send_id(${id})" style="cursor: pointer">즐겨찾기 등록</p>
                            <p onclick="location.href='/coffee/${id}'" style="cursor: pointer">상세페이지 이동</p>
                            </a>
                            </div>
                            </div>
                            </div>
                            </div>
                            </div>`
                $('#wrap').append(temp_html)
            }

        }
    })
}

function hollys() {
    $.ajax({
        type: 'GET',
        url: '/hollys',
        data: {},
        success: function (response) {
            $('#wrap').empty()
            let rows = response['hollys']
            for (let i = 0; i < rows.length; i++) {
                let id = rows[i]['coffee_id']
                let name = rows[i]['coffee_name']
                let url = rows[i]['coffee_image']
                let favorites = rows[i]['favorites']
                let temp_html = `<div class="col-lg-4 col-6 mb-4 shuffle-item"  data-groups="[&quot;design&quot;,&quot;illustration&quot;]">
                            <div class="position-relative inner-box">
                            <div class="image position-relative ">
                            <h3><span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger"
                            style="margin-top: 9px; opacity: 1; z-index: 1; transform: scale(1.1);" >⭐ ${favorites}</span></h3>
                            <img src="${url}" alt="portfolio-image" class="img-fluid w-100 d-block">
                            <div class="overlay-box">
                            <div class="overlay-inner">
                            <a class="overlay-content">
                            <h5 class="mb-0">${name}</h5>
                            <p class="test" onclick="send_id(${id})" style="cursor: pointer">즐겨찾기 등록</p>
                            <p onclick="location.href='/coffee/${id}'" style="cursor: pointer">상세페이지 이동</p>
                            </a>
                            </div>
                            </div>
                            </div>
                            </div>
                            </div>`
                $('#wrap').append(temp_html)
            }
        }
    })
}

function paikdabang() {
    $.ajax({
        type: 'GET',
        url: '/paikdabang',
        data: {},
        success: function (response) {
            $('#wrap').empty()
            let rows = response['paikdabang']
            for (let i = 0; i < rows.length; i++) {
                let id = rows[i]['coffee_id']
                let name = rows[i]['coffee_name']
                let url = rows[i]['coffee_image']
                let favorites = rows[i]['favorites']
                let temp_html = `<div class="col-lg-4 col-6 mb-4 shuffle-item"  data-groups="[&quot;design&quot;,&quot;illustration&quot;]">
                            <div class="position-relative inner-box">
                            <div class="image position-relative ">
                            <h3><span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger"
                            style="margin-top: 9px; opacity: 1; z-index: 1; transform: scale(1.1);" >⭐ ${favorites}</span></h3>
                            <img src="${url}" alt="portfolio-image" class="img-fluid w-100 d-block">
                            <div class="overlay-box">
                            <div class="overlay-inner">
                            <a class="overlay-content">
                            <h5 class="mb-0">${name}</h5>
                            <p class="test" onclick="send_id(${id})" style="cursor: pointer">즐겨찾기 등록</p>
                            <p onclick="location.href='/${id}'" style="cursor: pointer">상세페이지 이동</p>
                            </a>
                            </div>
                            </div>
                            </div>
                            </div>
                            </div>`
                $('#wrap').append(temp_html)
            }

        }
    })
}

function send_id(item) {
    $.ajax({
        type: 'POST',
        url: '/favorites_send',
        data: {coffee_id : item},
        success: function (response) {
            alert(response['msg'])
            if (response['cafe'] <= 50) {
                hollys();
            }else if (response['cafe'] <= 98) {
                ediya();
            }else if (response['cafe'] <= 247) {
                starbucks();
            }else if (response['cafe'] <= 342){
                paikdabang();
            } else {
                starbucks();
            }
        }
    })
}

var swiper = new Swiper(".mySwiper", {
        // slidesPerView: 2,
        slidesPerView: 3,
        spaceBetween: 30,
        pagination: {
          el: ".swiper-pagination",
          clickable: true,
        },
		navigation : { // 네비게이션
        nextEl : '.swiper-button-next', // 오른쪽(다음) 화살표
        prevEl : '.swiper-button-prev', // 왼쪽(이전) 화살표
    	},
		  autoplay: {
			disableOnInteraction: false, // 화살표 눌러도 autoplay 멈추지 않음
		  },
      });

