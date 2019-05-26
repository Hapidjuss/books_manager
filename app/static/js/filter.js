function filterTable() {
    var authorInput, categoryInput;
    var authorFilter, categoryFilter;
    var table, tr, td, x;

    authorInput = document.getElementById("AuthorFilter");
    categoryInput = document.getElementById("CategoryFilter");

    authorFilter = authorInput.value.toUpperCase();
    categoryFilter = categoryInput.value.toUpperCase();

    table = document.getElementsByTagName("table")[0];
    tr = table.getElementsByTagName("tr");

    for (x = 0; x < tr.length; x++) {
        if (x < 2) continue;                                // without thead and filter rows
        a_td = tr[x].getElementsByTagName("td")[1];
        c_td = tr[x].getElementsByTagName("td")[2];
        if (a_td && c_td) {                                 // check if both filters apply to row
            if ((a_td.innerHTML.toUpperCase().indexOf(authorFilter) > -1) &&
                (c_td.innerHTML.toUpperCase().indexOf(categoryFilter) > -1)) {
                tr[x].style.display = "";
            }
            else {
                tr[x].style.display = "none";
            }
        }
    }
}

function clearFilter(node) {
    var input;
    input = node.parentNode.childNodes[1];
    input.value = "";
    input.focus();
    filterTable();
}
