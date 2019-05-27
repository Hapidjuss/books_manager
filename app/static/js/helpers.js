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

    for (x = 2; x < tr.length; x++) {
        if (tr[x].className.match(/(?:^|\s)active_row(?!\S)/)) {
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
}

function clearFilter(node) {
    var input;
    input = node.parentNode.childNodes[1];
    input.value = "";
    input.focus();
    filterTable();
}

function doShortText() {
    var table, tr, td, text;
    var length = 100;
    table = document.getElementsByTagName("table")[0];
    tr = table.getElementsByClassName("short_text_row");

    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[3];
        text = td.innerHTML;
        if (text.length > length) {             // text shortening
            td.innerHTML = text.substring(0, length) + "...";
        }
    }
}

function showHideFullText(node) {
    var node_index, other_node;
    node_index = Array.prototype.indexOf.call(node.parentNode.children, node);

    if (node.className.match(/(?:^|\s)short_text_row(?!\S)/)) {     // short text row
        other_node = node.parentNode.children[node_index + 1];
        node.className = "nonactive_row short_text_row";

        other_node.className = "active_row full_text_row";
    }
    else {                                                          //full text row
        other_node = node.parentNode.children[node_index - 1];
        node.className = "nonactive_row full_text_row";

        other_node.className = "active_row short_text_row";
    }
    filterTable();
}