$(function()
{
    $("#dfilter").keyup(function() {
        var filter = $(this).val().toUpperCase();
        $("#dfilter li").hide();
        $("#departments li a").each(function(){

            if($(this).html().toUpperCase().indexOf(filter) >= 0)
                $(this).parent().slideDown();

            else
                $(this).parent().slideUp();
        });
    });
})