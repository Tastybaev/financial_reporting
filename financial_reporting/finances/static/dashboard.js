function loadJson(selector, dump_type) {
  return JSON.parse(document.querySelector(selector).getAttribute(dump_type));
}

window.onload = function() {
  var jsonData = loadJson('#jsonData', 'data-json');

  var data = jsonData.map((item) => item.value);
  var labels = jsonData.map((item) => item.date);
  console.log(jsonData)
  var dataSecond = [{
      label: "Исходящие",
      data: data,
      lineTension: 0,
      fill: false,
      borderColor: 'blue'
    }];

  var speedData = {
    labels: labels,
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
  var ctx = document.getElementById('myChart').getContext('2d');
  window.myLine = new Chart(ctx, lineChart);
  var button = document.getElementById('chart-togle-button');
  var chart = document.getElementById('myChart');
  var link = document.getElementById('togle_transaction');
  if (window.location.href.indexOf('outgoing') > -1)
  {
    button.innerHTML = 'Исходящие';
    link.setAttribute("href", "income");
  }
  else if (window.location.href.indexOf('income') > -1)
  {
    button.innerHTML = 'Входящие';
    link.setAttribute("href", "outgoing");
  }
  else
  {
    chart.style.display = 'none';
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
    if (type == 'Входящие'){
      type = 'income';
    }
    else if (type == 'Исходящие'){
      type = 'outgoing';
    }
    else {
      type = null
    }
    period = type  + "/" + start.format('DD.MM.YYYY') + "/" + end.format('DD.MM.YYYY');
    $('#url_daterange').attr('href', period);
  });
});
// Еадо поравить тип транзакции в юрл и сделать, вьюху. Решить проблему с выпадающем списком.