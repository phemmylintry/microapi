//line chart 
const ctx_graph = document.getElementById('apigraph').getContext('2d'); 
let chart1 = new Chart(ctx_graph, { 
    // The type of chart we want to create
    type: 'line',

    // The data for our dataset
    data: {
        labels: ['', '', '', '', '', '', '','','','',''],
        datasets: [{
            fill: 'false',
            data: [1, 2, 4, 3, 2, 1, 2, 4, 5, 0.5],
            borderColor: '#00FF29',
            borderWidth: 1,
            pointRadius:0,
            label: ''
        },{
            fill: 'false',
            data: [2, 1, 2, 3, 4, 5, 4, 3, 2, 3],
            borderColor: '#4D7CFE',
            borderWidth: 1,
            pointRadius:1,
            label: '',
        }]
    },
    // Configuration options go here
    options: {
      scales: {
        xAxes: [{
            gridLines: {
                display:false
            }
        }],
        yAxes: [{
            gridLines: {
              drawBorder: false,
              beginAtZero: false,     
            },
            ticks: {
                fontSize: 11,
                fontColor: "black",
                beginAtZero: false,     
                min: 0, // it is for ignoring negative step.
                stepSize: 1
            },
        }]
    },
    title: {
        display: false
    },
    legend: {
        display:false
    }
  }
});


//pie chart 
const ctx_piechart1 = document.getElementById('pie').getContext('2d');
let chart2 = new Chart(ctx_piechart1, { 
    // The type of chart we want to create
    type: 'doughnut',

    data: {
        labels: ["", "","",""],
        datasets: [{
            labels: "Email",
            borderWidth: [0,0,0,10],
            borderColor: 'brown',
            backgroundColor: ['#21D184','#4E4E4E','#0F52FF','brown'],
            data:[5,2,7,4]
        }]
    },
    title: {
        display: false
    },
    options:{
        legend: {
            display: false
         },
    }
});