/**
 * WEBSITE: https://themefisher.com
 * TWITTER: https://twitter.com/themefisher
 * FACEBOOK: https://www.facebook.com/themefisher
 * GITHUB: https://github.com/themefisher/
 */
$(document).ready(function () {
    starbucks();
});
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
                let temp_html = `<div class="col-lg-4 col-6 mb-4 shuffle-item"  data-groups="[&quot;design&quot;,&quot;illustration&quot;]">
                            <div class="position-relative inner-box">
                            <div class="image position-relative ">
                            <img src="${url}" alt="portfolio-image" class="img-fluid w-100 d-block">
                            <div class="overlay-box">
                            <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger"
                            >99+</span>
                            <div class="overlay-inner">
                            <a class="overlay-content" href="portfolio-single.html">
                            <h5 class="mb-0">${name}</h5>
                            <p>즐겨찾기1</p>
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
                let temp_html = `<div class="col-lg-4 col-6 mb-4 shuffle-item"  data-groups="[&quot;design&quot;,&quot;illustration&quot;]">
                            <div class="position-relative inner-box">
                            <div class="image position-relative ">
                            <img src="${url}" alt="portfolio-image" class="img-fluid w-100 d-block">
                            <div class="overlay-box">
                            <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger"
                            >99+</span>
                            <div class="overlay-inner">
                            <a class="overlay-content" href="portfolio-single.html">
                            <h5 class="mb-0">${name}</h5>
                            <p>즐겨찾기1</p>
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
                let temp_html = `<div class="col-lg-4 col-6 mb-4 shuffle-item"  data-groups="[&quot;design&quot;,&quot;illustration&quot;]">
                            <div class="position-relative inner-box">
                            <div class="image position-relative ">
                            <img src="${url}" alt="portfolio-image" class="img-fluid w-100 d-block">
                            <div class="overlay-box">
                            <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger"
                            >99+</span>
                            <div class="overlay-inner">
                            <a class="overlay-content" href="portfolio-single.html">
                            <h5 class="mb-0">${name}</h5>
                            <p>즐겨찾기1</p>
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
                let temp_html = `<div class="col-lg-4 col-6 mb-4 shuffle-item"  data-groups="[&quot;design&quot;,&quot;illustration&quot;]">
                            <div class="position-relative inner-box">
                            <div class="image position-relative ">
                            <img src="${url}" alt="portfolio-image" class="img-fluid w-100 d-block">
                            <div class="overlay-box">
                            <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger"
                            >99+</span>
                            <div class="overlay-inner">
                            <a class="overlay-content" a href="javascript:void(0);" onclick="favorites_send();">
                            <h5 class="mb-0">${name}</h5>
                            <p class="test">${id}</p>
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

function favorites_send() {
    $.ajax({
        type: 'POST',
        url: '/favorites_send',
        data: {coffee_id : $('.test').text()},
        success: function (response) {
            alert(response['msg'])
            console.log()
        }
    })
}

var swiper = new Swiper(".mySwiper", {
        slidesPerView: 2,
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
