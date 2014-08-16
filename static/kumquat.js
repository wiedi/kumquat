$(function() {
	$(".confirm-delete").on("click", function(e) {
		var form = $(this);
		e.preventDefault();
		bootbox.confirm("Are you sure?", function(result) {
			if(result) {
				form.submit()
			}
		})
	})
})
