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
			value = value < 1 ? 1 : value;
			$input.val(value);
			$input.change();
			updatePriceSlider($this , value);
			
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

		$input.on('change', function(){
			var value = parseInt(this.value);
			var maxValue = parseInt(this.max);

			if(value > maxValue)
				value = maxValue;

			if(value < 1)
				value = 1;

			this.value = value;
		})
	});

	var priceInputMax = document.getElementById('price-max'),
			priceInputMin = document.getElementById('price-min');
	if(priceInputMax){
		priceInputMax.addEventListener('change', function(){
			updatePriceSlider($(this).parent() , this.value);
		});
	}
	if(priceInputMin){
		priceInputMin.addEventListener('change', function(){
			updatePriceSlider($(this).parent() , this.value)
		});
	}

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

	// Timer to friday
	function getNextFridayAtNine() {
		const now = new Date();
		const dayOfWeek = now.getDay();
		const nextFriday = new Date(now);

		let daysUntilFriday = (5 - dayOfWeek + 7) % 7;

		if (dayOfWeek === 5 && now.getHours() >= 9) {
			daysUntilFriday += 7;
		}

		nextFriday.setDate(now.getDate() + daysUntilFriday);
		nextFriday.setHours(9, 0, 0, 0);

		return nextFriday;
	}

	function updateTimer() {
		const now = new Date();
		const nextFriday = getNextFridayAtNine();

		const timeDiff = nextFriday - now;

		const days = Math.floor(timeDiff / (1000 * 60 * 60 * 24));
		const hours = Math.floor((timeDiff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
		const minutes = Math.floor((timeDiff % (1000 * 60 * 60)) / (1000 * 60));
		const seconds = Math.floor((timeDiff % (1000 * 60)) / 1000);

		if(document.getElementById("days")){
			document.getElementById("days").innerHTML = days;
			document.getElementById("hours").innerHTML = hours;
			document.getElementById("minutes").innerHTML = minutes;
			document.getElementById("seconds").innerHTML = seconds;
		}
	}

	updateTimer();
	setInterval(updateTimer, 1000);

	//Shipping and billing methods

	$("#shipping-pobranie").change(function(){
		if(this.checked){
			document.querySelector('#billing-pobranie').disabled = false;
			document.querySelector('#billing-pobranie').checked = true;
			document.querySelector('#billing-przelew').disabled = true;
			document.querySelector('#billing-BLIK').disabled = true;

			let content = this.parentNode.childNodes[3].innerHTML;

			let pos_first = content.indexOf('(')+1;
			let pos_last = content.indexOf('zł');
			
			let price = Number(content.slice(pos_first, pos_last));

			let total_price = document.querySelector('.order-total').innerHTML;
			total_price = total_price.slice(0, total_price.indexOf('zł'));
			total_price = Number(total_price);

			total_price += price;
			price = content.slice(pos_first, pos_last) + "zł";

			pos_first = content.indexOf('K');
			pos_last = content.indexOf(' (');
			
			let shipping_method = content.slice(pos_first, pos_last);

			// Reload shipping_price with current method of shipping
			let shipping_price = document.querySelector("#shipping-price").innerHTML;

			let d_efault = true;

			if(!shipping_price.includes('od'))			
				d_efault = false;

			if (d_efault){
				shipping_price = shipping_price.slice(3, shipping_price.indexOf('zł'));
				shipping_price = Number(shipping_price);
				total_price -= shipping_price;
			}
			else{
				shipping_price = shipping_price.slice(0, shipping_price.indexOf('zł'));
				shipping_price = Number(shipping_price);
				total_price -= shipping_price;
			}

			document.querySelector('.order-total').innerHTML = total_price + 'zł';
			document.querySelector('#input_total_price').value = total_price;
			document.querySelector("#shipping-price").innerHTML = price;
			document.querySelector("#shipping-name").innerHTML = shipping_method;
		}
	})

	$("#shipping-inpost, #shipping-kurier").change(function(){
		let billing_pobranie = document.querySelector('#billing-pobranie');

		if(this.checked){
			document.querySelector('#billing-przelew').disabled = false;
			document.querySelector('#billing-BLIK').disabled = false;
			document.querySelector('#billing-pobranie').disabled = true;

			if(billing_pobranie.checked){
				document.querySelector('#billing-przelew').checked = true;
			}

			let content = this.parentNode.childNodes[3].innerHTML;

			let pos_first = content.indexOf('(')+1;
			let pos_last = content.indexOf('zł');
			
			let price = Number(content.slice(pos_first, pos_last));

			let total_price = document.querySelector('.order-total').innerHTML;
			total_price = total_price.slice(0, total_price.indexOf('zł'));
			total_price = Number(total_price);

			total_price += price;
			price = content.slice(pos_first, pos_last) + "zł";

			if(content.includes('K'))
				pos_first = content.indexOf('K');
			else
				pos_first = content.indexOf('P')

			pos_last = content.indexOf(' (');
			
			let shipping_method = content.slice(pos_first, pos_last);

			// Reload shipping_price with current method of shipping
			let shipping_price = document.querySelector("#shipping-price").innerHTML;

			let d_efault = true;

			if(!shipping_price.includes('od'))			
				d_efault = false;

			if (d_efault){
				shipping_price = shipping_price.slice(3, shipping_price.indexOf('zł'));
				shipping_price = Number(shipping_price);
				total_price -= shipping_price;
			}
			else{
				shipping_price = shipping_price.slice(0, shipping_price.indexOf('zł'));
				shipping_price = Number(shipping_price);
				total_price -= shipping_price;
			}

			document.querySelector('.order-total').innerHTML = total_price + 'zł';
			document.querySelector('#input_total_price').value = total_price;
			document.querySelector("#shipping-price").innerHTML = price;
			document.querySelector("#shipping-name").innerHTML = shipping_method;
		}
	})

	$(".order-submit").click(function(event) {
        let valid = true;

        // Check if a shipping method is selected
        const shippingOptions = document.querySelectorAll('input[name="shipping_method"]');
        const shippingSelected = Array.from(shippingOptions).some(option => option.checked);
        if (!shippingSelected) {
            document.getElementById('order-error').style.display = 'block';
            valid = false;
        } else {
            document.getElementById('order-error').style.display = 'none';
        }

        // Check if a billing method is selected
        const billingOptions = document.querySelectorAll('input[name="billing_method"]');
        const billingSelected = Array.from(billingOptions).some(option => option.checked);
        if (!billingSelected) {
            document.getElementById('order-error').style.display = 'block';
            valid = false;
        } else {
            document.getElementById('order-error').style.display = 'none';
        }

        // Prevent form submission if validation fails
        if (!valid) {
            event.preventDefault();
        }
    });

	
})(jQuery);
