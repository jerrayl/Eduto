/**
 * Created by user on 3/8/2016.
 */
var data = [];
$('table .mainRow').each(function () {
    var subject = $(this).find('.subject').html();
    if (data[subject] != null) {
        data[subject] += 1
    } else {
        data[subject] = 1
    }
});

console.log(data);

// Load the Visualization API and the corechart package.
google.charts.load('current', {'packages': ['corechart']});

// Set a callback to run when the Google Visualization API is loaded.
google.charts.setOnLoadCallback(drawChart);

// Callback that creates and populates a data table,
// instantiates the pie chart, passes in the data and
// draws it.
function drawChart() {

    // Create the data table.
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Subject');
    data.addColumn('number', 'Number');

    var arr = [];
    for(var key in Object.keys(data)) {
        var innerArr = [];
        innerArr.push(key);
        innerArr.push(data[key]);
        arr+=innerArr
    }
    console.log(arr);

    data.addRows([['a',1], ['b', 2]]);

    // Set chart options
    var options = {
        'title': 'How Much Pizza I Ate Last Night',
        'width': 400,
        'height': 300
    };

    // Instantiate and draw our chart, passing in some options.
    var chart = new google.visualization.PieChart(document.getElementById('pie_chart'));
    chart.draw(data, options);
}