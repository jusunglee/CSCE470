$(document).ready(function () {
    $("#loading").hide();
    // event listener for the search button
    $("#search-button").click(function () {
        document.getElementById("loading-spinner").src = "http://127.0.0.1:5000/static/img/spinner" + Math.floor(Math.random() * 10) + ".gif";
        $("#add-button").removeAttr('disabled');
        $("#search-results-container").empty();
        var query = $("#search-bar").val()
        var encodedQuery = encodeURI(query);
        $.get("track/" + encodedQuery, function (data, status) {
            displaySearchResults(data);
        });
    });

    $("#add-button").click(function () { // process playlist button
        var list = [];
        
        $("div[clicked='true']").val(function () {
            list.push($(this).attr('uri'));
        });
        var trackUri = list[0];
        // IMPLEMENT LOADING BAR OR WHATEVER HERE
        $("#loading").show();
        $("#search-results-container").hide();
        $.get( "process/track/" + trackUri, function( results ) {
            // CANCEL LOADING BAR HERE BECAUSE IM ABOUT TO DISPLAY ALL THE RESULTS
            $("#loading").hide();
            console.log(results);
            $("#add-button").attr('disabled', 'disabled');
            $("#search-results-container").empty();
            for (var i = 0; i < results.length; i++) {
                var list = JSON.parse(results[i]);
                var playlistTitle = list[1];
                var ownerName = list[3];
                var album_url = list[5];
                var tracks = list[6];
                var ppd = document.createElement("div");
                ppd.className = "panel panel-default";
                var ph = document.createElement("div");
                ph.className = "panel-heading";
                var pt = document.createElement("h4");
                var a = document.createElement("a");
                a.setAttribute("data-toggle", "collapse");
                a.href = "#collapse" + i;
                var titleText = document.createTextNode(playlistTitle);
                var title = document.createElement("b");
                title.appendChild(titleText);
                var owner = document.createTextNode(ownerName);
                var br = document.createElement("br");
                a.appendChild(title);
                pt.appendChild(a);
                var img = document.createElement("img");
                img.className = "spotify-img";
                img.setAttribute("src", "http://marilynscott.com/wp-content/uploads/2016/03/spotify-icon-22.png");
                var imgLink = document.createElement("a");
                imgLink.setAttribute("target", "_blank");
                imgLink.href = album_url;
                imgLink.appendChild(img);
                pt.appendChild(imgLink);
                pt.appendChild(br);
                pt.appendChild(owner);
                ph.appendChild(pt);
                ppd.appendChild(ph);
                var cd = document.createElement("div");
                cd.id = "collapse" + i;
                cd.className = "panel-collapse collapse";
                var ul = document.createElement("ul");
                ul.className = "list-group";
                NUM_TRACKS = 20;
                for(var j = 0; (j < NUM_TRACKS) && (j < tracks.length); j++) {
                    var trackName = tracks[j][0];
                    var artistName = tracks[j][1];
                    var trackUrl = tracks[j][2];
                    var li = document.createElement("li");
                    li.className = "list-group-item";
                    var nameNode = document.createElement("b");
                    var nameTextNode = document.createTextNode(trackName);
                    var urlNode = document.createElement("a");
                    urlNode.appendChild(nameTextNode);
                    urlNode.href = trackUrl;
                    urlNode.setAttribute("target", "_blank");
                    nameNode.appendChild(urlNode);
                    var artistNode = document.createTextNode(artistName);
                    var br2 = document.createElement("br");
                    li.appendChild(nameNode);
                    li.appendChild(br2);
                    li.appendChild(artistNode);
                    ul.appendChild(li);
                }
                cd.appendChild(ul);
                ppd.appendChild(cd);
                document.getElementById("search-results-container").appendChild(ppd);
            }
            $("#search-results-container").show();
        });
    });
});

displaySearchResults = function (searchResults) {
    for (var i = 0; i < searchResults.length; i++) {
        var track = searchResults[i];
        var trackName = track['song_name'];
        var artistName = track['artist_name'];
        var uri = track['song_uri'];
        var $resultItemDiv = $("<div>", { id: "search-result-" + i, "class": "search-result-item", "clicked": "false", "uri": uri });
        var $trackNameItem = $("<p>", { "class": "track-name" });
        $trackNameItem.append(trackName);
        var $artistNameItem = $("<p>", { "class": "artist-name" });
        $artistNameItem.append(artistName);
        $resultItemDiv.append($trackNameItem);
        $resultItemDiv.append($artistNameItem);

        // onclick listener to highlight the individual search result item
        $resultItemDiv.click(function () {
            var $clickedItem = $(this);
            $clickedItem.toggleClass("search-result-item-highlighted");
            $clickedItem.toggleClass("search-result-item");
            var numSelectedTracks = parseInt($("#search-results-container").attr("num-selected-tracks"));
            if ($clickedItem.attr("clicked") == "false") {
                $clickedItem.attr("clicked", "true");
                $("#search-results-container").attr("num-selected-tracks", numSelectedTracks + 1);
                numSelectedTracks += 1;
            }
            else {
                $clickedItem.attr("clicked", "false");
                $("#search-results-container").attr("num-selected-tracks", numSelectedTracks - 1);
                numSelectedTracks -= 1;
            }

            if (numSelectedTracks > 0) {
                $("#add-button").removeAttr('disabled');
            }
            else {
                $("#add-button").attr('disabled', 'disabled');
            }
        });

        $("#search-results-container").append($resultItemDiv);
    }
}
