$('#slider1, #slider2, #slider3, #slider4').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: true,
            autoplay: true,
        },
        600: {
            items: 2,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 4, 
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

$('.plus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var element = this.parentNode.children[2];
    console.log(id);
    $.ajax({
        type:"GET",
        url:"/pluscart",
        data:{
            prod_id: id
        },
        success: function(data){
            element.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamt").innerText = data.total_amount
        }
    })
})

$('.minus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var element = this.parentNode.children[2];
    console.log(id);
    $.ajax({
        type:"GET",
        url:"/minuscart",
        data:{
            prod_id: id
        },
        success: function(data){
            element.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamt").innerText = data.total_amount
        }
    })
})

$('.remove-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var element = this
    console.log(id);
    $.ajax({
        type:"GET",
        url:"/removecart",
        data:{
            prod_id: id
        },
        success: function(data){
            element.parentNode.parentNode.parentNode.parentNode.remove()
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamt").innerText = data.total_amount
        }
    })
})