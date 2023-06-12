$(document).ready(function () {
	$('#getInfoBtn').click(function () {
		$.ajax({
			url: '/test/video/',
			dataType: 'html',
			data: {
				videoURL: $('#video_url')
			},
			success: function (response) {
				$('#videoInfoDiv').html(response);
			},
			error: function () {
				$('#videoInfoDiv').text('Error! Unable to get the video...');
			}
		})
	})
})