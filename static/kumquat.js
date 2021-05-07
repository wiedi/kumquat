$(function() {
	$(".confirm-delete").on("click", function(e) {
		var form = $(this);
		e.preventDefault();
		bootbox.confirm({
			title: form.attr('data-name') + " " + form.attr('data-value'),
			message: "Are you sure?",
			buttons: {
				confirm: { label: 'Confirm', className: 'btn-success' },
			},
			callback: function (result) {
				if(result) {
					form.submit()
				}
			}
		})
	})
	setTimeout(function() {
		$(".alert").alert('close')
	}, 1000 * 10)
	$('.show-hide-password').on('click', function() {
		$(this).toggleClass('glyphicon-eye-close').toggleClass('glyphicon-eye-open');
		if ($(this).hasClass('glyphicon-eye-open')) {
			$('.form-password :input').attr('type', 'text');
		} else {
			$('.form-password :input').attr('type', 'password');
		}
	});
	$('.generate-password').on('click', function(e) {
		e.preventDefault();
		$('.form-password input').val(generatePassword((Math.floor(Math.random() * (20 - 15)) + 15), false));
		if ($('.show-hide-password').hasClass('glyphicon-eye-close')) {
			$('.show-hide-password').toggleClass('glyphicon-eye-close').toggleClass('glyphicon-eye-open');
			$('.form-password :input').attr('type', 'text');
		}
	});
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
	$('.nav-sidebar a[href="' + path + '"]').closest('li').addClass('active');
})
