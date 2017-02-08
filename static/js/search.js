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

$(function() {

  $('input[name="datefilter"]').daterangepicker({
      autoUpdateInput: false,
      locale: {
          cancelLabel: 'Clear'
      }
  });

  $('input[name="datefilter"]').on('apply.daterangepicker', function(ev, picker) {
      $(this).val(picker.startDate.format('MM/DD/YYYY') + ' - ' + picker.endDate.format('MM/DD/YYYY'));
  });

  $('input[name="datefilter"]').on('cancel.daterangepicker', function(ev, picker) {
      $(this).val('');
  });

});