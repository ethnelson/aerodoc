


function createChart(ctx, name, data) {
  var param1 = {
    type: 'line',
    data: {
      labels: ['now', '-15s', '-30s', '-45s', '-60s',
              '-75s', '-90s', '-105s', '-120s', '-135s'],
      datasets: [
        {
        label: name,
        fill: false,
        data: data,
        borderColor: ['rgba(49, 52, 67, .8)']
        }
      ]
    },
    options: {
      scales: {
        xAxes: [{
          gridLines: { display: false }
        }],
        yAxes: [{ display: true }]
      }
    }
  };

  var chart = new Chart(document.getElementById(ctx), param1);
  return chart;
}

function updateChart(chart, data) {
  chart.data.datasets[0].data.pop();
  chart.data.datasets[0].data.unshift(data);

  chart.update();
}


var json_data;
var data_length = 10;

var ecChart;
var phChart;
var tempChart;
var humChart;

function reqData() {
  $.get("sensors/data", function(data, status) {
    if (status == 'success') {
      /*change this name 'json_data' to 'data'*/
      json_data = JSON.parse(data);

      ecData = grabItem(json_data, 'EC');
      phData = grabItem(json_data, 'PH');
      tempData = grabItem(json_data, 'temp');
      humData = grabItem(json_data, 'hum');


      ecChart = createChart('ecChart', 'EC', ecData);
      phChart = createChart('phChart', 'PH', phData);
      tempChart = createChart('tempChart', 'Temperature', tempData);
      humChart = createChart('humChart', 'Humidity', humData);
    }
  })
}

function reqDataUpdate() {
  $.get("sensors/dataUpdate", function(data, status) {
    if (status == 'success'){
      var data = JSON.parse(data);
      updateChart(ecChart, data['EC']);
      updateChart(phChart, data['PH']);
      updateChart(tempChart, data['temp']);
      updateChart(humChart, data['hum']);
    }
  });
}

function grabItem(data, filter) {
  var lst = [];
  for (i = 0; i < data_length; i++) {
    lst.push(data[i][filter]);
  }
  return lst;
}


//draw();
