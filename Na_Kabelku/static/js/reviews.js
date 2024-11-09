$(document).ready(function(){
    if(document.getElementById('reviews-counter'))
        page = document.getElementById('reviews-counter').value;
    $('#load-more').click(function(){
        $.ajax({
            url: `load-reviews/${page}/`,
            method: "GET",
            success: function(data) {
                $.each(data.reviews_list, function(index, review) {
                    var stars = '';
                    for (var i = 0; i < 5; i++) {
                        if (i < review.rating) {
                            stars += '<i class="fa fa-star"></i>';
                        } else {
                            stars += '<i class="fa fa-star-o empty"></i>';
                        }
                    }

                    $('#reviews-list').append(
                        `<li>
                            <div class="review-heading">
                                <h5 class="name">${review.username}</h5>
                                <p class="date">${review.created_at}</p>
                                <div class="review-rating">
                                    ${stars}
                                </div>
                            </div>
                            <div class="review-body">
                                <p>${review.comment}</p>
                            </div>
                        </li>`
                    );
                });
                if (!data.has_next) {
                    document.getElementById('load-more').style.display='none';
                }
                page++;
            },
            error: function(xhr, status, error) {
                document.getElementById('load-more').style.display='none';
            }
        });
    });

    $('#review-add-form').submit(function(e) {
        e.preventDefault();
        if(confirm("Czy na pewno chcesz dodać opinię?")){
            product = document.getElementById("id_product").value;
            $.ajax({
                url: `/products/product/reviews/add-review/${product}`,
                method: "POST",
                data: $(this).serialize(),
                success: function(data) {
                    review = data;
                    var stars = '';
                    for (var i = 0; i < 5; i++) {
                        if (i < review.rating) {
                            stars += '<i class="fa fa-star"></i>';
                        } else {
                            stars += '<i class="fa fa-star-o empty"></i>';
                        }
                    }
    
                    if (data.success) {
                        $('#reviews-list').prepend(
                            `<li>
                                <div class="review-heading">
                                    <h5 class="name">${review.username}</h5>
                                    <p class="date">${review.created_at}</p>
                                    <div class="review-rating">
                                        ${stars}
                                    </div>
                                </div>
                                <div class="review-body">
                                    <p>${review.comment}</p>
                                </div>
                            </li>`
                        );
                        $('#review-add-form')[0].reset();
                        $('#review-invalid-feedback > .invalid-feedback').remove();
                        var successHtml = '<div class="invalid-feedback" style="color:green;">Dziękujemy za dodanie opinii.</div>';
                        $('#review-invalid-feedback').append(successHtml);
                        
                        let len = location.href.split('/').length;
                        let productSlug = location.href.split('/')[len-2];

                        let reloadPage = $.ajax({
                            url: `/products/product/${productSlug}/`,
                            method: "GET",
                            success: function(data) {
                                let tempDiv = document.createElement('div');
                                tempDiv.innerHTML = data; 
                                document.getElementById("rating").innerHTML = tempDiv.querySelector("#rating").innerHTML;
                                document.getElementById("reviews-count-header").innerHTML = tempDiv.querySelector("#reviews-count-header").innerHTML;
                            }
                        });
                    }
                },
                error: function(xhr) {
                    if (xhr.status === 400) { 
                        var errors = xhr.responseJSON.errors;
                    
                        $('#review-invalid-feedback > .invalid-feedback').remove();
                        for (var field in errors) {
                            if (errors.hasOwnProperty(field)) {
                                var errorMessages = errors[field];
                                var errorHtml = '<div class="invalid-feedback ">' + errorMessages.join('<br>') + '<br></div>';
    
                                $('#review-invalid-feedback').append(errorHtml);
                            }
                        }
                    }
                }
            });
        }
        else{
        }
    });
});

if(document.querySelector("#review-link")){
    document.querySelector("#review-link").onclick = () => {
        document.getElementById("tab3-link").click();
    }
}