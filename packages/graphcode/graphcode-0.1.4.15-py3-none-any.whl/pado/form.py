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

from pado.theme import GcTheme

from html import unescape

class GcForm():
  def __init__(self, themeName = "default"):
    self.themeName = themeName
    
    self.gcTheme = GcTheme(themeName = themeName)
  
  def generateForms(self, form_dict):
    #logDebug("form_dict:[{}]".format(form_dict))
    thiForm_dict = {}
    
    for formName in form_dict.keys():
      #thisFormTags = formTheme_dict["begin"].replace("${{__form_target__}}", form_dict[formName]["target"]).replace("${{__form_method__}}", form_dict[formName]["method"])
      self.formCategory = form_dict[formName]["category"]
      thisFormTags = self.gcTheme.getFormTags(category= self.formCategory,tagName="begin").replace("${{__form_target__}}", form_dict[formName]["target"]).replace("${{__form_method__}}", form_dict[formName]["method"])
      
      if "columns" in form_dict[formName].keys():
        columnNumber = form_dict[formName]["columns"]
      else:
        columnNumber = 1 
      
      inputCount = 0
      thisFormTags += """
                              <!-- start:"row" -->
                              <div class="row">
      """
      for inputName in form_dict[formName]["inputs"].keys():
        if form_dict[formName]["inputs"][inputName]["type"] == "object":
          thisFormTags += self.generateObjectFormTags(objectName = inputName, 
                                                      objectForm_dict = form_dict[formName]["inputs"][inputName]["objects"], 
                                                      objectCount = form_dict[formName]["inputs"][inputName]["count"], 
                                                      start = 0)
          
        elif form_dict[formName]["inputs"][inputName]["type"] == "file":
          
          thisFormTags += self.generateFileTags(inputName = inputName, formInput_dict = form_dict[formName]["inputs"][inputName], isDisplay= form_dict[formName]["display"])
        
        elif form_dict[formName]["inputs"][inputName]["type"] == "textarea":
          
          thisFormTags += self.generateTextAreaTags(inputName = inputName, formInput_dict = form_dict[formName]["inputs"][inputName], isDisplay= form_dict[formName]["display"])
          
        elif form_dict[formName]["inputs"][inputName]["type"] == "codearea":
          
          if "display" in form_dict[formName]["inputs"][inputName].keys() and form_dict[formName]["inputs"][inputName]["display"] == False:
            continue
          else:
            thisFormTags += self.generateCodeAreaTags(inputName = inputName, formInput_dict = form_dict[formName]["inputs"][inputName])
          
        elif form_dict[formName]["inputs"][inputName]["type"] == "text":
          thisFormTags += self.generateTextTags(inputName = inputName, formInput_dict = form_dict[formName]["inputs"][inputName], isDisplay= form_dict[formName]["display"])
        
        elif form_dict[formName]["inputs"][inputName]["type"] == "password":
          thisFormTags += self.generateTextTags(inputName = inputName, formInput_dict = form_dict[formName]["inputs"][inputName], isDisplay= form_dict[formName]["display"])
        
        elif form_dict[formName]["inputs"][inputName]["type"] == "select":
          thisFormTags += self.generateSelectTags(inputName = inputName, formInput_dict = form_dict[formName]["inputs"][inputName], isDisplay= form_dict[formName]["display"])
        
        elif form_dict[formName]["inputs"][inputName]["type"] == "multipleselects":
          thisFormTags += self.generateMultiSelectTags(inputName = inputName, formInput_dict = form_dict[formName]["inputs"][inputName], isDisplay= form_dict[formName]["display"])
        
        elif form_dict[formName]["inputs"][inputName]["type"] == "profile":
          thisFormTags += self.generateProfileTags(inputName = inputName, formInput_dict = form_dict[formName]["inputs"][inputName], isDisplay= form_dict[formName]["display"])
        
        else:
          #logWarn("type:[{}] isn't supported at inputName:[{}]".format(form_dict[formName]["inputs"][inputName]["type"], inputName))
          pass
        
        inputCount += 1
        if inputCount % columnNumber == 0:
          thisFormTags += """
                              </div>
                              <!-- end:"row" -->
                              
                              <!-- start:"row" -->
                              <div class="row">
          """
      
      thisFormTags += """
                              </div>
                              <!-- end:"row" -->
                              
                              <!-- start:"row" -->
                              <div class="row">
      """
               
      thisFormTags += self.generateSubmitTags(submitItem_list= form_dict[formName]["submits"])
         
      thisFormTags += self.gcTheme.getFormTags(category= self.formCategory,tagName="end")
      
      thiForm_dict[formName] = thisFormTags
      
    #logDebug("thiForm_dict:[{}]".format(thiForm_dict))
    return thiForm_dict
  
  def generateFormJsTags(self, form_dict):
    #logDebug("form_dict:[{}]".format(form_dict))
    thisFormJsTags = ""
    
    inputCount = 0
    for formName in form_dict.keys():
      
      for inputName in form_dict[formName]["inputs"].keys():
        formInput_dict = form_dict[formName]["inputs"][inputName]
        
        if form_dict[formName]["inputs"][inputName]["type"] in ["codearea", "codeareas"]:
          inputCount += 1
          
          thisFormJsTags += """    
  var editor = CodeMirror.fromTextArea(document.getElementById("${{__input_id__}}"), {
    ${{__codeValue__}}
    mode: {${{__modeNmae__}}
        ${{__modeVersion__}}
        ${{__singleLineStringErrors__}}},
      ${{__lineNumbers__}}
      ${{__indentUnit__}}
      ${{__matchBrackets__}}
    });
          """.replace("${{__inputName__}}", inputName).replace("${{__input_id__}}", "{}{}".format(inputName.strip()[0].lower(),inputName.strip().replace(" ","")[1:]))
          
          
          if "value" in formInput_dict.keys() and isinstance(formInput_dict["value"], str) and len(formInput_dict["value"]) > 0:
            thisFormJsTags = thisFormJsTags.replace("${{__codeValue__}}", "value: \"{}\",".format(formInput_dict["value"]))
          else:
            thisFormJsTags = thisFormJsTags.replace("${{__codeValue__}}", "")
            
          if "name" in formInput_dict.keys() and isinstance(formInput_dict["name"], str) and len(formInput_dict["name"]) > 0:
            thisFormJsTags = thisFormJsTags.replace("${{__modeNmae__}}", "name: \"{}\",".format(formInput_dict["name"]))
          else:
            thisFormJsTags = thisFormJsTags.replace("${{__modeNmae__}}", "name: \"{}\",".format("text"))
            
          if "version" in formInput_dict.keys():
            thisFormJsTags = thisFormJsTags.replace("${{__modeVersion__}}", "version: {},".format(formInput_dict["version"]))
            
          if "singleLineStringErrors" in formInput_dict.keys():
            if formInput_dict["singleLineStringErrors"] in [True]:
              thisFormJsTags = thisFormJsTags.replace("${{__singleLineStringErrors__}}", "singleLineStringErrors: true")
            else:
              thisFormJsTags = thisFormJsTags.replace("${{__singleLineStringErrors__}}", "singleLineStringErrors: false")
          else:
            thisFormJsTags = thisFormJsTags.replace("${{__singleLineStringErrors__}}", "singleLineStringErrors: true")
            
          if "singleLineStringErrors" in formInput_dict.keys():
            thisFormJsTags = thisFormJsTags.replace("${{__singleLineStringErrors__}}", "singleLineStringErrors: {},".format(formInput_dict["version"]))
            
          if "lineNumbers" in formInput_dict.keys():
            if formInput_dict["lineNumbers"] in [True]:
              thisFormJsTags = thisFormJsTags.replace("${{__lineNumbers__}}", "lineNumbers: true,")
            else:
              thisFormJsTags = thisFormJsTags.replace("${{__lineNumbers__}}", "lineNumbers: false,")
          else:
            thisFormJsTags = thisFormJsTags.replace("${{__lineNumbers__}}", "lineNumbers: true,")
            
          if "indentUnit" in formInput_dict.keys() and isinstance(formInput_dict["indentUnit"], int) and formInput_dict["indentUnit"] > 0:
            thisFormJsTags = thisFormJsTags.replace("${{__indentUnit__}}", "indentUnit: {},".format(formInput_dict["indentUnit"]))
          else:
            thisFormJsTags = thisFormJsTags.replace("${{__indentUnit__}}", "indentUnit: 2,")
            
          if "matchBrackets" in formInput_dict.keys():
            if formInput_dict["matchBrackets"] in [True]:
              thisFormJsTags = thisFormJsTags.replace("${{__matchBrackets__}}", "matchBrackets: true,")
            else:
              thisFormJsTags = thisFormJsTags.replace("${{__matchBrackets__}}", "matchBrackets: false,")
          else:
            thisFormJsTags = thisFormJsTags.replace("${{__matchBrackets__}}", "matchBrackets: true,")
            
    if inputCount > 0:
      thisFormJsTags = """
  <!-- start:"formJsTags" -->
  <script>
  """ + thisFormJsTags + """
  </script>
  <!-- end:"formJsTags" -->
      """
    #logDebug("thiForm_dict:[{}]".format(thiForm_dict))
    return thisFormJsTags
  
  def generateSubmitTags(self, submitItem_list):
    thisFormTags = ""
    for submitItems in submitItem_list:
      if len(submitItems.keys()) == 0:
        thisFormTags += """
                              <hr>
        """
        
      elif "target" in submitItems.keys():
        try:
          submitId = "{}{}".format(submitItems["name"][0].lower(), submitItems["name"][1:].replace(" ",""))
        except:
          logException("unable to get submitId with submitName:[{}]".format(submitItems["name"]))
        thisFormTags += self.gcTheme.getFormTags(category= self.formCategory, tagName="button").replace("${{__submitId__}}", submitId).replace("${{__submitName__}}", submitItems["name"])
        
      else:
        thisFormTags += self.gcTheme.getFormTags(category= self.formCategory,tagName="link").replace("${{__form_target__}}", submitItems["link"]).replace("${{__submitName__}}", submitItems["name"])
  
      if "size" in submitItems.keys() and submitItems["size"] > 0:
        thisFormTags = thisFormTags.replace("${{__size__}}", "{}".format(submitItems["size"]))
      else:
        thisFormTags = thisFormTags.replace("${{__size__}}", "3")
    
    return thisFormTags
  
  def generateObjectFormTags(self, objectName, objectForm_dict, objectCount, start = 0, formValue_dict = {}):
    logDebug("objectName:[{}], objectForm_dict:[{}], objectCount:[{}], start:[{}]".format(objectName, objectForm_dict, objectCount, start))
    thisFormTags = ""
    
    
    inputId = "{}{}".format(objectName.strip()[0].lower(),objectName.strip().replace(" ","")[1:])
    if start == 0:
      thisFormTags += """
                              </div>
                              <!-- end:"row" -->
                              
                              <!-- start:"row" -->
                              <div class="row">
      
                                        <div class="col-lg-${{__size__}}">
                                          <div class="form-group">
                                            ${{__objectName__}}
                                              <!-- hidden objectCount -->
                                              {% if gc and gc.form and gc.form.__objectCount__ and  gc.form.__objectCount__.${{__inputId__}} and gc.form.__objectCount__.${{__inputId__}} > ${{__objectCount__}} %} 
                                                <input type='hidden' name='objectCount' value='{{ gc.form.__objectCount__.${{__inputId__}} }}' />
                                              {% else %}
                                                <input type='hidden' name='objectCount' value='${{__objectCount__}}' />
                                              {% endif %}
                                          </div>
                                        </div>
        """.replace("${{__objectName__}}", objectName).replace("${{__inputId__}}", inputId).replace("${{__objectCount__}}", "{}".format(objectCount))
        
      thisFormTags += """
                              </div>
                              <!-- end:"row" -->
                              
                              <!-- start:"row" -->
                              <div class="row">
      """
    
    subFormTags = ""
    for count in range(start, objectCount):
      for objectName in objectForm_dict.keys():
        inputItem_dict = objectForm_dict[objectName]
        subInputId = "{}{}_{}".format(objectName.strip()[0].lower(),objectName.strip().replace(" ","")[1:], count)
        
        if subInputId in formValue_dict.keys():
          subFormTags += """
                                      <div class="col-lg-${{__size__}}">
                                        <div class="form-group">
                                            <input type="${{__type__}}" class="form-control"
                                                id="${{__input_id__}}" name="${{__input_id__}}" value="${{__formValue__}}"
                                                placeholder="${{__input_placeHolder__}}:${{__count__}}" ${{__autocomplete__}} ${{__required__}}>
                                        </div>
                                    </div>
          """.replace("${{__type__}}", inputItem_dict["type"]).replace("${{__input_id__}}", subInputId).replace("${{__count__}}", "{}".format(count)).replace("${{__input_placeHolder__}}", inputItem_dict["placeholder"]).replace("${{__formValue__}}", formValue_dict[subInputId].replace('"',"&#34;"))
          #logDebug("#=====>formValue_dict['{}]']:{}".format(subInputId, formValue_dict[subInputId]))
          
          
            
        
        elif start == 0:
          subFormTags += """
                                      <div class="col-lg-${{__size__}}">
                                        <div class="form-group">
                                            <input type="${{__type__}}" class="form-control"
                                                id="${{__input_id__}}" name="${{__input_id__}}" value="{{ gc.form.${{__input_id__}} }}"
                                                placeholder="${{__input_placeHolder__}}:${{__count__}}" ${{__autocomplete__}} ${{__required__}}>
                                        </div>
                                    </div>
          """.replace("${{__type__}}", inputItem_dict["type"]).replace("${{__input_id__}}", subInputId).replace("${{__count__}}", "{}".format(count)).replace("${{__input_placeHolder__}}", inputItem_dict["placeholder"])
        else:
          subFormTags += """
                                      <div class="col-lg-${{__size__}}">
                                        <div class="form-group">
                                            <input type="${{__type__}}" class="form-control"
                                                id="${{__input_id__}}" name="${{__input_id__}}" value=""
                                                placeholder="${{__input_placeHolder__}}:${{__count__}}" ${{__autocomplete__}} ${{__required__}}>
                                        </div>
                                    </div>
          """.replace("${{__type__}}", inputItem_dict["type"]).replace("${{__input_id__}}", subInputId).replace("${{__count__}}", "{}".format(count)).replace("${{__input_placeHolder__}}", inputItem_dict["placeholder"])
           
        if "size" in inputItem_dict.keys() and inputItem_dict["size"] > 0:
          subFormTags = subFormTags.replace("${{__size__}}", "{}".format(inputItem_dict["size"]))
        else:
          subFormTags = subFormTags.replace("${{__size__}}", "3")
        
        if "required" in inputItem_dict.keys() and inputItem_dict["required"]:
          subFormTags = subFormTags.replace("${{__required__}}", "required")
        else:
          subFormTags = subFormTags.replace("${{__required__}}","")
    
        
        if "autocomplete" in inputItem_dict.keys() and inputItem_dict["autocomplete"] == False:
          subFormTags = subFormTags.replace("${{__autocomplete__}}","autocomplete=\"off\"")
        else:
          subFormTags = subFormTags.replace("${{__autocomplete__}}","")
          
            
            
    if start == 0:
      logDebug("----------------generating the default object's inputs----------")
      thisFormTags += subFormTags + """
                                      <!-- Begin: additional objects: ${{__inputId__}} -->
                                      {% if gc and gc.form and gc.form.__objectCount__ and  gc.form.__objectCount__.${{__inputId__}} and gc.form.__objectCount__.${{__inputId__}} > ${{__objectCount__}} %} 
                                        {% if gc and gc.form and gc.form.__objects__ and gc.form.__objects__.${{__inputId__}} %} 
                                        
                                          {{ gc.form.__objects__.${{__inputId__}} | safe }}
                                          
                                        {% endif %}
                                      {% endif %}
                                      </div>
                                      <!-- end:"row" -->
                                      
                                      <!-- start:"row" -->
                                      <div class="row">
                                      <!-- End: additional objects: ${{__inputId__}} -->
                                      
      """.replace("${{__inputId__}}", inputId).replace("${{__objectCount__}}", "{}".format(objectCount))
    
    else:
      
      logDebug("----------------generating the additional object's inputs:[len:{}]----------".format(len(subFormTags.split("\n"))))
      thisFormTags += subFormTags.replace("${{__inputId__}}", inputId).replace("${{__objectCount__}}", "{}".format(objectCount))
      
    return thisFormTags
  
  def generateFileTags(self, inputName, formInput_dict, isDisplay = True):
    thisFormTags = """
                              </div>
                              <!-- end:"row" -->
                              
                              <!-- start:"row" -->
                              <div class="row">
    """
    
    thisFormTags += """
                                  <div class="col-lg-${{__size__}}">
                                    <div class="form-group">
                                      <label for="${{__input_id__}}FileFor">${{__inputPlaceholder__}}</label>
                                      
                                      <input style="display:inline" id="${{__input_id__}}FileLabel" name="${{__input_id__}}" type="file" ${{__required__}}>
                                    </div>
                                  </div>
                                  

    """.replace("${{__inputName__}}", inputName).replace("${{__input_id__}}", "{}{}".format(inputName.strip()[0].lower(),inputName.strip().replace(" ","")[1:])).replace("${{__inputPlaceholder__}}", formInput_dict["placeholder"])
    
    if "size" in formInput_dict.keys() and formInput_dict["size"] > 0:
      thisFormTags = thisFormTags.replace("${{__size__}}", "{}".format(formInput_dict["size"]))
    else:
      thisFormTags = thisFormTags.replace("${{__size__}}", "3")
     
    if "required" in formInput_dict.keys() and formInput_dict["required"]:
      thisFormTags = thisFormTags.replace("${{__required__}}", "required=\"required\"")
    else:
      thisFormTags = thisFormTags.replace("${{__required__}}","")
      
    thisFormTags += """
                              </div>
                              <!-- end:"row" -->
                              
                              <!-- start:"row" -->
                              <div class="row">
    """
    
    return thisFormTags
  
  def generateTextAreaTags(self, inputName, formInput_dict, isDisplay = True):
    thisFormTags = """
                              </div>
                              <!-- end:"row" -->
                              
                              <!-- start:"row" -->
                              <div class="row">
    """
    
    thisFormTags += """
                                  <div class="col-lg-${{__size__}}">
                                    <div class="form-group">
                                      ${{__inputName__}}
                                        <textarea style="display:inline" class="form-control"
                                            id="${{__input_id__}}" name="${{__input_id__}}" ${{__rows__}} ${{__cols__}}
                                            placeholder="${{__input_placeHolder__}}"  ${{__required__}} 
                                            >{{ gc.form.${{__input_id__}} }}</textarea>
                                    </div>
                                  </div>
    """.replace("${{__inputName__}}", inputName).replace("${{__input_id__}}", "{}{}".format(inputName.strip()[0].lower(),inputName.strip().replace(" ","")[1:])).replace("${{__input_placeHolder__}}", formInput_dict["placeholder"])
    
    if "size" in formInput_dict.keys() and formInput_dict["size"] > 0:
      thisFormTags = thisFormTags.replace("${{__size__}}", "{}".format(formInput_dict["size"]))
    else:
      thisFormTags = thisFormTags.replace("${{__size__}}", "3")
     
    if "rows" in formInput_dict.keys() and formInput_dict["rows"] > 0:
      thisFormTags = thisFormTags.replace("${{__rows__}}", "rows=\"{}\"".format(formInput_dict["rows"]))
    else:
      thisFormTags = thisFormTags.replace("${{__rows__}}", "")
     
    if "cols" in formInput_dict.keys() and formInput_dict["cols"] > 0:
      thisFormTags = thisFormTags.replace("${{__cols__}}", "cols=\"{}\"".format(formInput_dict["cols"]))
    else:
      thisFormTags = thisFormTags.replace("${{__cols__}}", "")
     
    if "required" in formInput_dict.keys() and formInput_dict["required"]:
      thisFormTags = thisFormTags.replace("${{__required__}}", "required=\"required\"")
    else:
      thisFormTags = thisFormTags.replace("${{__required__}}","")
      
    thisFormTags += """
                              </div>
                              <!-- end:"row" -->
                              
                              <!-- start:"row" -->
                              <div class="row">
    """
    
    return thisFormTags
  
  
  def generateCodeAreaTags(self, inputName, formInput_dict):
    thisFormTags = """
                              </div>
                              <!-- end:"row" -->
                              
                              <!-- start:"row" -->
                              <div class="row">
    """
    
    thisFormTags += """
                                  <div class="col-lg-${{__size__}}">
                                    <div class="form-group">
                                      ${{__inputName__}}
                                        <textarea style="display:inline" class="form-control"
                                            id="${{__input_id__}}" name="${{__input_id__}}" ${{__rows__}} ${{__cols__}}
                                            placeholder="${{__input_placeHolder__}}"  ${{__required__}} 
                                            >{{ gc.form.${{__input_id__}} }}</textarea>

                                    </div>

                                  </div>
    """.replace("${{__inputName__}}", inputName).replace("${{__input_id__}}", "{}{}".format(inputName.strip()[0].lower(),inputName.strip().replace(" ","")[1:])).replace("${{__input_placeHolder__}}", formInput_dict["placeholder"])
    
    if "size" in formInput_dict.keys() and formInput_dict["size"] > 0:
      thisFormTags = thisFormTags.replace("${{__size__}}", "{}".format(formInput_dict["size"]))
    else:
      thisFormTags = thisFormTags.replace("${{__size__}}", "3")
     
    if "rows" in formInput_dict.keys() and formInput_dict["rows"] > 0:
      thisFormTags = thisFormTags.replace("${{__rows__}}", "rows=\"{}\"".format(formInput_dict["rows"]))
    else:
      thisFormTags = thisFormTags.replace("${{__rows__}}", "")
     
    if "cols" in formInput_dict.keys() and formInput_dict["cols"] > 0:
      thisFormTags = thisFormTags.replace("${{__cols__}}", "cols=\"{}\"".format(formInput_dict["cols"]))
    else:
      thisFormTags = thisFormTags.replace("${{__cols__}}", "")
     
    if "required" in formInput_dict.keys() and formInput_dict["required"]:
      thisFormTags = thisFormTags.replace("${{__required__}}", "required=\"required\"")
    else:
      thisFormTags = thisFormTags.replace("${{__required__}}","")
      
    thisFormTags += """
                              </div>
                              <!-- end:"row" -->
                              
                              <!-- start:"row" -->
                              <div class="row">
    """
    
    return thisFormTags
  
  def generateTextTags(self, inputName, formInput_dict, isDisplay = True):
    
    thisFormTags = ""
    if isDisplay:
      if "align" in formInput_dict.keys() and formInput_dict["align"] == "center":
        thisFormTags += self.gcTheme.getFormTags(category= self.formCategory,tagName="center-display").replace("${{__inputName__}}", inputName).replace("${{__type__}}", formInput_dict["type"]).replace("${{__input_id__}}", "{}{}".format(inputName.strip()[0].lower(),inputName.strip().replace(" ","")[1:])).replace("${{__input_placeHolder__}}", formInput_dict["placeholder"])
      else:
        thisFormTags += self.gcTheme.getFormTags(category= self.formCategory,tagName="display").replace("${{__inputName__}}", inputName).replace("${{__type__}}", formInput_dict["type"]).replace("${{__input_id__}}", "{}{}".format(inputName.strip()[0].lower(),inputName.strip().replace(" ","")[1:])).replace("${{__input_placeHolder__}}", formInput_dict["placeholder"])
    else:
      thisFormTags += self.gcTheme.getFormTags(category= self.formCategory,tagName="nodisplay").replace("${{__type__}}", formInput_dict["type"]).replace("${{__input_id__}}", "{}{}".format(inputName.strip()[0].lower(),inputName.strip().replace(" ","")[1:])).replace("${{__input_placeHolder__}}", formInput_dict["placeholder"])
    
    if "size" in formInput_dict.keys() and formInput_dict["size"] > 0:
      thisFormTags = thisFormTags.replace("${{__size__}}", "{}".format(formInput_dict["size"]))
    else:
      thisFormTags = thisFormTags.replace("${{__size__}}", "3")
      
    if "required" in formInput_dict.keys() and formInput_dict["required"]:
      thisFormTags = thisFormTags.replace("${{__required__}}", "required")
    else:
      thisFormTags = thisFormTags.replace("${{__required__}}","")
      
    if "value" in formInput_dict.keys() and len(formInput_dict["value"]) > 0:
      thisFormTags = thisFormTags.replace("${{__value__}}", formInput_dict["value"])
    else:
      thisFormTags = thisFormTags.replace("${{__value__}}","")
    
    return thisFormTags
  
  
  def generateSelectTags(self, inputName, formInput_dict, isDisplay = True):
    if "default" in formInput_dict.keys():
      selectItemTags = "                                              <option value='{}'>{}</option>\n".format(formInput_dict["default"], formInput_dict["default"])
    else:
      selectItemTags = "                                              <option value=''>{}</option>\n".format(formInput_dict["placeholder"])
    
    try:
      if isinstance(formInput_dict["list"], list):
        for name in formInput_dict["list"]:
          selectItemTags += "                                              <option value=\"{}\">{}</option>\n".format(name, name)
      
      elif isinstance(formInput_dict["list"], str):
        
          selectItemTags += """                                          <!-- {{ ${{__input_list__}} }}-->      
                                            {% for optionName in ${{__input_list__}} %}
                                                <option value="{{optionName}}">{{optionName}}</option>
                                            {% endfor %}""".replace("${{__input_list__}}", formInput_dict["list"])
    except:
      raiseValueError(f"inputName:[{inputName}] list must be a list or a string")
      
    if isDisplay:
      thisFormTags ="""
                                          <div class="col-lg-${{__size__}}">
                                            <div class="form-group">
                                              ${{__inputName__}}
                                              <select class="form-control" style="display:inline" name="${{__input_id__}}" id="${{__input_id__}}">
                                                ${{__selectItemTags__}}
                                              </select>
                                            </div>
                                          </div>
      """.replace("${{__inputName__}}", inputName).replace("${{__input_id__}}", "{}{}".format(inputName.strip()[0].lower(),inputName.strip().replace(" ","")[1:])).replace("${{__selectItemTags__}}", selectItemTags)
    else:
      thisFormTags ="""
                                          <div class="col-lg-${{__size__}}">
                                            <div class="form-group">
                                              <select class="form-control" name="${{__input_id__}}" id="${{__input_id__}}">
                                                ${{__selectItemTags__}}
                                              </select>
                                            </div>
                                          </div>
      """.replace("${{__input_id__}}", "{}{}".format(inputName.strip()[0].lower(),inputName.strip().replace(" ","")[1:])).replace("${{__selectItemTags__}}", selectItemTags)
            
    if "size" in formInput_dict.keys() and formInput_dict["size"] > 0:
      thisFormTags = thisFormTags.replace("${{__size__}}", "{}".format(formInput_dict["size"]))
    else:
      thisFormTags = thisFormTags.replace("${{__size__}}", "3")
      
    if "required" in formInput_dict.keys() and formInput_dict["required"]:
      thisFormTags = thisFormTags.replace("${{__required__}}", "required")
    else:
      thisFormTags = thisFormTags.replace("${{__required__}}","")
    
    return thisFormTags
      
  def generateMultiSelectTags(self, inputName, formInput_dict, isDisplay = True):
    selectItemTags = "                                              <option value="">Choose a template to load</option>\n"
    for name in formInput_dict["list"]:
      selectItemTags += "                                              <option value=\"{}\">{}</option>\n".format(name, name)
    
    if isDisplay:
      thisFormTags ="""
                                          <div class="col-lg-${{__size__}}">
                                            <div class="form-group">
                                              ${{__inputName__}}
                                              <select class="form-control" style="display:inline" name="${{__input_id__}}" id="${{__input_id__}}">
                                                ${{__selectItemTags__}}
                                              </select>
                                            </div>
                                          </div>
      """.replace("${{__inputName__}}", inputName).replace("${{__input_id__}}", "{}{}".format(inputName.strip()[0].lower(),inputName.strip().replace(" ","")[1:])).replace("${{__selectItemTags__}}", selectItemTags)
    else:
      thisFormTags ="""
                                          <div class="col-lg-${{__size__}}">
                                            <div class="form-group">
                                              <select class="form-control" name="${{__input_id__}}" id="${{__input_id__}}">
                                                ${{__selectItemTags__}}
                                              </select>
                                            </div>
                                          </div>
      """.replace("${{__input_id__}}", "{}{}".format(inputName.strip()[0].lower(),inputName.strip().replace(" ","")[1:])).replace("${{__selectItemTags__}}", selectItemTags)
            
    if "size" in formInput_dict.keys() and formInput_dict["size"] > 0:
      thisFormTags = thisFormTags.replace("${{__size__}}", "{}".format(formInput_dict["size"]))
    else:
      thisFormTags = thisFormTags.replace("${{__size__}}", "3")
      
    if "required" in formInput_dict.keys() and formInput_dict["required"]:
      thisFormTags = thisFormTags.replace("${{__required__}}", "required")
    else:
      thisFormTags = thisFormTags.replace("${{__required__}}","")
    
    return thisFormTags
      
      
  def generateProfileTags(self, inputName, formInput_dict, isDisplay = True):
    try:
      thisFormTags = """
                          {% if gc.profileSelect %}
                          
                              </div>
                              <!-- end:"row" -->
                              
                              <!-- start:"row" -->
                              <div class="row">
                              
                              
                                {% if gc.profiles.templateNames and gc.profileSelect.profileTemplates %}
                                  <!-- Begin: Profile form -->
                                  <div class="col-lg-3">
                                    <div class="form-group">
                                      Profile Templates
                                      <select class="form-control" style="display:inline" name="profileTemplates" id="profileTemplates" multiple>
                                        <option value="">-</option>
                                        {{ gc.profileSelect.profileTemplates | safe }}
                                        
                                      </select>
                                    </div>
                                  </div>
                                  
                                  <div class="col-lg-2">
                                    <div class="form-group">
                                      Profile Names
                                      <select class="form-control" style="display:inline" name="profileNames" id="profileNames" multiple>
                                        <option value="">-</option>
                                        {{ gc.profileSelect.profileNames | safe }}
                                        
                                      </select>
                                    </div>
                                  </div>
                                  
                                  <div class="col-lg-2">
                                    <div class="form-group">
                                      Service Names
                                      <select class="form-control" style="display:inline" name="serviceNames" id="serviceNames" multiple>
                                        <option value="">-</option>
                                        {{ gc.profileSelect.serviceNames | safe }}
                                        
                                      </select>
                                    </div>
                                  </div>
    
                                  
                                  <div class="col-lg-3">
                                    <div class="form-group">
                                      Account Ids
                                      <select class="form-control" style="display:inline" name="accountIds" id="accountIds" multiple>
                                        <option value="">-</option>
                                        {{ gc.profileSelect.accountIds | safe }}
                                      </select>
                                    </div>
                                  </div>
    
                                  
                                  <div class="col-lg-2">
                                    <div class="form-group">
                                      Region Codes
                                      <select class="form-control" style="display:inline" name="regionCodes" id="regionCodes" multiple>
                                        <option value="">-</option>
                                        {{ gc.profileSelect.regionCodes | safe }}
                                        
                                      </select>
                                    </div>
                                  </div>
                                {% else %}
                                  <!-- Begin: Profile form -->
                                  <div class="col-lg-3">
                                    <div class="form-group">
                                      Profile Names
                                      <select class="form-control" style="display:inline" name="profileNames" id="profileNames" multiple>
                                        <option value="">-</option>
                                        {{ gc.profileSelect.profileNames | safe }}
                                        
                                      </select>
                                    </div>
                                  </div>
                                  
                                  <div class="col-lg-2">
                                    <div class="form-group">
                                      Service Names
                                      <select class="form-control" style="display:inline" name="serviceNames" id="serviceNames" multiple>
                                        <option value="">-</option>
                                        {{ gc.profileSelect.serviceNames | safe }}
                                        
                                      </select>
                                    </div>
                                  </div>
    
                                  
                                  <div class="col-lg-5">
                                    <div class="form-group">
                                      Account Ids
                                      <select class="form-control" style="display:inline" name="accountIds" id="accountIds" multiple>
                                        <option value="">-</option>
                                        {{ gc.profileSelect.accountIds | safe }}
                                      </select>
                                    </div>
                                  </div>
    
                                  
                                  <div class="col-lg-2">
                                    <div class="form-group">
                                      Region Codes
                                      <select class="form-control" style="display:inline" name="regionCodes" id="regionCodes" multiple>
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
                        {% endif %}
                    <!-- End: Profile form  -->
          """
    except:
      logException("unable to generate 'profile-form'")
      
    return thisFormTags
      
      
  def loadFormThemeTags(self, themeName = "default"):
    if themeName in ["user"]:
      theme_dict = self.loadFormTheme_User()
    else:
      theme_dict = self.loadFormTheme_Default()
  
    return theme_dict