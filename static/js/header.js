if (new URLSearchParams(window.location.search).has('roomid')) {
    const params = new URLSearchParams(window.location.search)
    const home_link = document.getElementById('home_link');
    const now_playing_link = document.getElementById('now_playing_link');
    const search_link = document.getElementById('search_link');
    const roomid = params.get('roomid')
    home_link.setAttribute('href', '/home' + '?' + new URLSearchParams({ roomid: roomid }))
    now_playing_link.setAttribute('href', '/now_playing' + '?' + new URLSearchParams({ roomid: roomid }))
    search_link.setAttribute('href', '/search' + '?' + new URLSearchParams({ roomid: roomid }))
}