var comments_per_page = 50;
var num_pages;
var current_page;

$(function()
{
    current_page = 1;
    num_pages = Number($("#num_pages").html());
	get_comments(current_page);

	$("#right_arrow").click(function() {
		turn_page(1);
	});
	$("#left_arrow").click(function() {
		turn_page(-1);
	});
	$("#current_page").keypress(function(e) {
		if (e.which == 13) {
	    	get_comments($("#current_page").val());
  		}
	});
	$("#seemore").click(function(e){
		e.preventDefault();
		$("#table").toggle();
	});

	$(".content").hide();

	var prereqs_regex = /[^\s]/;
	if (prereqs_regex.exec($("#pre-reqs").html()) == null)
		$("#pre-reqs").html("None");

	var gened_regex = /\.(.*)(General Education requirement for [a-z\s]*)([A-Z][a-zA-Z ]+)( or the Core area requirement for [a-z\s]*)([A-Z][a-zA-Z ]+)(\.\s*)/;
	var notes = $("#notes").html();
	var gened_info = gened_regex.exec(notes);
	

	if (gened_info == null)
	{
		gened_info = [];
		for (var i = 0; i < 6; i++)
			gened_info[i] = "None";
	}

	else
	{
		var first_to_cut_out = notes.indexOf(gened_info[1]);
		var last_to_cut_out = notes.indexOf(gened_info[6]) + gened_info[4].length;
		var first_part = notes.substring(0, first_to_cut_out);
		var last_part = "";
		if (last_to_cut_out < notes.length)
		{
			last_part = notes.substring(last_to_cut_out, notes.length);
		}

		notes = first_part + last_part;
	}

	$("#gened").html("<b>General Education:</b> " + gened_info[3] + "<br/><b>Core:</b> " + gened_info[5]);
	$("#notes").html(notes).show();
	// $("#notes").show();
});

// Get a page of comments.  First page is page 1 (page 0 DNE), last page is page num_pages 
function get_comments(page_n)
{
	if (!is_int(page_n))
	{
		$("#current_page").val(current_page);
		console.log("Not an integer\n");
		return;
	}

	page_n = Number(page_n);

	if (page_n < 1 || page_n > num_pages)
	{
		$("#current_page").val(current_page);
		console.log("Page out of bounds\n");
		return;
	}

	var first_comment = (page_n - 1) * comments_per_page;
	var last_comment = first_comment + comments_per_page - 1;
	var field = $("#field").html();
	var number = $("#number").html();
	var term = $("#term").html();
	var year = $("#year").html();
	var url = "/courses/" + field + "/" + number + "/" + year + "/" + term + "/comments/?first=" + first_comment + "&last=" + last_comment;

	$.ajax({
		dataType: "json",
		url: url,
		success: function(data) {
			if (!data.success)
			{
				$("#current_page").val(current_page);
				return;
			}

			current_page = Number($("#current_page").val());

			var comments = data.comments_to_show;
			$("#comments").empty();

			comments.forEach(function(element, index, array) {

				var term = (element.term == 1) ? "Fall" : "Spring";

				$("#comments").append('<p class="comment raised">' + element.comment + "<i> - " + term + " " 
					                  + element.course_info.year + " (Instructor: " + element.course_info.profs[0] + ")</i>"+ '</p>');
				if (index == 0)
				{
					$("#comments p.comment").addClass("firstcomment");
				}
			});
		}
	});
}

// from user karim79 at http://stackoverflow.com/questions/1019515/javascript-test-for-an-integer#answer-1019526
function is_int(str)
{
	var intRegex = /^\d+$/;

	if (intRegex.test(str))
		return true;
	else
		return false;

}

function turn_page(delta)
{
	console.log("delta: " + delta + " num_pages: " + num_pages);
	page_n = current_page + delta;
	if (page_n > 0 && page_n <= num_pages)
	{
		$("#current_page").val(page_n);
		get_comments(page_n);
	}
}





