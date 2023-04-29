$(".cart-remove").each(function() {
    $(this).on("click", function() {
        $.ajax({
            type: "GET",
            url: "/rmvCart",
            data: {productid: $(this).parent().parent().attr("product")},
            success: function(respone) {
                $("#notice-message").append(
                    '<div style="width: 200px; cursor: pointer" onclick="this.remove()">'+respone+'</div>'
                )
            }
        });
        $(this).parent().parent().remove()
    });
});