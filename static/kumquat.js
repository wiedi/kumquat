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
	setTimeout(function() {
		$(".alert").alert('close')
	}, 1000 * 10)

	if ($("input[name='use_letsencrypt']").is(':checked')) {
		$("select[name='cert']").attr("disabled", true);
	}
	$("input[name='use_letsencrypt']").click(function(){
		if ($(this).is(':checked')) {
			$("select[name='cert']").attr("disabled", true);
		}
		else if ($(this).not(':checked')) {
			$("select[name='cert']").attr("disabled", false);
		}
	});
	/* Django workaround to submit also disabled form fields */
	$('#vhost_form').submit(function(){
		$("select[name='cert']").removeAttr('disabled');
	});
	/* Active menu item will be highlighted */
	var p = location.pathname.split('/');
	var path = '/';
	if( p.length > 2 ) {
		path = '/' + p.slice(1,3).join('/') + '/';
	}
	$('a[href="' + path + '"]').closest('li').addClass('active'); 
})
