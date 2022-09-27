// When the search button is clicked, show the search dialog
function showSearchForm(){
    var searchForm = document.getElementById("searchForm");
    searchForm.style.display = "block";
    searchForm.style.visibility = "visible";
}

// Hide the search dialog
function hideSearch(){
    var searchForm = document.getElementById("searchForm");
    searchForm.style.display = "none";
    searchForm.style.visibility = "hidden";
}