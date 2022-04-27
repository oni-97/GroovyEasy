const params = new URLSearchParams(window.location.search)
const roomid = params.get('roomid')
update();
const timmerId = setInterval(update, 1000);

const resume_btn = document.getElementById('resume-btn');
const pause_btn = document.getElementById('pause-btn');
const skip_next_btn = document.getElementById('skip-next-btn');
const skip_pre_btn = document.getElementById('skip-pre-btn');

pause_btn.addEventListener('click', () => {
    $.ajax({
            type: "GET",
            url: "/pause_playback" + '?' + new URLSearchParams({ roomid: roomid }),
        })
        .done(function(data) {
            update();
        })
        .fail(function(XMLHttpRequest, textStatus, errorThrown) {
            alert('fali to read \'pause_playback\'');
        });
});

resume_btn.addEventListener('click', () => {
    $.ajax({
            type: "GET",
            url: "/start_playback" + '?' + new URLSearchParams({ roomid: roomid }),
        })
        .done(function(data) {
            update();
        })
        .fail(function(XMLHttpRequest, textStatus, errorThrown) {
            alert('fali to read \'start_playback\'');
        });
});

skip_next_btn.addEventListener('click', () => {
    $.ajax({
            type: "GET",
            url: "/next_track" + '?' + new URLSearchParams({ roomid: roomid }),
        })
        .done(function(data) {
            update();
        })
        .fail(function(XMLHttpRequest, textStatus, errorThrown) {
            alert('fali to read \'next_track\'');
        });
});

skip_pre_btn.addEventListener('click', () => {
    $.ajax({
            type: "GET",
            url: "/previous_track" + '?' + new URLSearchParams({ roomid: roomid }),
        })
        .done(function(data) {
            update();
        })
        .fail(function(XMLHttpRequest, textStatus, errorThrown) {
            alert('fali to read \'previous_track\'');
        });
});

function escapeHTML(string) {
    return string.replace(/&/g, '&lt;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, "&#x27;");
}

function update() {
    $.ajax({
            type: "GET",
            url: "/currently_playing" + '?' + new URLSearchParams({ roomid: roomid }),
            // dataType: "json"
        })
        .done(function(data) {
            if (data == "ROOM_ERROR") {
                window.location.href = "/signed_out";
                return;
            }

            if (data == 'No track currently playing.') {
                target = document.getElementById("now-playing-track");
                target.innerHTML = data;
                $('#resume').hide();
                $('#pause').hide();
                $('#skip-next').hide();
                $('#skip-pre').hide();
            } else {
                var song_name = escapeHTML(data['item']['name']);
                var artists_name = escapeHTML(data['item']['artists'][0]['name']);
                var song_image_uri = escapeHTML(data['item']['album']['images'][1]["url"]);
                var is_playing = data['is_playing'];

                target = document.getElementById("song-img");
                target.innerHTML = "<img \" src=\"" +
                    song_image_uri +
                    "\" alt=\"image of album\" />";
                target = document.getElementById("song-name");
                target.innerHTML = "Title :   " + song_name;
                target = document.getElementById("artists-name");
                target.innerHTML = "Artist : " + artists_name;

                if (is_playing) {
                    $('#resume').hide();
                    $('#pause').show();
                } else {
                    $('#resume').show();
                    $('#pause').hide();
                }

                $('#skip-next').show();
                $('#skip-pre').show();
            }
        })
        .fail(function(XMLHttpRequest, textStatus, errorThrown) {
            clearInterval(timmerId);
            alert('failed to read \'current playing track\'');
        });
}