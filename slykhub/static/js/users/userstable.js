$(document).ready(function (){
    var table = $('#usertable').DataTable();
function tableToCSV() {  
    // Variable to store the final csv data
    var csv_data = [];

    // Get each row data
    var rows = document.getElementsByTagName('tr');
    for (var i = 0; i < rows.length; i++) {

        // Get each column data
        var cols = rows[i].querySelectorAll('td,th');

        // Stores each csv row data
        var csvrow = [];
        for (var j = 0; j < cols.length; j++) {

            // Get the text data of each cell
            // of a row and push it to csvrow
            csvrow.push(cols[j].innerHTML);
        }
        console.log(csvrow);

        // Combine each column value with comma
        csv_data.push(csvrow.join(","));
    }

    // Combine each row data with new line character
    csv_data = csv_data.join('\n');

    // Call this function to download csv file
    downloadCSVFile(csv_data);

}

function downloadCSVFile(csv_data) {

    // Create CSV file object and feed
    // our csv_data into it
    CSVFile = new Blob([csv_data], {
        type: "text/csv"
    });

    // Create to temporary link to initiate
    // download process
    var temp_link = document.createElement('a');

    // Download csv file
    var date = new Date();
	var current_date = date.getFullYear()+"_"+(date.getMonth()+1)+"_"+ date.getDate() +"_"+ date.getHours() + date.getMinutes() + date.getSeconds();
    temp_link.download = "Slykhub_users_" + current_date +".csv";
    var url = window.URL.createObjectURL(CSVFile);
    temp_link.href = url;

    // This link should not be displayed
    temp_link.style.display = "none";
    document.body.appendChild(temp_link);

    // Automatically click the link to
    // trigger download
    temp_link.click();
    document.body.removeChild(temp_link);
}


$('#usertable tbody').on('click', '.clickable-row', function() {
    var row = $(this).closest('tr');
    window.location = $(row).data("href");
});

$('#btnExport').click(tableToCSV);
});