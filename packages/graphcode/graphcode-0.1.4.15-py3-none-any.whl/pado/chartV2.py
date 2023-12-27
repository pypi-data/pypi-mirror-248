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

from random import random

class GcChart:
  def __init__(self, theme = "default"):
    self.theme = theme
    
    self.htmlChartTags = ""
    self.jsChartCode = ""
    
    self.color_list = [
      "#2980B9",
      "#1ABC9C",
      "#C0392B",
      "#9B59B6",
      "#27AE60",
      "#F1C40F",
      "#E67E22",
      "#ECF0F1",
      "#95A5A6",
      "#34495E",
      
      "#3498DB",
      "#16A085",
      "#E74C3C",
      "#8E44AD",
      "#2ECC71",
      "#F39C12",
      "#D35400",
      "#BDC3C7",
      "#7F8C8D",
      "#2C3E50"
      ]
    
    self.hoverColor_list = [
      "#2471A3",
      "#17A589",
      "#A93226",
      "#884EA0",
      "#229954",
      "#D4AC0D",
      "#CA6F1E",
      "#D0D3D4",
      "#839192",
      "#2E4053",
      
      "#2E86C1",
      "#138D75",
      "#CB4335",
      "#7D3C98",
      "#28B463",
      "#D68910",
      "#D68910",
      "#BA4A00",
      "#A6ACAF",
      "#707B7C",
      "#273746"
      ]
  
  def getColor(self, count = None):
    if isinstance(count, int):
      return self.color_list[count % len(self.color_list)]
    else:
      return self.color_list[int(count * random())]
    
  def getHoverColor(self, count = None):
    if isinstance(count, int):
      return self.hoverColor_list[count % len(self.hoverColor_list)]
    else:
      return self.hoverColor_list[int(count * random())]
    
  def getChartId(self, chartName):
    try:
      chartId = "{}{}".format(chartName[0].lower(), chartName[1:].replace(" ", ""))
    except:
      logException("unable to set chartId with chartName:[{}]".format(chartName))
      chartId = chartName.lower()
      
    return chartId
  
  def addChart(self, gc_dict, chartName, chart_dict):
    if "charts" not in gc_dict.keys():
      gc_dict["charts"] = {}
      logInfo("'charts' is initiated at 'gc_dict'")
      
    if chartName in gc_dict["charts"].keys():
      raiseValueError("chartName:[{}] is already registered. Please updateChart(chartName, chart_dict)".format(chartName))
    else:
      for chartKey in ["title", "type", "data"]:
        if chartKey in chart_dict.keys():
          pass
        else:
          raiseValueError("chartKey:[{}] isn't provided".format(chartKey))
      
      gc_dict["charts"][chartName] = chart_dict
    
    return gc_dict["charts"][chartName]
      
  def updateChart(self, gc_dict, chartName, chart_dict):
    if "charts" in gc_dict.keys():
      if chartName in gc_dict["charts"].keys():
        for chartKey in chart_dict.keys():
          gc_dict["charts"][chartName][chartKey] = chart_dict[chartKey]
      else:
        raiseValueError("chartName:[{}] is not registered. Please registerChart(chartName, chart_dict)".format(chartName))
    else:
      raiseValueError("'charts' is not initiated at 'gc_dict'")
      
    return gc_dict["charts"][chartName]
    
  def updateChartData(self, gc_dict, chartName, data):
    if "charts" in gc_dict.keys():
      if chartName in gc_dict["charts"].keys():
        if isinstance(data, dict):
          gc_dict["charts"][chartName]["data"] = data
        else:
          raiseValueError("'dict' is expected at type:{}:chartData:[{}]".format(type(data), data))
      else:
        raiseValueError("chartName:[{}] is not registered. Please registerChart(chartName, chart_dict)".format(chartName))
    else:
      raiseValueError("'charts' is not initiated at 'gc_dict'")
      
    return gc_dict["charts"][chartName]
    
  def getJsChartCode(self):
    return self.jsChartCode
  
  def getChartTags(self, chartName, chart_dict):
        
    if self.isValidChartData(chart_dict) == False:
      return """<!--  """ + chartName + """: unsupported chart values -->
                  <div class="col-xl-4 col-lg-5">
                      <div class="card shadow mb-4">
                          <!-- Card Header - Dropdown -->
                          <div
                              class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
                              <h6 class="m-0 font-weight-bold text-primary">""" + "Unsupport Chart:{}".format(chartName) + """</h6>
                              </div>
                          </div>
                          <!-- Card Body -->
                          <div class="card-body">
                              <div class="mt-4 text-center small">
                                  chart_dict:""" + "{}".format(chart_dict) + """<span class="mr-2">
                              </div>
                              
                          </div>
                      </div>
                  </div>
"""
    
    elif chart_dict["type"] in ["pie", "donut"]:
      chartTags = self.getPieChartTag(chartName, chart_dict)
      
    elif chart_dict["type"] in ["area", "line"]:
      chartTags = self.getAreaChartTag(chartName, chart_dict)
    
    elif chart_dict["type"] in ["bar"]:
      chartTags = self.getBarChartTags(chartName, chart_dict)
      
    else:
      chartTags = self.getUnsupportChartTags(chartName, chart_dict)
    
    return chartTags
  
  def isValidChartData(self, chart_dict):
    areValidChartValues = True
    for chartKey in ["title", "type", "width", "height", "data"]:
      if chartKey not in chart_dict.keys():
        if chartKey in ["width", "height"]:
          chart_dict[chartKey] = 1
          logWarn("chartKey:[{}] isn't provided, so it's set to {}".format(chartKey, chart_dict[chartKey]))
          
        else:
          logError("chartKey:[{}] isn't provided".format(chartKey))
          areValidChartValues = False
      
      elif chartKey in ["data"]:
        if isinstance(chart_dict["data"], dict) and len(chart_dict["data"].keys()) > 0:
          if chart_dict["type"] in ["pie", "donut"]:
            for legend in chart_dict["data"].keys():
              if isinstance(chart_dict["data"][legend], int) or isinstance(chart_dict["data"][legend], float):
                pass
              else:
                logError("unexpected type:{}:data[{}]:[{}] at {} chart".format(type(chart_dict["data"][legend]), legend, chart_dict["data"][legend], chart_dict["type"]))
                areValidChartValues = False
                
          elif chart_dict["type"] in ["area", "line"]:
            for legend in chart_dict["data"].keys():
              if isinstance(chart_dict["data"][legend], dict):
                pass
              else:
                logError("unexpected type:{}:data[{}]:[{}] at {} chart".format(type(chart_dict["data"][legend]), legend, chart_dict["data"][legend], chart_dict["type"]))
                areValidChartValues = False
            
        else:
          logError("'dict' or a single legend should be found at data:[{}]".format(chart_dict["data"]))
          areValidChartValues = False
          
    return areValidChartValues
  
  def getUnsupportChartTags(self, chart_dict):
    chartTags = """<!--  Revenue Sources: pie Chart -->
                  <div class="col-xl-4 col-lg-5">
                      <div class="card shadow mb-4">
                          <!-- Card Header - Dropdown -->
                          <div
                              class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
                              <h6 class="m-0 font-weight-bold text-primary">""" + chart_dict["title"] +"""</h6>
                              </div>
                          </div>
                          <!-- Card Body -->
                          <div class="card-body">
                              <div class="mt-4 text-center small">
                                  labels:""" + "{}".format(chart_dict["labels"]) + """<span class="mr-2">
                              </div>
                              <div class="mt-4 text-center small">
                                  data:""" + "{}".format(chart_dict["data"]) + """<span class="mr-2">
                              </div>
                          </div>
                      </div>
                  </div>
"""
    return chartTags
    
  def getPieChartTag(self, chartName, chart_dict):
    chartTitle = chart_dict["title"]
    chartId = "\"{}\"".format(self.getChartId(chart_dict["title"])) 
    
    if "displayLegend" in chart_dict.keys() and chart_dict["displayLegend"]:
      displayLegend = "true"
    else:
      displayLegend = "false"
      
    if "minValue" in chart_dict.keys():
      minValue = "min: {},".format(chart_dict["minValue"])
    else:
      minValue = ""
    
    if "maxValue" in chart_dict.keys():
      maxValue = "max: {},".format(chart_dict["maxValue"])
    else:
      maxValue = ""
          
    if "maxTicksLimit" in chart_dict.keys():
      maxTicksLimit = "maxTicksLimit: {},".format(chart_dict["maxTicksLimit"])
    else:
      maxTicksLimit = ""
    
    if "padding" in chart_dict.keys():
      yAxesPadding = "padding: {},".format(chart_dict["padding"])
    else:
      yAxesPadding = "padding: 10,"
    
    if "unit" in chart_dict.keys():
      chartUnit = "{}".format(chart_dict["unit"])
    else:
      chartUnit = ""
    
    chartWidth = "{}".format(chart_dict["width"])
    chartHeight = "{}".format(chart_dict["height"])
    
    chartLegend_list = []
    chartValue_list = []
    for thisLegend in chart_dict["data"].keys():
      chartLegend_list.append(thisLegend)
      chartValue_list.append(chart_dict["data"][thisLegend])
    
    chartLegend = "{}".format(chartLegend_list)
    chartValues = "{}".format(chartValue_list)
    
    chartColors = "{}".format(self.color_list)
    chartHoverColors = "{}".format(self.hoverColor_list)
    
    legendTags = ""
    labelCount = 0
    for thisLabel in chartLegend_list:
      legendTags += """
                                  <span class="mr-2">
                                      <i class="fas fa-circle" style=""" + "\"color:{}\"".format(self.getColor(labelCount)) +"""></i> """ + thisLabel + """
                                  </span>"""
      labelCount += 1
      
    
                                  
    cahrtTags = """
                <!--  Revenue Sources: pie Chart -->
                  <div class="col-xl-""" + chartWidth + """ col-lg-""" + chartHeight + """ ">
                      <div class="card shadow mb-4">
                          <!-- Card Header - Dropdown -->
                          <div
                              class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
                              <h6 class="m-0 font-weight-bold text-primary">""" + chartTitle + """</h6>
                              
                                    <div class="dropdown no-arrow">
                                        <a class="dropdown-toggle" href="#" role="button" id="dropdownMenuLink"
                                            data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                            <i class="fas fa-ellipsis-v fa-sm fa-fw text-gray-400"></i>
                                        </a>
                                        <div class="dropdown-menu dropdown-menu-right shadow animated--fade-in"
                                            aria-labelledby="dropdownMenuLink">
                                            
                                            <div class="dropdown-header">Dropdown Header2:</div>
              
                                            <a class="dropdown-item" href="Action2">Action2</a>
              
                                            <a class="dropdown-item" href="Another Action2">Another Action2</a>
              
                                            <div class="dropdown-divider"></div>
              
                                            <a class="dropdown-item" href="Something Else2">Something Else2</a>
              
                                        </div>
          
                              </div>
                          </div>
                          <!-- Card Body -->
                          <div class="card-body">
                              <div class="chart-pie pt-4 pb-2">
                                  <canvas id=""" + chartId + """></canvas>
                              </div>
                              <div class="mt-4 text-center small">
                              """ + legendTags + """
                              </div>
                          </div>
                      </div>
                  </div>
"""
              
    self.jsChartCode += """
<script>
// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

// Pie Chart Example
var ctx = document.getElementById(""" + chartId + """);
var myPieChart = new Chart(ctx, {
  type: 'doughnut',
  data: {
    labels: """ + chartLegend + """,
    datasets: [{
      data: """ + chartValues + """,
      backgroundColor: """ + chartColors + """,
      hoverBackgroundColor: """ + chartHoverColors + """,
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
      display: """ + displayLegend + """
    },
    cutoutPercentage: 80,
  },
});
</script>
"""
    return cahrtTags
  
  def getAreaChartTag(self, chartName, chart_dict):
    for key in chart_dict.keys():
      logDebug("{}:{}".format(key, chart_dict[key]))
      
    chartTitle = chart_dict["title"]
    chartId = "\"{}\"".format(self.getChartId(chartName)) 
    
    chartWidth = "{}".format(chart_dict["width"])
    chartHeight = "{}".format(chart_dict["height"])
    
    if "displayLegend" in chart_dict.keys() and chart_dict["displayLegend"]:
      displayLegend = "true"
    else:
      displayLegend = "false"
      
    if "minValue" in chart_dict.keys():
      minValue = "min: {},".format(chart_dict["minValue"])
    else:
      minValue = ""
    
    if "maxValue" in chart_dict.keys():
      maxValue = "max: {},".format(chart_dict["maxValue"])
    else:
      maxValue = ""
          
    if "maxTicksLimit" in chart_dict.keys():
      maxTicksLimit = "maxTicksLimit: {},".format(chart_dict["maxTicksLimit"])
    else:
      maxTicksLimit = ""
    
    if "padding" in chart_dict.keys():
      yAxesPadding = "padding: {},".format(chart_dict["padding"])
    else:
      yAxesPadding = "padding: 10,"
    
    if "unit" in chart_dict.keys():
      chartUnit = "{}".format(chart_dict["unit"])
    else:
      chartUnit = ""
    
    chartLegend_list = []
    chartLabel_list = []
    for thisLegend in chart_dict["data"].keys():
      chartLegend_list.append(thisLegend)
      
      for thisLabel in chart_dict["data"][thisLegend].keys():
        if thisLabel not in chartLabel_list:
          chartLabel_list.append(thisLabel)
    chartLabels = "{}".format(chartLabel_list)
    logDebug("{}:{}".format(chartId,chartLabels))
    
    dataSets_dict = {}
    for thisLegend in chart_dict["data"].keys():
      dataSets_dict[thisLegend] = []
      for thisLabel in chartLabel_list:
        if thisLabel in chart_dict["data"][thisLegend].keys():
          dataSets_dict[thisLegend].append(chart_dict["data"][thisLegend][thisLabel])
        else:
          dataSets_dict[thisLegend].append(None)
    
      logDebug("{}[{}](len:{:,}):{}".format(chartId, thisLegend, len(dataSets_dict[thisLegend]), dataSets_dict[thisLegend]))
      
    chartColors = "{}".format(self.color_list)
    chartHoverColors = "{}".format(self.hoverColor_list)
    
    legendTags = ""
    thiLegendCount = 0
    for thiLegend in chartLegend_list:
      legendTags += """
                                  <span class="mr-2">
                                      <i class="fas fa-circle" style=""" + "\"color:{}\"".format(self.getColor(thiLegendCount)) +"""></i> """ + thiLegend + """
                                  </span>"""
      thiLegendCount += 1
    
    dataSetTags = ""
    dataSetCount = 0
    for thisLegend in dataSets_dict.keys():
      logDebug("{}[{}](len:{:,}):{}".format(chartId, thisLegend, len(dataSets_dict[thisLegend]), dataSets_dict[thisLegend]))
      
      thisDataSet = ""
      for dataValue in dataSets_dict[thisLegend]:
        if dataValue in [None, "None", ""]:
          dataValue = "null"
        
        if thisDataSet == "":
          thisDataSet += "[{}".format(dataValue)
        else:
          thisDataSet += ", {}".format(dataValue)
      
      thisDataSet += "]"
      logDebug("{}[{}](len:{:,}):{}".format(chartId, thisLegend, len(dataSets_dict[thisLegend]), thisDataSet))
      
      thisDataSetTag = "{}".format(
        {
          "label": "{}".format(thisLegend),
          "lineTension": 0.3,
          "backgroundColor": "rgba(208, 211, 212, 0.05)",
          "borderColor": "{}".format(self.getColor(dataSetCount)),
          "pointRadius": 3,
          "pointBackgroundColor": "{}".format(self.getColor(dataSetCount)),
          "pointBorderColor": "{}".format(self.getColor(dataSetCount)),
          "pointHoverRadius": 3,
          "pointHoverBackgroundColor": "{}".format(self.getHoverColor(dataSetCount)),
          "pointHoverBorderColor": "{}".format(self.getHoverColor(dataSetCount)),
          "pointHitRadius": 10,
          "pointBorderWidth": 2,
          "data": "${{__thisDataSet__}}",
          }
        ).replace("'${{__thisDataSet__}}'", thisDataSet)
      
      if dataSetTags == "":
        dataSetTags += "[{}".format(thisDataSetTag)
      else:
        dataSetTags += ", {}".format(thisDataSetTag)
    
      dataSetCount += 1
    
    dataSetTags += "]"
    
    cahrtTags = """
                  <!-- """ + chartTitle + """: area Chart -->
                  <div class="col-xl-""" + chartWidth + """ col-lg-""" + chartHeight + """ ">
                      <div class="card shadow mb-4">
                          <!-- Card Header - Dropdown -->
                          <div
                              class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
                              <h6 class="m-0 font-weight-bold text-primary">""" + chartTitle + """</h6>
                              
                                    <div class="dropdown no-arrow">
                                        <a class="dropdown-toggle" href="#" role="button" id="dropdownMenuLink"
                                            data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                            <i class="fas fa-ellipsis-v fa-sm fa-fw text-gray-400"></i>
                                        </a>
                                        <div class="dropdown-menu dropdown-menu-right shadow animated--fade-in"
                                            aria-labelledby="dropdownMenuLink">
                                            
                                            <div class="dropdown-header">Dropdown Header:</div>
              
                                            <a class="dropdown-item" href="Action">Action</a>
              
                                            <a class="dropdown-item" href="Another Action">Another Action</a>
              
                                            <div class="dropdown-divider"></div>
              
                                            <a class="dropdown-item" href="Something Else">Something Else</a>
              
                                        </div>
          
                              </div>
                          </div>
                          <!-- Card Body -->
                          <div class="card-body">
                              <div class="chart-area">
                                  <canvas id=""" + chartId + """></canvas>
                              </div>
                          </div>
                      </div>
                  </div>
                  
"""
              
    self.jsChartCode += """
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
var ctx = document.getElementById(""" + chartId + """);
var myLineChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: """ + chartLabels +""",
    datasets: """ + dataSetTags + """,
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
            return '""" + chartUnit + """' + number_format(value);
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
      display: """ + displayLegend + """
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
          return datasetLabel + ': """ + chartUnit + """' + number_format(tooltipItem.yLabel);
        }
      }
    }
  }
});
</script>           
"""
    return cahrtTags
  
  
  def getBarChartTags(self, chartName, chart_dict):
    for key in chart_dict.keys():
      logDebug("{}:{}".format(key, chart_dict[key]))
      
    chartTitle = chart_dict["title"]
    chartId = "\"{}\"".format(self.getChartId(chartName)) 
    
    chartWidth = "{}".format(chart_dict["width"])
    chartHeight = "{}".format(chart_dict["height"])
    
    if "displayLegend" in chart_dict.keys() and chart_dict["displayLegend"]:
      displayLegend = "true"
    else:
      displayLegend = "false"
    
    if "minValue" in chart_dict.keys():
      minValue = "min: {},".format(chart_dict["minValue"])
    else:
      minValue = ""
    
    if "maxValue" in chart_dict.keys():
      maxValue = "max: {},".format(chart_dict["maxValue"])
    else:
      maxValue = ""
          
    if "maxTicksLimit" in chart_dict.keys():
      maxTicksLimit = "maxTicksLimit: {},".format(chart_dict["maxTicksLimit"])
    else:
      maxTicksLimit = ""
    
    if "padding" in chart_dict.keys():
      yAxesPadding = "padding: {},".format(chart_dict["padding"])
    else:
      yAxesPadding = "padding: 10,"
    
    if "unit" in chart_dict.keys():
      chartUnit = "{}".format(chart_dict["unit"])
    else:
      chartUnit = ""
    
    
    chartLegend_list = []
    chartLabel_list = []
    for thisLegend in chart_dict["data"].keys():
      chartLegend_list.append(thisLegend)
      
      for thisLabel in chart_dict["data"][thisLegend].keys():
        if thisLabel not in chartLabel_list:
          chartLabel_list.append(thisLabel)
    chartLabels = "{}".format(chartLabel_list)
    logDebug("{}:{}".format(chartId,chartLabels))
    
    dataSets_dict = {}
    for thisLegend in chart_dict["data"].keys():
      dataSets_dict[thisLegend] = []
      for thisLabel in chartLabel_list:
        if thisLabel in chart_dict["data"][thisLegend].keys():
          dataSets_dict[thisLegend].append(chart_dict["data"][thisLegend][thisLabel])
        else:
          dataSets_dict[thisLegend].append(None)
    
      logDebug("{}[{}](len:{:,}):{}".format(chartId, thisLegend, len(dataSets_dict[thisLegend]), dataSets_dict[thisLegend]))
      
    legendTags = ""
    thiLegendCount = 0
    for thiLegend in chartLegend_list:
      legendTags += """
                                  <span class="mr-2">
                                      <i class="fas fa-circle" style=""" + "\"color:{}\"".format(self.getColor(thiLegendCount)) +"""></i> """ + thiLegend + """
                                  </span>"""
      thiLegendCount += 1
    
    dataSetTags = ""
    dataSetCount = 0
    for thisLegend in dataSets_dict.keys():
      logDebug("{}[{}](len:{:,}):{}".format(chartId, thisLegend, len(dataSets_dict[thisLegend]), dataSets_dict[thisLegend]))
      
      thisDataSet = ""
      for dataValue in dataSets_dict[thisLegend]:
        if dataValue in [None, "None", ""]:
          dataValue = "null"
        
        if thisDataSet == "":
          thisDataSet += "[{}".format(dataValue)
        else:
          thisDataSet += ", {}".format(dataValue)
      
      thisDataSet += "]"
      logDebug("{}[{}](len:{:,}):{}".format(chartId, thisLegend, len(dataSets_dict[thisLegend]), thisDataSet))
      
      chartColors = "{}".format(self.getColor(dataSetCount))
      chartHoverColors = "{}".format(self.getHoverColor(dataSetCount))
      
      thisDataSetTag = "{}".format(
        {
          "label": thisLegend,
          "backgroundColor": chartColors,
          "hoverBackgroundColor": chartHoverColors,
          "borderColor": chartColors,
          "data": "${{__thisDataSet__}}"
          }
        ).replace("'${{__thisDataSet__}}'", thisDataSet)
      
      if dataSetTags == "":
        dataSetTags += "[{}".format(thisDataSetTag)
      else:
        dataSetTags += ", {}".format(thisDataSetTag)
    
      dataSetCount += 1
    
    dataSetTags += "]"
    
    cahrtTags = """
                  <!-- """ + chartTitle + """: area Chart -->
                  <div class="col-xl-""" + chartWidth + """ col-lg-""" + chartHeight + """ ">
                      <div class="card shadow mb-4">
                          <!-- Card Header - Dropdown -->
                          <div
                              class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
                              <h6 class="m-0 font-weight-bold text-primary">""" + chartTitle + """</h6>
                              
                                    <div class="dropdown no-arrow">
                                        <a class="dropdown-toggle" href="#" role="button" id="dropdownMenuLink"
                                            data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                            <i class="fas fa-ellipsis-v fa-sm fa-fw text-gray-400"></i>
                                        </a>
                                        <div class="dropdown-menu dropdown-menu-right shadow animated--fade-in"
                                            aria-labelledby="dropdownMenuLink">
                                            
                                            <div class="dropdown-header">Dropdown Header:</div>
              
                                            <a class="dropdown-item" href="Action">Action</a>
              
                                            <a class="dropdown-item" href="Another Action">Another Action</a>
              
                                            <div class="dropdown-divider"></div>
              
                                            <a class="dropdown-item" href="Something Else">Something Else</a>
              
                                        </div>
          
                              </div>
                          </div>
                          <!-- Card Body -->
                          <div class="card-body">
                              <div class="chart-area">
                                  <canvas id=""" + chartId + """></canvas>
                              </div>
                          </div>
                      </div>
                  </div>
                  
"""
              
    self.jsChartCode += """
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

// Bar Chart Example
var ctx = document.getElementById(""" + chartId + """);
var myBarChart = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: """ + chartLabels + """,
    datasets:""" + dataSetTags + """,
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
          unit: 'month'
        },
        gridLines: {
          display: false,
          drawBorder: false
        },
        ticks: {
          maxTicksLimit: 6
        },
        maxBarThickness: 25,
      }],
      yAxes: [{
        ticks: {
          """ + minValue + """
          """ + maxValue + """
          """ + maxTicksLimit + """
          """ + yAxesPadding + """
          // Include a dollar sign in the ticks
          callback: function(value, index, values) {
            return '""" + chartUnit + """' + number_format(value);
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
      display: """ + displayLegend + """
    },
    tooltips: {
      titleMarginBottom: 10,
      titleFontColor: '#6e707e',
      titleFontSize: 14,
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      caretPadding: 10,
      callbacks: {
        label: function(tooltipItem, chart) {
          var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
          return datasetLabel + ': """ + chartUnit + """' + number_format(tooltipItem.yLabel);
        }
      }
    },
  }
});
</script>
"""
    return cahrtTags
  
 