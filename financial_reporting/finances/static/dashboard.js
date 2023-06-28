function loadJson(selector, dump_type) {
  return JSON.parse(document.querySelector(selector).getAttribute(dump_type));
}

window.onload = function() {
  var jsonData_out = loadJson('#jsonData', 'data-json-out');

  var data_outgoing = jsonData_out.map((item) => item.value_outgoing);
  var labels_outgoing = jsonData_out.map((item) => item.date_outgoing);
  console.log(data_outgoing)
  console.log(labels_outgoing)
  console.log(jsonData_out)
  var dataSecond = [{
      label: "Исходящие",
      data: data_outgoing,
      lineTension: 0,
      fill: false,
      borderColor: 'red'
    }];

  var speedData = {
    labels: labels_outgoing,
    datasets: dataSecond
  };

  var chartOptions = {
    legend: {
      display: true,
      position: 'top',
      labels: {
        boxWidth: 80,
        fontColor: 'black'
      }
    }
  };

  var lineChart = {
    type: 'line',
    data: speedData,
    options: chartOptions
  };
  var ctx = document.getElementById('myChartOut').getContext('2d');
  window.myLine = new Chart(ctx, lineChart);
  var jsonData_in = loadJson('#jsonData', 'data-json-in');
  var data_income = jsonData_in.map((item) => item.value_income);
  var labels_income = jsonData_in.map((item) => item.date_income);

  var dataFirst = [{
    label: "Входящие",
    data: data_income,
    lineTension: 0,
    fill: false,
    borderColor: 'green'
  }];

  var speedData = {
    labels: labels_income,
    datasets: dataFirst
  };

  var chartOptions = {
    legend: {
      display: true,
      position: 'top',
      labels: {
        boxWidth: 80,
        fontColor: 'black'
      }
    }
  };
  
  var lineChart = {
    type: 'line',
    data: speedData,
    options: chartOptions
  };
  var ctx = document.getElementById('myChartIn').getContext('2d');
  window.myLine = new Chart(ctx, lineChart);
  var button = document.getElementById('chart-togle-button');
  var chart_in = document.getElementById('myChartIn');
  var chart_out = document.getElementById('myChartOut');
  var link = document.getElementById('togle_transaction');
  if (window.location.href.indexOf('outgoing') > -1)
  {
    chart_in.style.display = 'none';
    chart_out.style.display = 'block';
    button.innerHTML = 'Исходящие';
    link.setAttribute("href", "income");
  }
  else if (window.location.href.indexOf('income') > -1)
  {
    chart_in.style.display = 'block';
    chart_out.style.display = 'none';
    button.innerHTML = 'Входящие';
    link.setAttribute("href", "outgoing");
  }
  else
  {
    chart_in.style.display = 'none';
    chart_out.style.display = 'none';
  }
};

$(function() {
  $('input[name="daterange"]').daterangepicker({
    opens: 'right',
    locale: {
      cancelLabel: 'Очистить',
      format: 'DD.MM.YYYY',
      "separator": " - ",
      "applyLabel": "Применить",
      "cancelLabel": "Очистить",
      "fromLabel": "от",
      "toLabel": "до",
      "customRangeLabel": "Custom",
      "weekLabel": "Н",
      "daysOfWeek": [
          "ВС",
          "ПН",
          "ВТ",
          "СР",
          "ЧТ",
          "ПТ",
          "СБ"
      ],
      "monthNames": [
          "Январь",
          "Февраль",
          "March",
          "April",
          "May",
          "June",
          "July",
          "August",
          "September",
          "October",
          "November",
          "December"
      ],
      "firstDay": 1
    }
  }, function(start, end, label) {
    type = $('#type_select').val();
    period = type  + "/" + start.format('DD.MM.YYYY') + "/" + end.format('DD.MM.YYYY');
    $('#url_daterange').attr('href', period);
  });
});
// Еадо поравить тип транзакции в юрл и сделать, вьюху. Решить проблему с выпадающем списком.