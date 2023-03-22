
$("#Cate_Selector").on("change", function(){
    id = $("#Cate_Selector").val();
    selCom = $(".selCom");
    if (id > 0) {
        $(selCom.get(0)).removeClass("notshow");

        $.ajax({
            type: "GET",
            url: "getCategory",
            data: { cate_id: id},
            success: function(respone) {
                selCom[1].value = respone;
            }
        })
    }
    else {
        $(selCom.get(0)).addClass("notshow");
    }
})

$("#Product_Selector").on("change", function(){
    id = $("#Product_Selector").val();
    selCom = $(".selCom");
    if (id > 0) {
        $(selCom.get(0)).removeClass("notshow");

        $.ajax({
            type: "GET",
            url: "getProduct",
            data: { product_id: id},
            success: function(respone) {
                $("#select_show").html(respone)
            }
        })
    }
    else {
        $(selCom.get(0)).addClass("notshow");
    }
})