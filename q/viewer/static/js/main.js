$(function(){
	$("input.search_box").keypress(function(e) {
		if (e.which == 13) {
	    	$(this).parent().submit();
  		}
	});
});