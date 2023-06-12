$('#getVideoInfoForm').submit(function(e) {
    e.preventDefault();
    var videoUrl = $('#video_url').val();
    $.ajax({
        url: "api/get_video_info/",
        data: {video_url: videoUrl},
        success: function(data) {
            $('#video-info').html(data);
        },
        error: function(xhr, status, error) {
            console.log(error);
        }
    });
});