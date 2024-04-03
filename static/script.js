document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("searchForm").addEventListener("submit", function(event) {
        event.preventDefault(); // Prevent form submission

        var searchTerm = document.getElementById("searchInput").value.toLowerCase();
        switch (searchTerm) {
            case "colombia":    //when "colombia" is searched /colombia will be returned
                window.location.href = "/colombia";
                break;
            case "brazil":      //when "brazil" is searched /brazil is returned
                window.location.href = "/brazil";
                break;
            case "galapagos":       //when "galapagos" is searched, /galapagos is returned
                window.location.href = "/galapagos";
                break;
            case "tips":        //when "tips" is searched, /traveltips is returned
                window.location.href = "/traveltips";
                break;
            case "facts":               //when "facts" is searched, /facts is returned
                window.location.href = "/facts";
                break;
            case "advice":              //when "advice" is searched, /traveltips is returned
                window.location.href = "/traveltips"
                break;

            default:
                // Redirect to a default page or display a message if the search term does not match
                alert("Sorry, no results found for '" + searchTerm + "'.");
                break;
        }
    });
});
