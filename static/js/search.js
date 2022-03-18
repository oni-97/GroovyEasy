const search_query_input = document.getElementById("search_query_input");
search_query_input.addEventListener('input', () => {
    var input_text = event.currentTarget.value;
    if (event.currentTarget.value == "") {
        target = document.getElementById("search_result");
        target.innerHTML = "";
    } else {
        $.ajax({
                type: "GET",
                url: "/search_track",
                data: {
                    q: input_text
                },
                dataType: 'json'
            })
            .done(function(data) {
                if (data['tracks']['items'].length == 0) {
                    target = document.getElementById("search_result");
                    target.innerHTML = "No results found for \"" + input_text + "\"";
                } else {
                    const target = document.getElementById("search_result");
                    target.innerHTML = "";
                    const ul_element = document.createElement('ul');
                    for (const item of data['tracks']['items']) {
                        const song_name = item['name'];
                        var artists = "";
                        for (const artist of item['album']['artists']) {
                            artists += artist['name'] + ', ';
                        }
                        artists = artists.replace(/,\s$/g, "");
                        const img = item['album']['images'][2]['url'];
                        const uri = item['id'];

                        var li_element = document.createElement('li');
                        li_element.className = "song_info";
                        li_element.onclick = function() {
                            var result = window.confirm("add \"" + song_name + "\" to queue?")
                            if (result) {
                                $.ajax({
                                        type: "GET",
                                        url: "/add_to_queue",
                                        data: {
                                            uri: uri
                                        }
                                    })
                                    .done(function(data) {
                                        alert("added to queue");
                                    })
                                    .fail(function(XMLHttpRequest, textStatus, errorThrown) {
                                        console.log(XMLHttpRequest);
                                        console.log(textStatus);
                                        console.log(errorThrown);
                                        alert('fali to read \'add_to_queue\'');
                                    });
                            }
                        };

                        const div_img = document.createElement('div');
                        div_img.className = 'div_img';
                        const img_element = document.createElement('img');
                        img_element.src = img;
                        div_img.appendChild(img_element);
                        li_element.appendChild(div_img);

                        const div_song = document.createElement('div');
                        div_song.className = 'div_song';

                        const div_song_name = document.createElement('div');
                        div_song_name.className = 'div_song_name';
                        div_song_name.innerHTML = song_name;
                        div_song.appendChild(div_song_name);

                        const div_artists = document.createElement('div');
                        div_artists.className = 'div_artists';
                        div_artists.innerHTML = artists;
                        div_song.appendChild(div_artists);

                        li_element.appendChild(div_song);

                        target.appendChild(li_element);
                    }
                }
            })
            .fail(function(XMLHttpRequest, textStatus, errorThrown) {
                alert('fali to read \'search\'');
            });
    }
});