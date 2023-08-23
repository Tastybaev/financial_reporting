function loadJson(selector, dump_type) {
  return JSON.parse(document.querySelector(selector).getAttribute(dump_type));
}

window.onload = function() {
  var jsonData = loadJson('#jsonData', 'data-json');

  var data = jsonData.map((item) => item.value);
  var labels = jsonData.map((item) => item.date);
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
    link.setAttribute("href", "/transactions/income/");
  }
  else if (window.location.href.indexOf('income') > -1)
  {
    button.innerHTML = 'Входящие';
    link.setAttribute("href", "/transactions/outgoing/");
  }
  else
  {
    chart.style.display = 'none';
  }
};

function getDateRangeUrl(start, end) {
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
  period = "/transactions/" + type  + "/" + start.format('DD.MM.YYYY') + "/" + end.format('DD.MM.YYYY');
  $('#url_daterange').attr('href', period);
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
  }, function(start, end) {
      getDateRangeUrl(start, end)
  });
});

$(document).ready(function() {
  $('#type_select').change(function() {
    var types = ['null', 'income', 'outgoing']
    var type = $(this).val();
    var link = $('#url_daterange').attr("href");
    if (type == 'Входящие'){
      type = 'income';
    }
    else if (type == 'Исходящие'){
      type = 'outgoing';
    }
    else {
      type = null
    }
    for (var i = 0; i<types.length; i++){
      var substr = types[i];
      if (link.includes(substr)){
        var link = link.replace(substr, type);
      }
    }
    $('#url_daterange').attr('href', link);
  });
});

function deleteTransaction(transaction_id) {
  const csrf = getCookie('csrftoken')
  fetch(
    `/transaction/delete/${transaction_id}/`,
    {
      method:'POST',
      headers:{'X-CSRFToken': csrf,},
    }
  )
  .then(response => response.json())
    .then(data => {
      // Обработка ответа от сервера
      openNotification(data.message)
      if (data.success) {
        // Удаление транзакции из DOM
        const transactionElement = document.querySelector(`#transaction-${transaction_id}`);
        console.log(transactionElement)
        if (transactionElement) {
          transactionElement.remove();
        }
      }
    })
    .catch(error => {
      console.error('Произошла ошибка при удалении транзакции:', error);
    });
}

function deleteCategory(category_id) {
  const csrf = getCookie('csrftoken')
  fetch(
    `/auth/settings/delete_category/${category_id}/`,
    {
      method:'POST',
      headers:{'X-CSRFToken': csrf,},
    }
  )
  .then(response => response.json())
    .then(data => {
      // Обработка ответа от сервера
      openNotification(data.message)
      if (data.success) {
        // Удаление транзакции из DOM
        const categoryElement = document.querySelector(`#category-${category_id}`);
        console.log(categoryElement)
        if (categoryElement) {
          categoryElement.remove();
        }
        // location.reload();
      }
    })
    .catch(error => {
      console.error('Произошла ошибка при удалении транзакции:', error);
    });
}

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

function openNotification(message) {
  $('#modal-message').text(message);
  $('#notificationModal').modal('show');
}

$('#notificationClose').click(function(){
  $('#notificationModal').modal('hide');
})