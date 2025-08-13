document.addEventListener("DOMContentLoaded", function() {
    const searchInput = document.getElementById("search-input");
    searchInput.addEventListener("input", function() {
        if (searchInput.value.length > 2) {
            searchInput.style.borderColor = "#0077aa";
        } else {
            searchInput.style.borderColor = "#ccc";   
        }    
    });
});