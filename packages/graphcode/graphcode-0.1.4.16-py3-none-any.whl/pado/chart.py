'''
Copyright (c) 1998-2124 Ryeojin Moon
Copyright (c) 2020-2124 GraphCode

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

THIS SOFTWARE IS NOT PROVIDED TO ANY ENTITY OR ANY GROUP OR ANY PERSON
TO THREATEN, INCITE, PROMOTE, OR ACTIVELY ENCOURAGE VIOLENCE, TERRORISM,
OR OTHER SERIOUS HARM. IF NOT, THIS SOFTWARE WILL NOT BE PERMITTED TO USE.
IF NOT, THE BENEFITS OF ALL USES AND ALL CHANGES OF THIS SOFTWARE ARE GIVEN
TO THE ORIGINAL AUTHORS WHO OWNED THE COPYRIGHT OF THIS SOFTWARE  ORIGINALLY.
THE CONDITIONS CAN ONLY BE CHANGED BY THE ORIGINAL AUTHORS' AGREEMENT
IN AN ADDENDUM, THAT MUST BE DOCUMENTED AND CERTIFIED IN FAIRNESS MANNER.
===
Created by Jan 1, 2011
Modified by Jan 1, 2023

@contributor: hoeseong
'''
#from graphcode.logging import logCritical, logError, logWarn, logInfo, logDebug, logException, logExceptionWithValueError, raiseValueError
from graphcode.logging import logCritical, logError, logWarn, logInfo, logDebug, logException, logExceptionWithValueError, raiseValueError

