$(function() {
	function refreshEmails() {
		$('.results').html('');
		$.get('/data/' + $('.options li.active').attr("name") + "-" + $('.year select').val(), function(data) {
			$.each(JSON.parse(data), function(i, email) {
				$('.results').append('<li>' + email.subject + '</li>');
			});
		});
	}

	$('ul.options li').click(function() {
		$('.active').removeClass('active');
		$(this).addClass('active');
		refreshEmails();
	});
});