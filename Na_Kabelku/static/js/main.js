(function($) {
	"use strict"

	// Mobile Nav toggle
	$('.menu-toggle > a').on('click', function (e) {
		e.preventDefault();
		$('#responsive-nav').toggleClass('active');
	})

	// Fix cart dropdown from closing
	$('.cart-dropdown').on('click', function (e) {
		e.stopPropagation();
	});

	/////////////////////////////////////////

	// Products Slick
	$('.products-slick').each(function() {
		var $this = $(this),
				$nav = $this.attr('data-nav');

		$this.slick({
			slidesToShow: 4,
			slidesToScroll: 1,
			autoplay: true,
			infinite: true,
			speed: 300,
			dots: false,
			arrows: true,
			appendArrows: $nav ? $nav : false,
			responsive: [{
	        breakpoint: 991,
	        settings: {
	          slidesToShow: 2,
	          slidesToScroll: 1,
	        }
	      },
	      {
	        breakpoint: 480,
	        settings: {
	          slidesToShow: 1,
	          slidesToScroll: 1,
	        }
	      },
	    ]
		});
	});

	// Products Widget Slick
	$('.products-widget-slick').each(function() {
		var $this = $(this),
				$nav = $this.attr('data-nav');

		$this.slick({
			infinite: true,
			autoplay: true,
			speed: 300,
			dots: false,
			arrows: true,
			appendArrows: $nav ? $nav : false,
		});
	});

	/////////////////////////////////////////

	// Product Main img Slick
	$('#product-main-img').slick({
    infinite: true,
    speed: 300,
    dots: false,
    arrows: true,
    fade: true,
    asNavFor: '#product-imgs',
  });

	// Product imgs Slick
  $('#product-imgs').slick({
    slidesToShow: 3,
    slidesToScroll: 1,
    arrows: true,
    centerMode: true,
    focusOnSelect: true,
		centerPadding: 0,
		vertical: true,
    asNavFor: '#product-main-img',
		responsive: [{
        breakpoint: 991,
        settings: {
					vertical: false,
					arrows: false,
					dots: true,
        }
      },
    ]
  });

	// Product img zoom
	var zoomMainProduct = document.getElementById('product-main-img');
	if (zoomMainProduct) {
		$('#product-main-img .product-preview').zoom();
	}

	/////////////////////////////////////////

	// Input number
	$('.input-number').each(function() {
		var $this = $(this),
		$input = $this.find('input[type="number"]'),
		up = $this.find('.qty-up'),
		down = $this.find('.qty-down');

		down.on('click', function () {
			var value = parseInt($input.val()) - 1;
			value = value < 0 ? 0 : value;
			$input.val(value);
			$input.change();
			updatePriceSlider($this , value)
		})

		up.on('click', function () {
			var value = parseInt($input.val()) + 1;
			var maxValue = parseInt($input.attr('max'));

			if(value > maxValue)
				value = maxValue;

			$input.val(value);
			$input.change();
			updatePriceSlider($this , value)
		})
	});

	var priceInputMax = document.getElementById('price-max'),
			priceInputMin = document.getElementById('price-min');

	priceInputMax.addEventListener('change', function(){
		updatePriceSlider($(this).parent() , this.value);
	});

	priceInputMin.addEventListener('change', function(){
		updatePriceSlider($(this).parent() , this.value)
	});

	function updatePriceSlider(elem , value) {
		if ( elem.hasClass('price-min') ) {
			priceSlider.noUiSlider.set([value, null]);
		} else if ( elem.hasClass('price-max')) {
			priceSlider.noUiSlider.set([null, value]);
		}
	}

	// Price Slider
	var priceSlider = document.getElementById('price-slider');
	var currentUrl = window.location.href;
	var url = new URL(currentUrl);
	const params = new URLSearchParams(url.search);
	let max_price = params.get('max-price');
	let min_price = params.get('min-price');

	max_price = max_price ? max_price : 5999;
	min_price = min_price ? min_price : 1;

	if (priceSlider) {
		noUiSlider.create(priceSlider, {
			start: [min_price, max_price],
			connect: true,
			step: 1,
			range: {
				'min': 1,
				'max': 5999
			}
		});
		priceSlider.noUiSlider.on('update', function( values, handle ) {
			var value = values[handle];
			handle ? priceInputMax.value = value : priceInputMin.value = value;
		});
	}


	// // Timer to friday
	// function getNextFridayAtNine() {
	// 	const now = new Date();
	// 	const dayOfWeek = now.getDay();
	// 	const nextFriday = new Date(now);
	// 	console.log(now);

	// 	let daysUntilFriday = (5 - dayOfWeek + 7) % 7;

	// 	if (dayOfWeek === 5 && now.getHours() >= 9) {
	// 		daysUntilFriday += 7;
	// 	}

	// 	nextFriday.setDate(now.getDate() + daysUntilFriday);
	// 	nextFriday.setHours(9, 0, 0, 0);  // Set time to 9:00 AM

	// 	return nextFriday;
	// }

	// function updateTimer() {
	// 	const now = new Date();
	// 	const nextFriday = getNextFridayAtNine();

	// 	const timeDiff = nextFriday - now;

	// 	const days = Math.floor(timeDiff / (1000 * 60 * 60 * 24));
	// 	const hours = Math.floor((timeDiff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
	// 	const minutes = Math.floor((timeDiff % (1000 * 60 * 60)) / (1000 * 60));
	// 	const seconds = Math.floor((timeDiff % (1000 * 60)) / 1000);

	// 	console.log(days)

	// 	document.getElementById("days").innerHTML = "siema";
	// }

	// setInterval(updateTimer, 1000);

})(jQuery);
