
$(document).ready(function () {
    
    // event listener for the search button
    $("#search-button").click(function () {
        $("#search-results-container").empty();
        var query = $("#search-bar").val()
        var encodedQuery = encodeURI(query);
        $.get("playlist/" + encodedQuery, function (data, status) {
            displaySearchResults(data['playlists']['items']);
        });
    });

    $("#add-button").click(function () { // process playlist button
        var list = [];
        $("div[clicked='true']").val(function () {
            list.push($(this).attr('uri'));
        });
        var playlistUri = list[0];
        // IMPLEMENT LOADING BAR OR WHATEVER HERE
        $.get( "process/playlist/" + playlistUri, function( results ) {
            // CANCEL LOADING BAR HERE BECAUSE IM ABOUT TO DISPLAY ALL THE RESULTS
            console.log(results);
        });
    });
});

displaySearchResults = function (searchResults) {
    for (var i = 0; i < searchResults.length; i++) {
        var trackName = searchResults[i]['name']; // actually playlist name
        var artistName = searchResults[i]['owner']['display_name']; // actually playlist owner
        var uri = searchResults[i]['uri']; // actually playlist id
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