class GcChart:
  def __init__(self, theme = "default"):
    self.theme = theme
    
    self.chartJsScript = ""
  
  def getJsScript(self):
    return self.chartJsScript
  
  def getChartTags(self, cardName, card_dict):
    try:
      chartId = "{}{}".format(cardName[0].lower(), cardName[1:].replace(" ", ""))
    except:
      logException("unable to set chartId with cardName:[{}]".format(cardName))
      chartId = cardName.lower()
      
    try:
      self.chartJsScript += self.getChartJsScript(chartId= chartId, chartType= card_dict["unit"] , chartLabels= card_dict["labels"] , chartData= card_dict["data"], chartDataUnit= card_dict["data-unit"])
    except:
      logException("unable to get chart tags with {}".format(card_dict))
      
    if card_dict["unit"] == "area":
      chartTags = """
                  <!-- ${{__cardName__}}: ${{__chartType__}} Chart -->
                  <div class="col-xl-8 col-lg-7">
                      <div class="card shadow mb-4">
                          <!-- Card Header - Dropdown -->
                          <div
                              class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
                              <h6 class="m-0 font-weight-bold text-primary">${{__cardName__}}</h6>
                              ${{__dropdownItems__}}
                              </div>
                          </div>
                          <!-- Card Body -->
                          <div class="card-body">
                              <div class="chart-area">
                                  <canvas id="${{__chartId__}}"></canvas>
                              </div>
                          </div>
                      </div>
                  </div>
      """.replace("${{__cardName__}}", cardName).replace("${{__chartId__}}", chartId).replace("${{__chartType__}}", card_dict["unit"]).replace("${{__data__}}", card_dict["data"])
      
    elif card_dict["unit"] == "pie":
      chartTags = """
                  <!--  ${{__cardName__}}: ${{__chartType__}} Chart -->
                  <div class="col-xl-4 col-lg-5">
                      <div class="card shadow mb-4">
                          <!-- Card Header - Dropdown -->
                          <div
                              class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
                              <h6 class="m-0 font-weight-bold text-primary">${{__cardName__}}</h6>
                              ${{__dropdownItems__}}
                              </div>
                          </div>
                          <!-- Card Body -->
                          <div class="card-body">
                              <div class="chart-pie pt-4 pb-2">
                                  <canvas id="${{__chartId__}}"></canvas>
                              </div>
                              <div class="mt-4 text-center small">
                                  <span class="mr-2">
                                      <i class="fas fa-circle text-primary"></i> Direct
                                  </span>
                                  <span class="mr-2">
                                      <i class="fas fa-circle text-success"></i> Social
                                  </span>
                                  <span class="mr-2">
                                      <i class="fas fa-circle text-info"></i> Referral
                                  </span>
                              </div>
                          </div>
                      </div>
                  </div>
      """.replace("${{__cardName__}}", cardName).replace("${{__chartId__}}", chartId).replace("${{__chartType__}}", card_dict["unit"]).replace("${{__data__}}", card_dict["data"])
    else:
      chartTags = """
                    <!-- ${{__cardName__}}: Unsupported Chart: ${{__chartType__}} -->
                    <div class="col-xl-8 col-lg-7">
                        <div class="card shadow mb-4">
                            <!-- Card Header - Dropdown -->
                            <div
                                class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
                                <h6 class="m-0 font-weight-bold text-primary">Earnings Overview</h6>
                                ${{__dropdownItems__}}
                            </div>
                            <!-- Card Body -->
                            <div class="card-body">
                                <div class="chart-area">
                                    <canvas id="myAreaChart"></canvas>
                                </div>
                            </div>
                        </div>
                    </div>
        """.replace("${{__cardName__}}", cardName).replace("${{__chartId__}}", chartId).replace("${{__chartType__}}", card_dict["unit"]).replace("${{__data__}}", card_dict["data"])
    
    
    
    return chartTags
    
  def getChartJsScript(self, chartId, chartType, chartLabels, chartData, chartDataUnit = ""):
    if chartType == "area":
      chartJsScript = """
<script>
    // Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

function number_format(number, decimals, dec_point, thousands_sep) {
  // *     example: number_format(1234.56, 2, ',', ' ');
  // *     return: '1 234,56'
  number = (number + '').replace(',', '').replace(' ', '');
  var n = !isFinite(+number) ? 0 : +number,
    prec = !isFinite(+decimals) ? 0 : Math.abs(decimals),
    sep = (typeof thousands_sep === 'undefined') ? ',' : thousands_sep,
    dec = (typeof dec_point === 'undefined') ? '.' : dec_point,
    s = '',
    toFixedFix = function(n, prec) {
      var k = Math.pow(10, prec);
      return '' + Math.round(n * k) / k;
    };
  // Fix for IE parseFloat(0.55).toFixed(0) = 0;
  s = (prec ? toFixedFix(n, prec) : '' + Math.round(n)).split('.');
  if (s[0].length > 3) {
    s[0] = s[0].replace(/\B(?=(?:\d{3})+(?!\d))/g, sep);
  }
  if ((s[1] || '').length < prec) {
    s[1] = s[1] || '';
    s[1] += new Array(prec - s[1].length + 1).join('0');
  }
  return s.join(dec);
}

// Area Chart Example
var ctx = document.getElementById("${{__chartId__}}");
var myLineChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: ${{__chartLabels__}},
    datasets: [{
      label: "Earnings",
      lineTension: 0.3,
      backgroundColor: "rgba(78, 115, 223, 0.05)",
      borderColor: "rgba(78, 115, 223, 1)",
      pointRadius: 3,
      pointBackgroundColor: "rgba(78, 115, 223, 1)",
      pointBorderColor: "rgba(78, 115, 223, 1)",
      pointHoverRadius: 3,
      pointHoverBackgroundColor: "rgba(78, 115, 223, 1)",
      pointHoverBorderColor: "rgba(78, 115, 223, 1)",
      pointHitRadius: 10,
      pointBorderWidth: 2,
      data: ${{__chartData__}},
    }],
  },
  options: {
    maintainAspectRatio: false,
    layout: {
      padding: {
        left: 10,
        right: 25,
        top: 25,
        bottom: 0
      }
    },
    scales: {
      xAxes: [{
        time: {
          unit: 'date'
        },
        gridLines: {
          display: false,
          drawBorder: false
        },
        ticks: {
          maxTicksLimit: 7
        }
      }],
      yAxes: [{
        ticks: {
          maxTicksLimit: 5,
          padding: 10,
          // Include a dollar sign in the ticks
          callback: function(value, index, values) {
            return '${{__dataUnit__}}' + number_format(value);
          }
        },
        gridLines: {
          color: "rgb(234, 236, 244)",
          zeroLineColor: "rgb(234, 236, 244)",
          drawBorder: false,
          borderDash: [2],
          zeroLineBorderDash: [2]
        }
      }],
    },
    legend: {
      display: false
    },
    tooltips: {
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      titleMarginBottom: 10,
      titleFontColor: '#6e707e',
      titleFontSize: 14,
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      intersect: false,
      mode: 'index',
      caretPadding: 10,
      callbacks: {
        label: function(tooltipItem, chart) {
          var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
          return datasetLabel + ': $' + number_format(tooltipItem.yLabel);
        }
      }
    }
  }
});
</script>
""".replace("${{__chartId__}}", chartId).replace("${{__chartLabels__}}", "{}".format(chartLabels)).replace("${{__chartData__}}", "{}".format(chartData)).replace("${{__dataUnit__}}", chartDataUnit)
    
    
    elif chartType == "pie":
      chartJsScript = """
      <script>
      // Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

// Pie Chart Example
var ctx = document.getElementById("${{__chartId__}}");
var myPieChart = new Chart(ctx, {
  type: 'doughnut',
  data: {
    labels: ${{__chartLabels__}},
    datasets: [{
      data: ${{__chartData__}},
      backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc'],
      hoverBackgroundColor: ['#2e59d9', '#17a673', '#2c9faf'],
      hoverBorderColor: "rgba(234, 236, 244, 1)",
    }],
  },
  options: {
    maintainAspectRatio: false,
    tooltips: {
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      caretPadding: 10,
    },
    legend: {
      display: false
    },
    cutoutPercentage: 80,
  },
});
</script>
""".replace("${{__chartId__}}", chartId).replace("${{__chartLabels__}}", "{}".format(chartLabels)).replace("${{__chartData__}}", "{}".format(chartData)).replace("${{__dataUnit__}}", chartDataUnit)

    else:
      logError("chartType:[{}] isn't supported".format(chartType))
      
      chartJsScript = ""
    return chartJsScript