var options = {
           chart: {
               renderTo: 'container',
               type: 'spline'
           },
           xAxis: {},
           series: [{}]
       };

       $.getJSON('data.json', function (data) {
           var categories = [],
               points = [];

            $.each(data, function(i, el) {
                categories.push(el.Time);
                points.push(parseFloat(el.ReadData));
            });
           options.xAxis.categories = categories;
           options.series[0].data = points;
           var chart = new Highcharts.Chart(options);
       });



       $(document).ready(function() {

    var options = {
        chart: {
            renderTo: 'container',
            type: 'spline'
        },
        series: [{}]
    };

    $.getJSON('data.json', function(data) {
        options.series[0].data = data;
        var chart = new Highcharts.Chart(options);
    });

});