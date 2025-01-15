$(document).ready(function() {
    // Quantity input changes event
    $('.cart-details input').change(function() {
        let quantity = this.value;
        let id = this.id.substring(14);

        $.ajax({
            url: `item/update/${id}/${quantity}/`,
            method: "GET",
            success: function(data) {
                // Update total_price of product
                document.querySelector(`#cart-item-${id} .product-price`).innerHTML = data.price + "zł";

                let item = document.querySelector(`#order-item-${id}`).childNodes[1];
                let endQuantityIndex = item.innerHTML.indexOf('x');
                let itemName = item.innerHTML.slice(endQuantityIndex);
                let itemPrice = document.querySelector(`#order-item-${id}`).childNodes[3];
                itemPrice.innerHTML = data.price + "zł";
                document.querySelector(`.order-total`).innerHTML = data.cart_price + "zł"; 
                console.log(data.cart_price)
                //TODO
                // if (quantity != 0)
                item.innerHTML = quantity + itemName;
                // else
                //     document.querySelector(`#order-item-${id}`).remove();
            },
            error: function(xhr, status, error) {
                console.error("Error update item:", error);
            }
        });
    });


    // Quantity buttons event
    $('.cart-details span').click(function() {
        let quantity = this.parentElement.children[1].value;
        let id = this.parentElement.children[1].id.substring(14);

        $.ajax({
            url: `item/update/${id}/${quantity}/`,
            method: "GET",
            success: function(data) {
                // Update total_price of product
                document.querySelector(`#cart-item-${id} .product-price`).innerHTML = data.price + "zł";

                let item = document.querySelector(`#order-item-${id}`).childNodes[1];
                let endQuantityIndex = item.innerHTML.indexOf('x');
                let itemName = item.innerHTML.slice(endQuantityIndex);
                let itemPrice = document.querySelector(`#order-item-${id}`).childNodes[3];
                itemPrice.innerHTML = data.price + "zł";
                document.querySelector(`.order-total`).innerHTML = data.cart_price + "zł"; 
                //TODO
                // if (quantity != 0)
                item.innerHTML = quantity + itemName;
                // else
                //     document.querySelector(`#order-item-${id}`).remove();
            },
            error: function(xhr, status, error) {
                console.error("Error update item:", error);
            }
        });
    });
});
