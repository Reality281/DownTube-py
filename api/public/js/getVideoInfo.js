$(document).ready(function() {
    console.log($('#video_url').value())
	$('#getInfoBtn').click(function() {
		$.ajax({
			url: '/api/getVideoInfo',
			type: 'GET',
			contentType: 'application/json',
			data: {
				video_url: $('#video_url').value()
			},
			success: function(response) {
				$('#getInfoBtn').text(response.video_id)
			}
		})
	})
})