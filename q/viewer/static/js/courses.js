var comments_per_page = 10;
var hidden = true;

function pageturn(page)
{
	console.log(page);
	var first_comment = comments_per_page * (page - 1) + 1;
	var i;

	// If first_comment not found, page out of range
	if (!$("#comment" + first_comment).html())
		return;

	// reduce margin-top
	$("#comment" + first_comment).addClass("firstcomment");

	// hide comments before
	for(i = 1; i < first_comment; i++)
	{
		$("#comment" + i).hide();
	}

	// show comments on page
	for(i = first_comment; i < first_comment + comments_per_page && $("#comment" + i).html(); i++)
	{
		$("#comment" + i).show();
	}

	// hide comments after
	for(i = first_comment + comments_per_page; $("#comment" + i).html(); i++)
	{
		$("#comment" + i).hide();
	}

	$(".pagination ul li").removeClass("active");
	$("#page" + page).addClass("active");
}

$(function()
{
	// number each comment
	var count = 1;
	$("#comments p.comment").each(function(){
		this.id = "comment" + count;
		count ++;
	});
	
	// add page numbers to the bottom of the page
	for(var page = 1; $("#comment" + (comments_per_page * (page - 1) + 1)).html(); page ++)
	{
		// id = "page<number>"
		var elt = "<li id=\"page" + page + "\"><a href=\"#comments\">" + page + "</a></li>"
		$(".pagination ul").append(elt);
		$("#page" + page + " a").click(function(e){
			e.preventDefault();
			// http://stackoverflow.com/questions/448666/parsing-an-int-from-a-string-in-javascript
			// find the page number clicked 
			var p = $(this).parent().attr("id").match(/\d+/);
			pageturn(p);
		});
	}
	// start with page 1
	pageturn(1);
	// hide or show the table
	$("#seemore").click(function(e){
		e.preventDefault();
		if(hidden)
		{
			$("#table").show();
			hidden = false;
			$("#seemore a").html("Hide previous years");
		}

		else
		{
			$("#table").hide();
			hidden = true;
			$("#seemore a").html("See previous years");
		}
	});
}
)