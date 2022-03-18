set_copy_link();
load_user_name();

function set_copy_link() {
    document.getElementById("copy-page").onclick = function() {
        $(document.body).append("<textarea id=\"copyTarget\" style=\"position:absolute; left:-9999px; top:0px;\" readonly=\"readonly\">" + location.href + "</textarea>");
        let obj = document.getElementById("copyTarget");
        let range = document.createRange();
        range.selectNode(obj);
        window.getSelection().addRange(range);
        document.execCommand('copy');
    };
}

function escapeHTML(string) {
    return string.replace(/&/g, '&lt;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, "&#x27;");
}

function load_user_name() {
    $.ajax({
            type: "GET",
            url: "/current_user",
            dataType: "json"
        })
        .done(function(data) {
            var display_name = escapeHTML(data['display_name']);
            target = document.getElementById("user-profile");
            target.innerHTML = "<h1>Logged in as " + display_name;
        })
        .fail(function(XMLHttpRequest, textStatus, errorThrown) {
            alert('fali to read \'current_user\'');
        });
}