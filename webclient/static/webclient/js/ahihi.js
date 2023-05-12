$(".AddtoWishList2").each(function (index, element) {
    // element == this
    $(element).on("click", function() {
        id = $(this).attr("productid");
        $.ajax({
            type: "GET",
            url: "/AddtoWishList",
            data: { productid: id},
            success: function(respone) {
                $("#notice-message").append(
                    '<div style="width: 200px; cursor: pointer" onclick="this.remove()">'+respone+'</div>'
                )
            }
        });
    })
});

$(".AddtoCart2").each(function (index, element) {
    // element == this
    $(element).on("click", function() {
        id = $(this).attr("productid");
		product_number= $("#product_number").val()
		if (product_number==null) {
				product_number=1;
		}
		
		
        $.ajax({
            type: "GET",
            url: "/AddtoCart",
            data: { productid: id, number:product_number},
			
            success: function(respone) {
                $("#notice-message").append(
                    '<div style="width: 200px; cursor: pointer" onclick="this.remove()">'+respone+'</div>'
                )
            }
        });

        $.ajax({
            type: "GET",
            url: "/preCart",
            data: {},
            success: function(respone) {
                $("body > div > header > nav > div.side > li > ul").html(respone);
            }
        });
    })
});