/* Convert HTML table data into |-delimited text that can be POSTed 
 * to a server-side view and written virtually as-is to a CSV.
 *
 * Takes table ID string with preceding hash (e.g., "#my_table") as input.
 *
 * BEWARE that this works in conjunction with some server-side 
 * code that only handles ASCII text, so using this on HTML tables
 * that involve non-ASCII characters will not work */

function tableToCSV(tableID) {

    var SEPARATOR = ',';
    var op = ""; /* output string to be built */
    var table = $(tableID);
    var rows = $('tr', table);
    var nl = "%0A"; /* newline character */

    /* get header row */
    var cells = $('th', rows[0]);
    cells.each(function (index2, value2) {
        op = op.concat($(value2).text().trim());
        op = op.concat(SEPARATOR);
    });
    op = op.concat(nl);

    /* deal with non-header rows */
    rows.each(function(i, v) {
        if (!$(rows[i]).hasClass('hidden')) {
            var cells = $('td', v);

            cells.each(function(index2, value2) {
                op = op.concat($(value2).text().trim());
                op = op.concat(SEPARATOR);
            });
            op = op.concat(nl);
        }
    });

    return op;
}
