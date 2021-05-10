
/* ------------------------------ CHARTS -------------------------------------*/
var ecChart;
var phChart;
var tempChart;
var humChart;

/* -------------------------- CHART FUNCTIONS --------------------------------*/
function createChart(ctx, name, time, data) {
  var param = {
    type: 'line',
    data: {
      labels: [...time],
      datasets: [
        {
        label: name,
        fill: false,
        data: [...data],
        borderColor: ['rgba(49, 52, 67, .8)']
        }
      ]
    },
    options: {
      scales: {
        xAxes: [{
          stacked: false,
          ticks: {
            autoSkip: true,
            maxTicksLimit: 10
          },
          gridLines: { display: false }
        }],
        yAxes: [{
          stacked: false,
            ticks: {
              suggestedMin: 0,
              suggestMax: 100,
              stepSize: 1
            },
          display: true
        }]
      }
    }
  };

  /* Specific configuratins per chart */
  switch (ctx) {
    case 'ecChart':
      param.options.scales.yAxes[0].ticks.suggestedMin = .5;
      param.options.scales.yAxes[0].ticks.suggestedMax = 2.5;
      param.options.scales.yAxes[0].ticks.stepSize = 0.5;
      break;
    case 'phChart':
      param.options.scales.yAxes[0].ticks.suggestedMin = 4;
      param.options.scales.yAxes[0].ticks.suggestedMax = 11;
      param.options.scales.yAxes[0].ticks.stepSize = 1
      break;
    case 'tempChart':
      param.options.scales.yAxes[0].ticks.suggestedMin = 15;
      param.options.scales.yAxes[0].ticks.suggestedMax = 35;
      param.options.scales.yAxes[0].ticks.stepSize = 5
      break;
    case 'humChart':
      param.options.scales.yAxes[0].ticks.suggestedMin = 20;
      param.options.scales.yAxes[0].ticks.suggestedMax = 80;
      param.options.scales.yAxes[0].ticks.stepSize = 20;
      break;
    default:
      break;
  }

  var myChart = new Chart(document.getElementById(ctx).getContext('2d'), param);
  return myChart;
}

/* Updates
function updateChart(passedChart, data) {
  for (i = 0; i < data.length; i++) {
    passedChart.data.labels.pop();
    if (passedChart.data.datasets[0].data.length >= chart_range){
      passedChart.data.datasets[0].data.pop()
    }
  }
  for (i = data.length-1; i >= 0; i--) {
    passedChart.data.labels.unshift(time[i]);
    passedChart.data.datasets[0].data.unshift(data[i]);
  }
  passedChart.update();
}
/* Updates control display ( light, fan )                                     */
function updateControls(data) {
  items = {
            'light': data['light'],
            'fan': data['fan']
          };
  for (element in items) {
    if (items[element]){
      $('#'+element).text('ON');
    } else {
      $('#'+element).text('OFF');
    }
  }
}


/* ------------------------------ CREATE CHARTS ------------------------------*/
/* Request sensor and system information to display
    & create charts for dislaying sensor data                                 */
function reqData() {
  $.get("sensors/data", function(data, status) {
    if (status == 'success') {
      json_data = JSON.parse(data);

      ecData = grabItem(json_data, 'EC');
      phData = grabItem(json_data, 'PH');
      tempData = grabItem(json_data, 'temp');
      humData = grabItem(json_data, 'hum');

      datetime = grabItem(json_data, 'time');
      time = [];
      /* separate datetime into simply time */
      for (i = 0; i < Object.keys(json_data).length; i++){
        time.push(datetime[i].split(" ")[1]);
      }
      /* Adjust time range label based on config */
      if (time.length < chart_range) {
        for (i = 0; i < (chart_range - time.length); i++) {
          time.push(null);
        }
      }
      /* create charts */
      ecChart = createChart('ecChart', 'EC', time, ecData);
      phChart = createChart('phChart', 'PH', time, phData);
      tempChart = createChart('tempChart', 'Temperature', time, tempData);
      humChart = createChart('humChart', 'Humidity', time, humData);

      updateControls(json_data[0]);
    }
  })
}

/* ------------------------------ UPDATE CHARTS ----------------------------- */
function reqDataUpdate() {
  $.get("sensors/dataUpdate", function(data, status) {
    if (status == 'success'){
      if (data) {
        var json_data = JSON.parse(data);
        ecData = grabItem(json_data, 'EC');
        phData = grabItem(json_data, 'PH');
        tempData = grabItem(json_data, 'temp');
        humData = grabItem(json_data, 'hum');
        datetime = grabItem(json_data, 'time');
        time = [];
        for (i = 0; i < Object.keys(json_data).length; i++){
          time.push(datetime[i].split(" ")[1]);
        }

        updateChart(ecChart, ecData);
        updateChart(phChart, phData);
        updateChart(tempChart, tempData);
        updateChart(humChart, humData);

        updateControls(json_data[0]);
      }
    }
  });
}
/* --------------------------- HELPER FUNCTIONS ----------------------------- */
/* Splits the chart information gathered from the server into separate lists
    based on the filter ( 'EC', 'PH', 'temp', etc )                           */
function grabItem(data, filter) {
  var lst = [];
  for (i = 0; i < Object.keys(data).length; i++) {
    lst.push(data[i][filter]);
  }
  return lst;
}
