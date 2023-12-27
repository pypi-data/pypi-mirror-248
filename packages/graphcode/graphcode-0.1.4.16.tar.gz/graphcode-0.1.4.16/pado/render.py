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

from pado.chart import GcChart
from pado.form import GcForm

import json
import time

class GcRender:
  def __init__(self, request = None):
    self.request = request
    self.gcChart = GcChart()
    
    self.cardJsTags = ""
          
  def getParameters(self, kwargs):
    if "type" in kwargs.keys():
      type = kwargs["type"]
    else:
      logError("'type' should be provided")
      return None

    if "unit" in kwargs.keys():
      unit = kwargs["unit"]
    else:
      unit = ""
    
    if "size" in kwargs.keys():
      if "width" in kwargs["size"].keys():
        try:
          size_width = float(kwargs["size"]["width"])
        except:
          logException("unable to get width:[{}]".format(kwargs["size"]["width"]))
          size_width = -1
      else:
        size_width = -1
            
      if "height" in kwargs["size"].keys():
        try:
          size_height = float(kwargs["size"]["height"])
        except:
          logException("unable to get height:[{}]".format(kwargs["size"]["height"]))
          size_height = -1
      else:
        size_height = -1
      
    else:
      size_width = -1
      size_height = -1
    
    
    if "display" in kwargs.keys():
      if "title" in kwargs["display"].keys():
        if isinstance(kwargs["display"]["title"], bool):
          display_title = kwargs["display"]["title"]
        else:
          logError("'display.title' should be the 'bool' format".format(kwargs["display"]["title"]))
          display_title = False
      else:
        display_title = False
        
      if "label" in kwargs["display"].keys():
        if isinstance(kwargs["display"]["label"], bool):
          display_label = kwargs["display"]["label"]
        else:
          logError("'display.label' should be the 'bool' format".format(kwargs["display"]["label"]))
          display_label = False
      else:
        display_label = False
          
      if "data" in kwargs["display"].keys():
        if isinstance(kwargs["display"]["data"], bool):
          display_data = kwargs["display"]["data"]
        else:
          logError("'display.data' should be the 'bool' format".format(kwargs["display"]["data"]))
          display_data = False
      else:
        display_data = False
      
    else:
      display_title = False
      display_label = False
      display_data = False
    
    return {"type": type,
            "unit": unit,
            "size_width": size_width,
            "size_height": size_height,
            "display_title": display_title,
            "display_label": display_label,
            "display_data": display_data
            }
    
  def generateCardTags(self, card_dict, form_dict, depth = 0):
    if depth == 0:
      cardTags = """
                <div class="container-fluid">
                """
    else:
      cardTags = ""
      
    for cardName in card_dict.keys():
      cardItem_dict = card_dict[cardName]
      cardNameUrl = "./{}{}".format(cardName[0].lower(), cardName.replace(" ","")[1:])
      #logInfo("{}:cardName:[{}]:url:[{}]:[{}]".format(depth, cardName, cardNameUrl, cardItem_dict))
      
      if "type" in cardItem_dict.keys() and cardItem_dict["type"] in ["title", "object"]:
        #logInfo("type:[{}]".format(cardItem_dict["type"]))
        
        modalTags = ""
        if card_dict[cardName]["type"] == "title":
          if "modals" in cardItem_dict.keys() and isinstance(cardItem_dict["modals"], list):
            modalTags += """
                        <!-- Nav Item - Actions -->
                        <div class="nav-item dropdown no-arrow">
                            <a class="nav-link dropdown-toggle text-gray-50" href="#" id="actionDropdown" role="button"
                                data-toggle="dropdown"><i
                                  class="fas fa-bars fa-sm text-gray-400"></i>&nbsp;&nbsp;Actions</a>
                            <!-- Dropdown - Actions -->
                            <div class="dropdown-menu dropdown-menu-right shadow"
                                aria-labelledby="actionDropdown">"""
                                
            for modalName in cardItem_dict["modals"]:
              modalTags += """
                              <a href="#" class="dropdown-item" data-toggle="modal" data-target="#${{__modalId__}}Modal"><i
                                      class="fas fa-desktop fa-sm text-gray-400"></i>&nbsp;&nbsp;${{__modalName__}}</a>
                      """.replace("${{__modalName__}}", modalName).replace("${{__modalId__}}", "{}{}".format(modalName[0].lower(), modalName.replace(" ", "")[1:]))
                                
            modalTags += """
                            </div>
                        </div>
                        """
                        
            #for modalName in cardItem_dict["modals"]:
              
              #modalTags += """
              #                <a href="#" class="d-none d-sm-inline-block btn btn-sm btn-primary shadow-sm" data-toggle="modal" data-target="#${{__modalId__}}Modal"><i
              #                        class="fas fa-download fa-sm text-white-50"></i>${{__modalName__}}</a>
              #        """.replace("${{__modalName__}}", modalName).replace("${{__modalId__}}", "{}{}".format(modalName[0].lower(), modalName.replace(" ", "")[1:]))
                    
          if "display" in cardItem_dict.keys() and "title" in cardItem_dict["display"].keys() and isinstance(cardItem_dict["display"]["title"], bool) and cardItem_dict["display"]["title"]:
            cardTags += """
                      <!-- Page Heading -->
                      <div class="d-sm-flex align-items-center justify-content-between mb-4">
                          {% if gc.rulePath != "" %}
                            <div><h1 class="h3 mb-0 text-gray-800" style="display:inline;"><a href='/{{ gc.ruleName }}'>{{ gc.ruleName }}</a>&nbsp;/&nbsp;<a href='/{{ gc.ruleName }}/{{ gc.rulePath }}'>{{ gc.rulePath }}</a></h1>&nbsp;[<a 
                                href="#" data-toggle="modal" data-target="#{{ gc.ruleName }}Modal">hint</a>]</div>
                            
                            
                          {% else %}
                            <div><h1 class="h3 mb-0 text-gray-800" style="display:inline;"><a href='/{{ gc.ruleName }}'>${{__cardName__}}</a></h1>&nbsp;[<a 
                                href="#" data-toggle="modal" data-target="#{{ gc.ruleName }}Modal">hint</a>]</div>
                                
                          {% endif %}
                          <div style="display:inline;">${{__modals__}}</div>
                      </div>
                      """.replace("${{__cardName__}}", cardName).replace("${{__cardNameUrl__}}", cardNameUrl).replace("${{__modals__}}", modalTags)
          else:
            cardTags += """
                        <!-- Page Heading -->
                        <div class="d-sm-flex align-items-center justify-content-between mb-4" style="display:inline;">
                            ${{__modals__}}
                        </div>
                        """.replace("${{__modals__}}", modalTags)
        
        if isinstance(cardItem_dict["data"], list):
          for subCardItems in cardItem_dict["data"]:
            #logInfo("subCardItems:[{}]".format(depth, subCardItems))
            
            if depth == 1:
              cardTags += """
                        <!-- Begin: Content Row -->
                        <div class="row">
              """
              cardTags += self.generateCardTags(card_dict=subCardItems, form_dict=form_dict, depth=depth + 1)
              
              cardTags += """
                        </div>
                        <!-- End: Content Row -->
              """
            else:
              cardTags += self.generateCardTags(card_dict=subCardItems, form_dict=form_dict, depth=depth + 1)
        else:
          logError("unsupported card_dict:[{}]".format(card_dict))
          
      else:
        #logDebug("{}:{}:{}".format(depth, cardName, cardItem_dict))
        cardTags += self.getCardTags(cardName, cardItem_dict, form_dict, depth)

          
    if depth == 0:
      cardTags += """
                </div>
                <!-- /.container-fluid -->
          """
            
    return cardTags
  
  def getCardTags(self, cardName, card_dict, form_dict, depth):
    #logDebug("{}:{}:{}".format(depth, cardName, card_dict))
    
    if isinstance(card_dict, dict):
      if "type" in card_dict.keys():
        cardId = "{}{}".format(cardName[0].lower(), cardName.replace(" ","")[1:])
        
        width = "3"
        height = "1"
        if "size" in card_dict.keys():
          if "width" in card_dict["size"]:
            width = card_dict["size"]["width"]
          
          if "height" in card_dict["size"]:
            height = card_dict["size"]["height"]
                                      
        if "dropdown-items" in card_dict.keys() and isinstance(card_dict["dropdown-items"], list):
          dropdownTags = ""
          for item_dict in card_dict["dropdown-items"]:
            if dropdownTags == "" and item_dict["name"] not in ["dropdwon-divider"]:
              dropdownTags += """
                                            <div class="dropdown-header">${{__dropdownItemName__}}:</div>
              """.replace("${{__dropdownItemName__}}", item_dict["name"])
              
            elif item_dict["name"] == "dropdown-divider":
              dropdownTags += """
                                            <div class="dropdown-divider"></div>
              """
            else:
              dropdownTags += """
                                            <a class="dropdown-item" href="${{__dropdownItemTarget__}}">${{__dropdownItemTarget__}}</a>
              """.replace("${{__dropdownItemName__}}", item_dict["name"]).replace("${{__dropdownItemTarget__}}", item_dict["name"])
              
          dropDownItemTags = """
                                    <div class="dropdown no-arrow">
                                        <a class="dropdown-toggle" href="#" role="button" id="dropdownMenuLink"
                                            data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                            <i class="fas fa-ellipsis-v fa-sm fa-fw text-gray-400"></i>
                                        </a>
                                        <div class="dropdown-menu dropdown-menu-right shadow animated--fade-in"
                                            aria-labelledby="dropdownMenuLink">
                                            ${{__dropdownItems__}}
                                        </div>
          """.replace("${{__dropdownItems__}}", dropdownTags)
        else:
          dropDownItemTags = ""
        
        if "icon" in card_dict.keys() and isinstance(card_dict["icon"], str):
          iconTags = """
                                          <div class="col-auto">
                                              <i class="fas ${{__icon__}} fa-2x text-gray-300"></i>
                                          </div>
          """.replace("${{__icon__}}", card_dict["icon"])
        else:
          iconTags = ""
          
        if card_dict["type"] in ["text"]:
          if card_dict["unit"] == "percentage":
            cardTags = """
                          <!-- ${{__cardName__}} Card Example -->
                          <div class="col-xl-3 col-md-6 mb-4">
                              <div class="card border-left-info shadow h-100 py-2">
                                  <div class="card-body">
                                      <div class="row no-gutters align-items-center">
                                          <div class="col mr-2">
                                              <div class="text-xs font-weight-bold text-info text-uppercase mb-1">
                                                  ${{__cardName__}}</div>
                                              <div class="row no-gutters align-items-center">
                                                  <div class="col-auto">
                                                      <div class="h5 mb-0 mr-3 font-weight-bold text-gray-800">${{__data__}}</div>
                                                  </div>
                                                  <div class="col">
                                                      <div class="progress progress-sm mr-2">
                                                          <div class="progress-bar bg-info" role="progressbar"
                                                              style="width: ${{__data__}}" aria-valuenow="${{__data__}}" aria-valuemin="0"
                                                              aria-valuemax="100"></div>
                                                      </div>
                                                  </div>
                                              </div>
                                          </div>
                                          ${{__iconTags__}}
                                      </div>
                                  </div>
                              </div>
                          </div>
            """.replace("${{__cardName__}}", cardName).replace("${{__data__}}", card_dict["data"])
          
          else:
            cardTags = """
                          <!-- ${{__cardName__}} Card Example -->
                          <div class="col-xl-3 col-md-6 mb-4">
                              <div class="card border-left-primary shadow h-100 py-2">
                                  <div class="card-body">
                                      <div class="row no-gutters align-items-center">
                                          <div class="col mr-2">
                                              <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">
                                                  ${{__cardName__}}</div>
                                              <div class="h5 mb-0 font-weight-bold text-gray-800">${{__data__}}</div>
                                          </div>
                                          ${{__iconTags__}}
                                      </div>
                                  </div>
                              </div>
                          </div>
            """.replace("${{__cardName__}}", cardName).replace("${{__data__}}", card_dict["data"])
          
        elif  card_dict["type"] in ["box"]:
          if card_dict["unit"] == "progress-bar":
            cardTags = """                       
                          <!-- Content Column -->
                          <div class="col-lg-6 mb-4">
  
                              <!-- ${{__cardName__}} Card Example -->
                              <div class="card shadow mb-4">
                                  <div class="card-header py-3">
                                      <h6 class="m-0 font-weight-bold text-primary">${{__cardName__}}</h6>
                                  </div>
                                  <div class="card-body">
                                      {% for progressbarName, progressbarItems in ${{__data__}} %}
                                      <h4 class="small font-weight-bold">{{ progressbarName }} <span
                                              class="float-right">{{ progressbarItems.value }}%</span></h4>
                                      <div class="progress mb-4">
                                          <div class="progress-bar {{ progressbarItems.color}}" role="progressbar" style="width: {{ progressbarItems.value }}%"
                                              aria-valuenow="{{ progressbarItems.value }}" aria-valuemin="{{ progressbarItems.value }}" aria-valuemax="100"></div>
                                      </div>
                                      {% endfor %}
                                  </div>
                              </div>
                          </div>
            """.replace("${{__cardName__}}", cardName).replace("${{__data__}}", card_dict["data"])
          elif card_dict["unit"] == "textcard":
            cardTags = """
                          <!-- Content Column -->
                          <div class="col-lg-6 mb-4">
  
                            <!-- ${{__cardName__}} Card Example -->
                            <div class="row">
                                {% for cardName, cardItems in ${{__data__}} %}
                                <div class="col-lg-6 mb-4">
                                    <div class="card {{ cardItems.bgcolor }} {{ cardItems.color }} shadow">
                                        <div class="card-body">
                                            {{ cardName }}
                                            <div class="{{ cardItems.color }}-50 small">{{ cardItems.value }}</div>
                                        </div>
                                    </div>
                                </div>
                                {% endfor %}
                            </div>
                         </div>
            """.replace("${{__cardName__}}", cardName).replace("${{__data__}}", card_dict["data"])
          
          elif card_dict["unit"] == "codeareas":
            gcForm = GcForm(themeName="default")
            
            #logDebug("form_dict:[{}]".format(form_dict))
            inputCount = 0
            
            formTags = """
                        <form action='./continuousInnovations' method='get' enctype="multipart/form-data" class="default">
                          <input type='hidden' name='atk' value='{{ gc.form.authenticityTokenId }}' />
                          <input type='hidden' name='iSL' value='y' />
            """
            formSubmitTags = ""
            codeAreaTags = ""
            codeButtonTags = ""
            codeAreaJsTags = ""
            for formName in form_dict.keys():
              
              if form_dict[formName]["display"]:
                gcForm.formCategory = form_dict[formName]["category"]
                formSubmitTags += gcForm.generateSubmitTags(submitItem_list= form_dict[formName]["submits"])
              
              for inputName in form_dict[formName]["inputs"].keys():
                formInput_dict = form_dict[formName]["inputs"][inputName]
                
                if form_dict[formName]["inputs"][inputName]["type"] in ["codeareas:text"] and form_dict[formName]["display"]:
                  formTags += """
                          <!-- start:"row" -->
                          <div class="row">
                            """ + gcForm.generateTextTags(inputName, formInput_dict, isDisplay=True) + """
                          </div>
                          <!-- end:"row" -->
                          """
                  
                elif form_dict[formName]["inputs"][inputName]["type"] in ["codeareas:select"] and form_dict[formName]["display"]:
                  formTags += """
                          <!-- start:"row" -->
                          <div class="row">
                            """ + gcForm.generateSelectTags(inputName, formInput_dict, isDisplay=True) + """
                          </div>
                          <!-- end:"row" -->
                          """
                  
                elif form_dict[formName]["inputs"][inputName]["type"] in ["codeareas"]:
                  inputCount += 1
            
                  codeId = "{}{}".format(inputName.strip()[0].lower(),inputName.strip().replace(" ","")[1:])
                  
                  codeAreaTags += """
                          <!-- Tab content: ${{__inputName__}} -->
                              <!-- Code Area Example -->
                              <div id="${{__cardId__}}:${{__codeId__}}" class="tabcontent">
                                <div class="table-responsive">
                                  <div id="${{__cardId__}}:${{__codeId__}}CodeArea">
                                    <textarea style="display:inline"
                                        id="${{__codeId__}}" name="${{__codeId__}}" ${{__rows__}} ${{__cols__}}
                                        placeholder="${{__input_placeHolder__}}"
                                        ></textarea>
                                  </div>
                                </div>
                              </div>
                          <!-- end:Tab content: ${{__inputName__}}  -->
                      """.replace("${{__cardId__}}", cardId).replace("${{__width__}}", "{}".format(int(width))).replace("${{__codeId__}}", codeId).replace("${{__inputName__}}", inputName).replace("${{__input_placeHolder__}}", formInput_dict["placeholder"])
            
            
            
                  codeButtonTags += """
                                        <button class="tablinks" onclick="codeArea(event, '${{__cardId__}}:${{__codeId__}}')" align="center">${{__inputName__}}</button>
                  """.replace("${{__cardId__}}", cardId).replace("${{__codeId__}}", codeId).replace("${{__inputName__}}", inputName)
                
                  codeAreaJsTags += """
    // Call the dataTables jQuery plugin
    $(document).ready(function() {
      $('#${{__cardId__}}:${{__codeId__}}CodeArea').DataTable();
    });
    """.replace("${{__cardId__}}", cardId).replace("${{__codeId__}}", codeId)
            
            formSubmitTags += """      
                        </form>
            """
                                
            cardTags = """
                    <!-- Code Areas Tab Begin: ${{__cardName__}} -->
                    
                    ${{__formTags__}}
                    
                    <div class="col-lg-${{__width__}} mb-4">
                        <!-- ${{__cardName__}} Textarea Card -->
                        
                        
                        <div class="card shadow mb-4">

                            <!-- Tab links -->
                            <div class="row">
                              <div class="tab" align="center">
                                  <table width="100%">
                                    <tr align="center">
                                      <td>
                                        ${{__codeButtonTags__}}
                                      </td>
                                    </tr>
                                  </table>
                              </div>
                          
                            </div>
                            <div class="row">
                              <div class="col-lg-${{__width__}}">
                                <div class="form-group">
                                  ${{__codeAreaTags__}}
                                </div>
                              </div>
                            </div>

                        </div>
                    </div>
                        
                    ${{__formSubmitTags__}}

                    <!-- Code Areas Tab End: ${{__cardName__}} -->
            """.replace("${{__cardName__}}", cardName).replace("${{__cardId__}}", cardId).replace("${{__formTags__}}", formTags).replace("${{__formSubmitTags__}}", formSubmitTags).replace("${{__codeAreaTags__}}", codeAreaTags).replace("${{__codeButtonTags__}}", codeButtonTags).replace("${{__width__}}", width)
            
            self.cardJsTags += """    
    <script>
    """+codeAreaJsTags+"""
    </script>
    
    <script>
    function codeArea(event, apiName) {
      var i, tabcontent, tablinks;
      tabcontent = document.getElementsByClassName("tabcontent");
      for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
      }
      tablinks = document.getElementsByClassName("tablinks");
      for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
      }
      document.getElementById(apiName).style.display = "block";
      event.currentTarget.className += " active";
    }
  </script>
  """.replace("${{__cardId__}}", cardId).replace("${{__data__}}", card_dict["data"])

          elif card_dict["unit"] == "tables":
            tableTags = """
                      {% for apiName, apiResultItems in ${{__data__}} %}
                        {% if apiName == "_summary" %}
                          <!-- Tab content: "{{ apiName }}"
                              <!-- DataTales Example -->
                              <div id="{{ apiName }}" class="tabcontent card shadow mb-4">
                                  <div class="card-header py-3">
                                      <h6 class="m-0 font-weight-bold text-primary">
                                        {{ apiName }}
                                      </h6>
                                  </div>
                                  <div class="card-body">
                                      <div class="table-responsive">
                                        {{ apiResultItems.results | safe }}
                                      </div>
                                  </div>
                              </div>
                              
                        {% else %}
                          <!-- Tab content: "{{ apiName }}" -->
                              <!-- DataTales Example -->
                              <div id="${{__cardId__}}:{{ apiName }}" class="tabcontent card shadow col-lg-${{__width__}} mb-4">
                                  <div class="card-header py-3">
                                      <h6 class="m-0 font-weight-bold text-primary">
                                        {{ apiName }}
                                        [ {% if apiResultItems and apiResultItems.file %}
                                            <a href="/download?atk={{ gc.form.authenticityTokenId }}&iSL=y&filename={{ apiResultItems.file }}">csv</a>
                                          {% else %}
                                            no csv
                                          {% endif %}
                                        ]
                                      </h6>
                                  </div>
                                  <div class="card-body">
                                      <div class="table-responsive">
                                        <table class="table table-bordered" id="${{__cardId__}}:{{ apiName }}Table" width="100%" cellspacing="0">
                                          <thead>
                                            <tr>
                                              {% for label in apiResultItems.labels %}
                                                <th>{{ label }}</th>
                                              {% endfor %}
                                            </tr>
                                          </thead>
                                          <tfoot>
                                            <tr>
                                              {% for label in apiResultItems.labels %}
                                                <th>{{ label }}</th>
                                              {% endfor %}
                                            </tr>
                                          </tfoot>
                                          
                                          <tbody>
                                            {% for resultItems in apiResultItems.data %}
                                                <tr>
                                                    {% for resultItemValue in resultItems %}
                                                      {% if resultItemValue | isHtmlTag %}
                                                        <td>{{ resultItemValue | htmlTag | safe }} </td>
                                                      {% else %}
                                                        <td>{{ resultItemValue }}</td>
                                                      {% endif %}
                                                    {% endfor %}
                                                </tr>
                                            {% endfor %}
                                          </tbody>
                                          
                                        </table>
                                      </div>
                                  </div>
                              </div>
                          <!-- end:Tab content: "{{ apiName }}" -->
                        {% endif %}
                      {% endfor %}
                      """.replace("${{__cardId__}}", cardId).replace("${{__width__}}", "{}".format(int(width)-1))
            
            cardTags = """
                    <!-- Tab Begin: ${{__cardName__}} -->
                    <div class="col-lg-${{__width__}} mb-4">
                        <!-- ${{__cardName__}} Textarea Card -->
                        <div class="card shadow mb-4">

                            <!-- Tab links -->
                            <div class="row">
                              <div class="tab" align="center">
                                  <table width="100%">
                                    <tr align="center">
                                      <td>
                                      {% for apiName, apiResultItems in ${{__data__}} %}
                                        <button class="tablinks" onclick="apiResult(event, '${{__cardId__}}:{{ apiName }}')" align="center">{{ apiName }} ({{ apiResultItems.count }})</button>
                                      {% endfor %}
                                      </td>
                                    </tr>
                                  </table>
                              </div>
                          
                            </div>
                            <div class="row">
                            
                              ${{__tableTags__}}
        
                            </div>

                        </div>
                    </div>
                    
                    <!-- Tab End: ${{__cardName__}} -->
            """.replace("${{__cardName__}}", cardName).replace("${{__cardId__}}", cardId).replace("${{__tableTags__}}", tableTags).replace("${{__data__}}", card_dict["data"]).replace("${{__width__}}", width)
            
            self.cardJsTags += """
    {% for apiName, apiResultItems in ${{__data__}} %}        
    <script>
    // Call the dataTables jQuery plugin
    $(document).ready(function() {
      $('#${{__cardId__}}:{{ apiName }}Table').DataTable();
    });
    </script>
    {% endfor %}
    
    <script>
    function apiResult(event, apiName) {
      var i, tabcontent, tablinks;
      tabcontent = document.getElementsByClassName("tabcontent");
      for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
      }
      tablinks = document.getElementsByClassName("tablinks");
      for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
      }
      document.getElementById(apiName).style.display = "block";
      event.currentTarget.className += " active";
    }
  </script>
  """.replace("${{__cardId__}}", cardId).replace("${{__data__}}", card_dict["data"])

        elif  card_dict["type"] in ["textarea"]:
          cardTags = """ 
                        <!-- Content Column -->
                        <div class="col-lg-${{__width__}} mb-4">
                            <!-- ${{__cardName__}} Textarea Card -->
                            <div class="card shadow mb-4">
                                <div class="card-header py-3">
                                    <h6 class="m-0 font-weight-bold text-primary">${{__cardName__}}</h6>
                                </div>
                                <div class="card-body">
                                    ${{__data__}}
                                </div>
                            </div>
                        </div>
          """.replace("${{__cardName__}}", cardName).replace("${{__data__}}", card_dict["data"]).replace("${{__width__}}", width)
        
        elif  card_dict["type"] in ["form"]:
          cardTags = """ 
                    <!-- ${{__cardName__}}: Tales Example -->
                    <div class="card col-lg-${{__width__}} shadow mb-4">
                        <div class="card-header py-3">
                            <h6 class="m-0 font-weight-bold text-primary">${{__cardName__}}</h6>
                        </div>
                        <div class="card-body">
                            ${{__data__}}
                        </div>
                    </div>
          """.replace("${{__cardName__}}", cardName).replace("${{__data__}}", "${{__form_"+card_dict["data"]+"__}}").replace("${{__width__}}", width)
          
        elif  card_dict["type"] in ["profile-form"]:
          try:
            selectProfileItemTags = "                                              \n"
            selectAccountIdItemTags = "                                              \n"
            
            profileTemplateNames = "Profile Template Names"
            profileTemplateId = "\"profileTemplateNames\""
            
            profileName = "Profile Names"
            profileId = "\"profileNames\""
            
            serviceName = "Service Names"
            serviceId = "\"serviceNames\""
            
            accountName = "Account Ids"
            accountId = "\"accountIds\""
            
            regionCode = "Region Codes"
            regionId = "\"regionCodes\""
            cardTags = """ 
                      <!-- Begin: """ + cardName + """: profile form -->
                      {% if gc.profileSelect %}
                        <div class="card col-lg-12 shadow mb-4">
                            <div class="card-header py-3">
                                <h6 class="m-0 font-weight-bold text-primary">""" + cardName + """</h6>
                            </div>
                            <div class="card-body">
                            
                            {% if gc.rulePath != "" %}
                              <form action="/{{ gc.ruleName }}/{{ gc.rulePath }}" method="get" class="default">
                            {% else %}
                              <form action="/{{ gc.ruleName }}" method="get" class="default">
                            {% endif %}
                            
                            <input type='hidden' name='atk' value='{{ gc.form.authenticityTokenId | safe }}'>
                            <input type='hidden' name='iSL' value='y' />
                        
                            <!-- start:"row" -->
                          
                            <div class="row">
                              {% if gc.profiles.templateNames %}
                                <div class="col-lg-3">
                                  <div class="form-group">
                                    """ + profileTemplateNames + """
                                    <select class="form-control" style="display:inline" name="""+profileTemplateId+""" id="""+profileTemplateId+""" multiple>
                                      <option value="">-</option>
                                      {{ gc.profileSelect.profileTemplates | safe }}
                                      
                                    </select>
                                  </div>
                                </div>
                                
                                <div class="col-lg-3">
                                  <div class="form-group">
                                    """ + profileName + """
                                    <select class="form-control" style="display:inline" name="""+profileId+""" id="""+profileId+""" multiple>
                                      <option value="">-</option>
                                      {{ gc.profileSelect.profileNames | safe }}
                                      
                                    </select>
                                  </div>
                                </div>
                                
                                <div class="col-lg-2">
                                  <div class="form-group">
                                    """ + serviceName + """
                                    <select class="form-control" style="display:inline" name="""+serviceId+""" id="""+serviceId+""" multiple>
                                      <option value="">-</option>
                                      {{ gc.profileSelect.serviceNames | safe }}
                                      
                                    </select>
                                  </div>
                                </div>
  
                                
                                <div class="col-lg-5">
                                  <div class="form-group">
                                    """ + accountName + """
                                    <select class="form-control" style="display:inline" name="""+accountId+""" id="""+accountId+""" multiple>
                                      <option value="">-</option>
                                      {{ gc.profileSelect.accountIds | safe }}
                                      
                                    </select>
                                  </div>
                                </div>
  
                                
                                <div class="col-lg-2">
                                  <div class="form-group">
                                    """ + regionCode + """
                                    <select class="form-control" style="display:inline" name="""+regionId+""" id="""+regionId+""" multiple>
                                      <option value="">-</option>
                                      {{ gc.profileSelect.regionCodes | safe }}
                                      
                                    </select>
                                  </div>
                                </div>
                              
                              {% else %}
                                <div class="col-lg-2">
                                  <div class="form-group">
                                    """ + profileName + """
                                    <select class="form-control" style="display:inline" name="""+profileId+""" id="""+profileId+""" multiple>
                                      <option value="">-</option>
                                      {{ gc.profileSelect.profileNames | safe }}
                                      
                                    </select>
                                  </div>
                                </div>
                                
                                <div class="col-lg-2">
                                  <div class="form-group">
                                    """ + serviceName + """
                                    <select class="form-control" style="display:inline" name="""+serviceId+""" id="""+serviceId+""" multiple>
                                      <option value="">-</option>
                                      {{ gc.profileSelect.serviceNames | safe }}
                                      
                                    </select>
                                  </div>
                                </div>
  
                                
                                <div class="col-lg-3">
                                  <div class="form-group">
                                    """ + accountName + """
                                    <select class="form-control" style="display:inline" name="""+accountId+""" id="""+accountId+""" multiple>
                                      <option value="">-</option>
                                      {{ gc.profileSelect.accountIds | safe }}
                                      
                                    </select>
                                  </div>
                                </div>
  
                                
                                <div class="col-lg-2">
                                  <div class="form-group">
                                    """ + regionCode + """
                                    <select class="form-control" style="display:inline" name="""+regionId+""" id="""+regionId+""" multiple>
                                      <option value="">-</option>
                                      {{ gc.profileSelect.regionCodes | safe }}
                                      
                                    </select>
                                  </div>
                                </div>
                            
                            {% endif %}
                                
                            </div>
                            <!-- end:"row" -->
                            
                            <!-- start:"row" -->
                            <div class="row">
                              <div class="col-lg-12">
                                <div class="form-group">
                                  <button class="btn btn-lg btn-primary btn-block" type="submit">Submit</button>
                                </div>
                              </div>
                            </div>
                            <!-- end:"row" -->
                            
                          </form>
  
                            </div>
                        </div>
                      
                      {% endif %}
                      <!-- End: """ + cardName + """: Tales Example -->
            """
          except:
            logException("unable to generate 'profile-form'")
            time.sleep(60)
            
        elif  card_dict["type"] in ["table"]:
          cardTags = """ 
                    <!-- ${{__cardName__}}: Tales Example -->
                    <div class="card col-lg-${{__width__}} shadow mb-4">
                        <div class="card-header py-3">
                            <h6 class="m-0 font-weight-bold text-primary">${{__cardName__}} ({{ ${{__count__}} }})
                            [ {% if ${{__fileTag__}} %}
                                <a href="/download?atk={{ gc.form.authenticityTokenId }}&iSL=y&filename={{ ${{__fileTag__}} }}">csv</a>
                              {% else %}
                                  no csv
                              {% endif %}
                            ]</h6>
                        </div>
                        <div class="card-body">
                            <div class="table-responsive">
                                <table class="table table-bordered" id="${{__tableId__}}" width="100%" cellspacing="0">
                                    <thead>
                                        <tr>
                                            {% for label in ${{__labels__}} %}
                                            <th>{{ label }}</th>
                                            {% endfor %}
                                        </tr>
                                    </thead>
                                    <tfoot>
                                        <tr>
                                            {% for label in ${{__labels__}} %}
                                            <th>{{ label }}</th>
                                            {% endfor %}
                                        </tr>
                                    </tfoot>
                                    <tbody>
                                        {% for lineItems in ${{__data__}} %}
                                        <tr>
                                            {% for data in lineItems %}
                                            <td>{{ data }}</td>
                                            {% endfor %}
                                        </tr>
                                        {% endfor %}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
          """.replace("${{__cardName__}}", cardName).replace("${{__tableId__}}", cardId).replace("${{__fileTag__}}", card_dict["file"]).replace("${{__labels__}}", card_dict["labels"]).replace("${{__data__}}", card_dict["data"]).replace("${{__width__}}", width).replace("${{__count__}}", card_dict["count"])
          
          self.cardJsTags = """
<script>
// Call the dataTables jQuery plugin
$(document).ready(function() {
  $('#${{__tableId__}}').DataTable();
});
</script>
""".replace("${{__tableId__}}", cardId)
        elif card_dict["type"] in ["chart"]:
          cardTags = self.gcChart.getChartTags(cardName, card_dict)
        
        elif card_dict["type"] in ["chartV2"]:
          try:
            chartId = "{}{}".format(cardName[0].lower(), cardName[1:].replace(" ", ""))
          except:
            logException("unable to set chartId with cardName:[{}]".format(cardName))
            chartId = cardName.lower()
            
          cardTags = """
                  {% if gc.outputs.charts %}
                    {% if gc.outputs.charts.${{__chartId__}} %}
                      {{ gc.outputs.charts.${{__chartId__}} | safe }}
                    {% endif %}
                  {% endif %}
          """.replace("${{__chartId__}}", chartId)
        
        else:
          logError("'type' is not supported:[{}]".format(card_dict))
          cardTags = ""
        
        cardTags = cardTags.replace("${{__dropdownItems__}}", dropDownItemTags).replace("${{__iconTags__}}", iconTags)
        
        
      else:
        logError("'type' is not provided:[{}]".format(card_dict))
        cardTags = ""
      
        
      return cardTags
    
    else:
      return ""
    
  def getJsTags(self):
    return self.cardJsTags + self.gcChart.getJsScript()