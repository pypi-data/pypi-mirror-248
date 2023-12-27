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

from pado.rules import GcRules
from pado.render import GcRender
from pado.form import GcForm

from os.path import join

class GcTemplates:
  def __init__(self, gcRules = None):
    if isinstance(gcRules, GcRules):
      self.homeDir = gcRules.homeDir
      logDebug("homeDir:[{}]".format(self.homeDir))
      
      self.confPath = gcRules.confPath
      logDebug("confPath:[{}]".format(self.confPath))
      
      self.serviceConf_dict = gcRules.serviceConf_dict
      logDebug("serviceConf_dict:[{}]".format(self.serviceConf_dict))
      
      self.frameConf_dict = gcRules.frameConf_dict
      logDebug("frameConf_dict:[{}]".format(self.frameConf_dict))
      
      self.cssConf_dict = gcRules.cssConf_dict
      logDebug("cssConf_dict:[{}]".format(self.cssConf_dict))
      
      self.jsConf_dict = gcRules.jsConf_dict
      logDebug("jsConf_dict:[{}]".format(self.jsConf_dict))
      
      self.modalConf_dict = gcRules.modalConf_dict
      logDebug("modalConf_dict:[{}]".format(self.modalConf_dict))
      
      self.nav_conf = gcRules.nav_conf
      logDebug("nav_conf:[{}]".format(self.nav_conf))
      
      self.static_dir = gcRules.static_dir
      logInfo("static_dir:[{}]".format(self.static_dir))
      
      self.template_dir = gcRules.template_dir
      logInfo("template_dir:[{}]".format(self.template_dir))
      
      self.rules_dict = gcRules.rules_dict
      logInfo("rules_dict:[{}]".format(self.rules_dict))
    
    else:
      raise ValueError("gcTemplates:[{}] is not the type:GcRules".format(gcRules))
    
    self.gcForm = GcForm()
    self.generateTemplates()
  
  def generateCssTags(self, css_dict):
    cssTag = ""
    for cssName in css_dict.keys():
      cssTag += "\n<!-- {} for this template-->\n".format(cssName)
      for cssItems in css_dict[cssName]:
        cssTag += "  <link href=\"{}\" rel=\"stylesheet\" type=\"text/css\">\n".format(cssItems["stylesheet"])
      
    #logDebug(cssTag)
    return cssTag
  
  def generateJsTags(self, js_dict):
    jsTag = ""
    for jsName in js_dict.keys():
      jsTag += "\n<!-- {} JavaScript for this template-->\n".format(jsName)
      for cssItems in js_dict[jsName]:
        jsTag += "  <script src=\"{}\"\"></script>\n".format(cssItems["script"])
      
    #logDebug(jsTag)
    return jsTag
  
  def generateTopBar(self):
    topBarTags_dict = {}
    topBarName = self.nav_conf["top"]["__name__"]
    for ruleName in self.nav_conf["top"].keys():
      if ruleName == "__name__":
        continue
      
      topBarTags_dict[ruleName] = {
        "searchBar":"""
                      <!-- Topbar Search -->
                      """, 
        "navBar":"""
                    <!-- Topbar Navbar -->
                    <ul class="navbar-nav ml-auto">
                """
        }
      
      for topNavItems in self.nav_conf["top"][ruleName]:
        logDebug("ruleName:[{}]".format(ruleName))
        for navItemName in topNavItems.keys():
          navItem_dict = {
            "name":navItemName,
            **topNavItems[navItemName]
            }
          logDebug("{}:navItem_dict:[{}]".format(ruleName, navItem_dict))
          try:
            if navItem_dict["type"] == "searchBar":
              topBarTags_dict[ruleName]["searchBar"] += """
                      <form action='${{__form_target__}}' method='${{__form_method__}}'
                          class="d-none d-sm-inline-block form-inline mr-auto ml-md-3 my-2 my-md-0 mw-100 navbar-search">
                          <div class="input-group">
                              <input type="text" class="form-control bg-light border-0 small" placeholder="${{__placeholder__}}"
                                  aria-label="${{__label__}}" aria-describedby="basic-addon2">
                              <div class="input-group-append">
                                  <button class="btn btn-primary" type="button">
                                      <i class="fas fa-search fa-sm"></i>
                                  </button>
                              </div>
                          </div>
                      </form>
                      """.replace("${{__label__}}",navItemName).replace("${{__form_target__}}", navItem_dict["target"]).replace("${{__form_method__}}", navItem_dict["method"]).replace("${{__placeholder__}}",navItem_dict["placeholder"])
            
            elif navItem_dict["type"] == "searchDropDwon":
              topBarTags_dict[ruleName]["navBar"] += """
                        <!-- Nav Item - Search Dropdown (Visible Only XS) -->
                        <li class="nav-item dropdown no-arrow d-sm-none">
                            <a class="nav-link dropdown-toggle" href="#" id="searchDropdown" role="button"
                                data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                <i class="fas fa-search fa-fw"></i>
                            </a>
                            <!-- Dropdown - Messages -->
                            <div class="dropdown-menu dropdown-menu-right p-3 shadow animated--grow-in"
                                aria-labelledby="searchDropdown">
                                <form class="form-inline mr-auto w-100 navbar-search">
                                    <div class="input-group">
                                        <input type="text" class="form-control bg-light border-0 small"
                                            placeholder="Search for..." aria-label="Search"
                                            aria-describedby="basic-addon2">
                                        <div class="input-group-append">
                                            <button class="btn btn-primary" type="button">
                                                <i class="fas fa-search fa-sm"></i>
                                            </button>
                                        </div>
                                    </div>
                                </form>
                            </div>
                        </li>
                        """

            elif navItem_dict["type"] == "modal":
              logDebug("ruleName:[{}]".format(ruleName))
              moduActions = ""
              for action_dict in navItem_dict["action"]:
                if "target" in action_dict.keys():
                  modalTarget = action_dict["target"]
                else:
                  modalTarget = "#"
                
                logDebug("bgColor:[{}]".format(action_dict["bgColor"]))
                
                if action_dict["type"] in ["text"]:
                  moduActions += """
                                <a class="dropdown-item d-flex align-items-center" href="${{__modalTarget__}}">
                                    <div class="mr-3">
                                        <div class="${{__modalIconType__}} ${{__modalBgColor__}}">
                                            <i class="fas fa-file-alt "></i>
                                        </div>
                                    </div>
                                    <div>
                                        <div class="small text-gray-500">${{__modalSubTitle__}}</div>
                                        <span class="font-weight-bold">${{__modalDescription__}}</span>
                                    </div>
                                </a>
                  """.replace("${{__modalTarget__}}",modalTarget).replace("${{__modalIcon__}}",action_dict["icon"]).replace("${{__modalIconType__}}",action_dict["iconType"]).replace("${{__modalBgColor__}}",action_dict["bgColor"]).replace("${{__modalSubTitle__}}",action_dict["subTitle"]).replace("${{__modalDescription__}}",action_dict["description"])

                elif action_dict["type"] in ["link"]:
                  moduActions += """
                                <a class="dropdown-item text-center small text-gray-500" href="${{__modalTarget__}}">${{__modalDescription__}}</a>
                  """.replace("${{__modalTarget__}}",modalTarget).replace("${{__modalDescription__}}",action_dict["description"])
                                
              topBarTags_dict[ruleName]["navBar"] += """
                        <!-- Nav Item - Alerts -->
                        <div class="nav-item dropdown no-arrow mx-1">
                            <a class="nav-link dropdown-toggle" href="#" id="${{__modalName__}}" role="button"
                                data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                <i class="fas fa-bell fa-fw"></i>
                                <!-- Counter - Alerts -->
                                <span class="badge ${{__modalBadgeColor__}} badge-counter">${{__modalBadge__}}</span>
                            </a>
                            <!-- Dropdown - Alerts -->
                            <div class="dropdown-list dropdown-menu dropdown-menu-right shadow animated--grow-in"
                                aria-labelledby="${{__modalName__}}">
                                <h6 class="dropdown-header">
                                    ${{__modalName__}}
                                </h6>
                                ${{__modalAction__}}
                            </div>
                        </div>
              """.replace("${{__modalName__}}", navItem_dict["name"]).replace("${{__modalBadgeColor__}}",navItem_dict["badgeColor"]).replace("${{__modalBadge__}}", navItem_dict["badge"]).replace("${{__modalAction__}}", moduActions)

            elif navItem_dict["type"] == "dropdown":
              topBarTags_dict[ruleName]["navBar"] += """
                        <!-- Nav Item - User Information -->
                        <div class="nav-item dropdown no-arrow">
                            <a class="nav-link dropdown-toggle" href="#" id="userDropdown" role="button"
                                data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                <span class="mr-2 d-none d-lg-inline text-gray-600 small">{{ gc.cookies.firstName }} {{ gc.cookies.lastName }}</span>
                                <img class="img-profile rounded-circle"
                                    src="https://internal-cdn.amazon.com/badgephotos.amazon.com/?uid={{ gc.cookies.loginAliasId }}">
                            </a>
                            <!-- Dropdown - User Information -->
                            <div class="dropdown-menu dropdown-menu-right shadow animated--grow-in"
                                aria-labelledby="userDropdown">
                                <a class="dropdown-item" href="#">
                                    <i class="fas fa-user fa-sm fa-fw mr-2 text-gray-400"></i>
                                    Profile
                                </a>
                                <a class="dropdown-item" href="#">
                                    <i class="fas fa-cogs fa-sm fa-fw mr-2 text-gray-400"></i>
                                    Settings
                                </a>
                                <a class="dropdown-item" href="#">
                                    <i class="fas fa-list fa-sm fa-fw mr-2 text-gray-400"></i>
                                    Activity Log
                                </a>
                                <div class="dropdown-divider"></div>
                                <a class="dropdown-item" href="https://moduaws.aka.amazon.com:8080/">
                                    <i class="fas fa-list fa-sm fa-fw mr-2 text-gray-400"></i>
                                    Prod
                                </a>
                                <a class="dropdown-item" href="https://moduaws-beta.aka.amazon.com:8080/">
                                    <i class="fas fa-list fa-sm fa-fw mr-2 text-gray-400"></i>
                                    Beta
                                </a>
                                <a class="dropdown-item" href="https://moduaws-alpha.aka.amazon.com:8080/">
                                    <i class="fas fa-list fa-sm fa-fw mr-2 text-gray-400"></i>
                                    Alpha
                                </a>
                                <div class="dropdown-divider"></div>
                                <a class="dropdown-item" href="#" data-toggle="modal" data-target="#logoutModal">
                                    <i class="fas fa-sign-out-alt fa-sm fa-fw mr-2 text-gray-400"></i>
                                    Logout
                                </a>
                            </div>
                        </div>
                        """
            elif navItem_dict["type"] == "text":
              topBarTags_dict[ruleName]["navBar"] += """
                        <span class="mr-2 d-none d-lg-inline text-gray-600 small">"""+ navItem_dict["rule"] + """</span>
                        """
            elif navItem_dict["type"] == "divider":
              topBarTags_dict[ruleName]["navBar"] += """
                        <div class="topbar-divider d-none d-sm-block"></div>
                        """
          except:
            logException("unable to generate topNavItems:[{}]".format(topNavItems))
          
        topBarTags_dict[ruleName]["navBar"] += """
                    </ul>
                    """
                    
    return topBarTags_dict
  
  def generateSideBar(self):
    sideBarTags_dict = {}
    sidebarName = self.nav_conf["left"]["__name__"]
    for ruleName in self.nav_conf["left"].keys():
      if ruleName == "__name__":
        continue
      
      leftNavItem_list = self.nav_conf["left"][ruleName]
    
      navItemTagTemplate = """
              <!-- Nav Item - Pages Collapse Menu -->
              <li class="nav-item">
                  <a class="nav-link collapsed" href="#" data-toggle="collapse" data-target="#${{__navId__}}"
                      aria-expanded="true" aria-controls="collapseTwo">
                      <i class="fas fa-fw fa-cog"></i>
                      <span>${{__navItemName__}}</span>
                  </a>
                  <div id="${{__navId__}}" class="collapse{% if gc.active in ${{__thisRuleAndAction__}} %} show{% endif %}" aria-labelledby="headingTwo" data-parent="#accordionSidebar">
                      <div class="bg-white py-2 collapse-inner rounded">
                          <!--  <h6 class="collapse-header">Custom Components:</h6> -->
                          ${{__actionItemTags__}}
                      </div>
                  </div>
              </li>
              """
              
      subNavItemTagWithActionTemplate ="""
                          <a class="collapse-item{% if gc.active == "${{__rule__}}:${{__action__}}" %} active{% endif %}" href="/${{__rule__}}?action=${{__action__}}&atk={{ gc.form.authenticityTokenId }}">${{__actionName__}}</a>
      """
      subNavItemTagWithoutActuibTemplate ="""
                          <a class="collapse-item{% if gc.active == "${{__rule__}}" %} active{% endif %}" href="/${{__rule__}}">${{__actionName__}}</a>
      """
      
      navTags = """
          <!-- Sidebar -->
          <ul class="navbar-nav bg-gradient-primary sidebar sidebar-dark accordion" id="accordionSidebar">
  
            <!-- Sidebar - Brand -->
              <a class="sidebar-brand d-flex align-items-center justify-content-center" href="./">
                  <div class="sidebar-brand-icon rotate-n-15">
                      <i class="fas fa-laugh-wink"></i>
                  </div>
                  <div class="sidebar-brand-text mx-3">${{__sidebarName__}}</div>
              </a>
              """.replace("${{__sidebarName__}}", sidebarName)
              
      for navItem_dict in leftNavItem_list:
        #logInfo("{}".format(navItem_dict))
        if "$__landingPage__" in navItem_dict.keys():
          landingPage_dict = navItem_dict["$__landingPage__"]
        elif "$__horizontal_divider__" in navItem_dict.keys() and navItem_dict["$__horizontal_divider__"]:
          navTags += """
              <!-- Divider -->
              <hr class="sidebar-divider">
              """
        elif "$__sidebar_message__" in navItem_dict.keys() and len(navItem_dict["$__sidebar_message__"]["msg"].strip().replace(" ","")) > 0:
          if "enable" in navItem_dict["$__sidebar_message__"].keys() and navItem_dict["$__sidebar_message__"]["enable"]:
              
            if "target" in navItem_dict["$__sidebar_message__"].keys():
              thisTag="""
                  <a class="btn btn-success btn-sm" href="${{__target__}}" target="_blank">${{__flashCard__}}</a>
              """.replace("${{__target__}}",navItem_dict["$__sidebar_message__"]["target"]).replace("${{__flashCard__}}", navItem_dict["$__sidebar_message__"]["flashCard"])
            else:
              thisTag = ""
              
            navTags += """
                <!-- Sidebar Message -->
                <div class="sidebar-card d-none d-lg-flex">
                    <img class="sidebar-card-illustration mb-2" src="/static/img/undraw_rocket.svg" alt="...">
                    <p class="text-center mb-2">${{__sidebar_message__}}</p>
                    ${{__msg_button__}}
                </div>
                """.replace("${{__sidebar_message__}}",navItem_dict["$__sidebar_message__"]["msg"].strip()).replace("${{__msg_button__}}",thisTag)
        else:
          for navItemName in navItem_dict.keys():
            if "rule" in navItem_dict[navItemName].keys():
              if navItem_dict[navItemName]["rule"] == "root":
                navItem_dict[navItemName]["rule"] = ""
              navTags += """
                <!-- Nav Item - ${{__ruleName__}} -->
                <li class="nav-item {% if gc.active == "${{__rule__}}" %}active{% endif %}">
                    <a class="nav-link" href="/${{__rule__}}">
                        <i class="fas fa-fw fa-chart-area"></i>
                        <span>${{__ruleName__}}</span></a>
                </li>
                """.replace("${{__rule__}}",navItem_dict[navItemName]["rule"]).replace("${{__ruleName__}}",navItemName)
              
            else:
              navTags += """
                <!-- Heading -->
                <div class="sidebar-heading">
                    ${{__headName__}}
                </div>
                """.replace("${{__headName__}}",navItemName)
              
              for navHeadName in navItem_dict.keys():
                #logDebug("{}:[{}]".format(navHeadName, navItem_dict[navHeadName]))
                
                
                for navSubItemName in navItem_dict[navHeadName].keys():
                  #logDebug("{}+{}:[{}]".format(navHeadName, navSubItemName, navItem_dict[navHeadName][navSubItemName]))
                  
                  if "rule" in navItem_dict[navHeadName][navSubItemName].keys():
                    navTags += """
                      <!-- Nav Item - ${{__ruleName__}} -->
                      <li class="nav-item {% if gc.active == "${{__rule__}}" %}active{% endif %}">
                          <a class="nav-link" href="/${{__rule__}}">
                              <i class="fas fa-fw fa-chart-area"></i>
                              <span>${{__ruleName__}}</span></a>
                      </li>
                      """.replace("${{__rule__}}",navItem_dict[navHeadName][navSubItemName]["rule"]).replace("${{__ruleName__}}",navSubItemName)
                  
                  else:
                    rule_list = []
                    subNavTags = ""
                    for actionName in navItem_dict[navHeadName][navSubItemName].keys():
                      if navItem_dict[navHeadName][navSubItemName][actionName]["action"] != "":
                        thisRuleAndAction = "{}:{}".format(navItem_dict[navHeadName][navSubItemName][actionName]["rule"], navItem_dict[navHeadName][navSubItemName][actionName]["action"])
                        subNavTags += subNavItemTagWithActionTemplate.replace("${{__rule__}}",navItem_dict[navHeadName][navSubItemName][actionName]["rule"]).replace("${{__action__}}",navItem_dict[navHeadName][navSubItemName][actionName]["action"]).replace("${{__actionName__}}",actionName)
                    
                      else:
                        thisRuleAndAction = "{}".format(navItem_dict[navHeadName][navSubItemName][actionName]["rule"])
                        subNavTags += subNavItemTagWithoutActuibTemplate.replace("${{__rule__}}",navItem_dict[navHeadName][navSubItemName][actionName]["rule"]).replace("${{__action__}}",navItem_dict[navHeadName][navSubItemName][actionName]["action"]).replace("${{__actionName__}}",actionName)
                    
                      if thisRuleAndAction in rule_list:
                        pass
                      else:
                        rule_list.append(thisRuleAndAction)
                        
                      
                    navTags += navItemTagTemplate.replace("${{__thisRuleAndAction__}}", "{}".format(rule_list)).replace("${{__actionItemTags__}}", subNavTags).replace("${{__navItemName__}}", navSubItemName).replace("${{__navId__}}", "{}{}".format(navSubItemName.strip().replace(" ","")[0].lower(), navSubItemName.strip().replace(" ","")[1:]))
                    
      navTags += """
              <!-- Divider -->
              <hr class="sidebar-divider d-none d-md-block">
  
              <!-- Sidebar Toggler (Sidebar) -->
              <div class="text-center d-none d-md-inline">
                  <button class="rounded-circle border-0" id="sidebarToggle"></button>
              </div>
              
              
  
          </ul>
          <!-- End of Sidebar -->
          """
      
      sideBarTags_dict[ruleName] = navTags
      #logDebug("sidebarName:[{}]:[{}]".format(sidebarName, sideBarTags_dict[ruleName]))
      
    return sideBarTags_dict
  
  
  
  def generateMoalTags(self, modal_dict):
    #for key in modal_dict.keys():
    #  logDebug("{}:[{}]".format(key, modal_dict[key]))
    
    modalTags = ""
    for modalName in modal_dict.keys():
      
      modalItem_dict = modal_dict[modalName]
      #for key in modalItem_dict.keys():
      #  logDebug("{}\t{}:[{}]".format(modalName, key, modalItem_dict[key]))
      
      if "type" in modalItem_dict.keys() and modalItem_dict["type"] in ["form"]:
        #logDebug("=========> name:[{}]->type:[{}]".format(modalName, modal_dict[modalName]["type"]))
        
        if isinstance(modalItem_dict["message"], str) and len(modalItem_dict["message"]) > 0:
          modalMessage = """<div class="modal-body">
                      ${{__modalMessage__}}
                  </div>""".replace("${{__modalMessage__}}",modalItem_dict["message"])
        else:
          modalMessage = ""
        
        if isinstance(modalItem_dict["inputs"], dict):
          if "action" in modalItem_dict.keys():
            modalInputTags = """
                        <input type='hidden' name='action' value='${{__action__}}' />
            """.replace("${{__action__}}", modalItem_dict["action"])
          else:
            logWarn("'action' is not provided")
            modalInputTags = ""
            
          for inputName in modalItem_dict["inputs"].keys():
            
            if len(inputName.strip()) > 0:
              inputName = inputName.strip()
              inputId = "{}{}".format(inputName[0].lower(), "{}".format(inputName[1:]).replace(" ",""))
            else:
              inputId = inputName  
            
            if modalItem_dict["inputs"][inputName]["type"] in ["select"]:
              
              logDebug("=========> name:[{}]->type:[{}]:[{}]".format(modalName, modal_dict[modalName]["type"], modalItem_dict["inputs"][inputName]["type"]))
              
              if "default" in modalItem_dict["inputs"][inputName].keys():
                selectItemTags = "                                              <option value='{}'>{}</option>\n".format(modalItem_dict["inputs"][inputName]["default"], modalItem_dict["inputs"][inputName]["default"])
              else:
                selectItemTags = "                                              <option value=''>{}</option>\n".format(modalItem_dict["inputs"][inputName]["placeholder"])
              
              if isinstance(modalItem_dict["inputs"][inputName]["list"], list):
                for name in modalItem_dict["inputs"][inputName]["list"]:
                  selectItemTags += "                                              <option value=\"{}\">{}</option>\n".format(name, name)
              
              elif isinstance(modalItem_dict["inputs"][inputName]["list"], str):
                
                  selectItemTags += """                                          <!-- {{ ${{__input_list__}} }}-->      
                                                    {% for optionName in ${{__input_list__}} %}
                                                        <option value="{{optionName}}">{{optionName}}</option>
                                                    {% endfor %}""".replace("${{__input_list__}}", modalItem_dict["inputs"][inputName]["list"])
                    
              
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
              
              if "size" in modalItem_dict["inputs"][inputName].keys() and modalItem_dict["inputs"][inputName]["size"] > 0:
                thisFormTags = thisFormTags.replace("${{__size__}}", "{}".format(modalItem_dict["inputs"][inputName]["size"]))
              else:
                thisFormTags = thisFormTags.replace("${{__size__}}", "3")
                
              if "required" in modalItem_dict["inputs"][inputName].keys() and modalItem_dict["inputs"][inputName]["required"]:
                thisFormTags = thisFormTags.replace("${{__required__}}", "required")
              else:
                thisFormTags = thisFormTags.replace("${{__required__}}","")
              
              modalInputTags += thisFormTags
            else:
              #logDebug("=========> name:[{}]->type:[{}]:[{}]".format(modalName, modal_dict[modalName]["type"], modalItem_dict["inputs"][inputName]["type"]))
              
              modalInputTags += """
                      <div class="col-lg-50">
                        <div class="form-group">
                          ${{__inputName__}}
                            <input style="display:inline" type="text" class="form-control"
                                id="${{__inputId__}}" name="${{__inputId__}}" value=""
                                placeholder="${{__placeholder__}}" >
                        </div>
                      </div>""".replace("${{__inputName__}}", inputName).replace("${{__inputId__}}",inputId).replace("${{__placeholder__}}",modalItem_dict["inputs"][inputName]["placeholder"])
                      
        modalName = "{}{}".format(modalName.strip()[0].lower(),modalName.strip().replace(" ","")[1:])
        modalTags += "\n<!-- {} Modal-->\n".format(modalName)
        modalTags += """  
      <div class="modal fade" id="${{__modalId__}}" tabindex="-1" role="dialog" aria-labelledby="${{__modalAlias__}}"
          aria-hidden="true">
          <div class="modal-dialog" role="document"  style="width:1250px;">
              <div class="modal-content">
            
                <div class="modal-header">
                    <h5 class="modal-title" id="${{__modalAlias__}}">${{__modalTitle__}}</h5>
                    <button class="close" type="button" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">x</span>
                    </button>
                </div>
                ${{__modalMessage__}}
                <form action='${{__modalTargetUrl__}}' method='get' class="default">
                  <div class="modal-body">
                      ${{__modalInputTags__}}
                      
                      <input type='hidden' name='iSL' value='y' />
                      <input type='hidden' name='atk' value='{{ gc.form.authenticityTokenId | safe }}' />
                      
                  </div>
                  <div class="modal-footer">
                      ${{__modalTargets__}}
                  </div>
                  
                </form>
                
              </div>
          </div>
      </div>
        """.replace("${{__modalId__}}","{}Modal".format(modalName)).replace("${{__modalAlias__}}","{}Label".format(modalName)).replace("${{__modalTitle__}}",modalItem_dict["title"]).replace("${{__modalTargetUrl__}}",modalItem_dict["target"]).replace("${{__modalMessage__}}",modalMessage).replace("${{__modalInputTags__}}",modalInputTags)
      
        modalTargets = ""
        for targetItems in modalItem_dict["targets"]:
          if "active" in targetItems.keys() and targetItems["active"]:
            active = "btn btn-primary"
          else:
            active = "btn btn-secondary"
          
          if "target" in targetItems.keys():
            if len(targetItems["target"].strip()) > 0 and targetItems["target"][0] != "#":
              modalTargets += """
                       <a class="${{__active__}}" href="${{__target__}}">${{__label__}}</a>
              """.replace("${{__active__}}", active).replace("${{__target__}}", targetItems["target"].strip()).replace("${{__label__}}",  targetItems["label"])
            else:
              modalTargets += """
                    <button class="${{__active__}}" type="button" data-dismiss="modal">
                        <span aria-hidden="true">${{__label__}}</span>
                    </button>
              """.replace("${{__active__}}", active).replace("${{__label__}}",  targetItems["label"])
          else:
            modalTargets += """
                     <button class="${{__active__}}" type="submit" name="submit" value="${{__label__}}">${{__label__}}</button>
            """.replace("${{__active__}}", active).replace("${{__label__}}", targetItems["label"]).replace("${{__name__}}",  targetItems["label"].lower())
        
        modalTags = modalTags.replace("${{__modalTargets__}}", modalTargets)
      
      elif "type" in modalItem_dict.keys() and modalItem_dict["type"] in ["hint"]:
        modalName = "{}{}".format(modalName.strip()[0].lower(),modalName.strip().replace(" ","")[1:])
        modalTags += "\n<!-- {} Modal-->\n".format(modalName)
        modalTags += """  
      <div class="modal fade" id="${{__modalId__}}" tabindex="-1" role="dialog" aria-labelledby="${{__modalAlias__}}"
          aria-hidden="true">
          <div class="modal-dialog" role="document">
              <div class="modal-content" style="top:5%;right:50%;outline: none;overflow:hidden;width:1024px;">
                  <div class="modal-header">
                      <h5 class="modal-title" id="${{__modalAlias__}}">${{__modalTitle__}}</h5>
                      <button class="close" type="button" data-dismiss="modal" aria-label="Close">
                          <span aria-hidden="true">x</span>
                      </button>
                  </div>
                  <div class="modal-body">${{__modalMessage__}}</div>
                  <div class="modal-footer">
                      ${{__modalTargets__}}
                  </div>
              </div>
          </div>
      </div>
        """.replace("${{__modalId__}}","{}Modal".format(modalName)).replace("${{__modalAlias__}}","{}Label".format(modalName)).replace("${{__modalTitle__}}",modalItem_dict["title"]).replace("${{__modalMessage__}}",modalItem_dict["message"])
      
        modalTargets = ""
        for targetItems in modalItem_dict["targets"]:
          if "active" in targetItems.keys() and targetItems["active"]:
            active = "btn btn-primary"
          else:
            active = "btn btn-secondary"
          
          if "link" in targetItems.keys():
              modalTargets += """
                       <a class="${{__active__}}" href="${{__target__}}" target="_blank">${{__label__}}</a>
              """.replace("${{__active__}}", active).replace("${{__target__}}", targetItems["link"].strip()).replace("${{__label__}}",  targetItems["label"])
          
          elif "target" in targetItems.keys():
            if len(targetItems["target"].strip()) > 0 and targetItems["target"][0] != "#":
              modalTargets += """
                       <a class="${{__active__}}" href="${{__target__}}">${{__label__}}</a>
              """.replace("${{__active__}}", active).replace("${{__target__}}", targetItems["target"].strip()).replace("${{__label__}}",  targetItems["label"])
            else:
              modalTargets += """
                       <button class="${{__active__}} type="button" data-dismiss="modal">${{__label__}}</button>
              """.replace("${{__active__}}", active).replace("${{__target__}}", targetItems["target"].strip()).replace("${{__label__}}",  targetItems["label"])
          else:
            modalTargets += """
                     <button class="${{__active__}} type="button" data-dismiss="modal">${{__label__}}</button>
            """.replace("${{__active__}}", active).replace("${{__label__}}",  targetItems["label"])
        
            
        modalTags = modalTags.replace("${{__modalTargets__}}", modalTargets)
        
      else:
        modalName = "{}{}".format(modalName.strip()[0].lower(),modalName.strip().replace(" ","")[1:])
        modalTags += "\n<!-- {} Modal-->\n".format(modalName)
        modalTags += """  
      <div class="modal fade" id="${{__modalId__}}" tabindex="-1" role="dialog" aria-labelledby="${{__modalAlias__}}"
          aria-hidden="true">
          <div class="modal-dialog" role="document">
              <div class="modal-content">
                  <div class="modal-header">
                      <h5 class="modal-title" id="${{__modalAlias__}}">${{__modalTitle__}}</h5>
                      <button class="close" type="button" data-dismiss="modal" aria-label="Close">
                          <span aria-hidden="true">x</span>
                      </button>
                  </div>
                  <div class="modal-body">${{__modalMessage__}}</div>
                  <div class="modal-footer">
                      ${{__modalTargets__}}
                  </div>
              </div>
          </div>
      </div>
        """.replace("${{__modalId__}}","{}Modal".format(modalName)).replace("${{__modalAlias__}}","{}Label".format(modalName)).replace("${{__modalTitle__}}",modalItem_dict["title"]).replace("${{__modalMessage__}}",modalItem_dict["message"])
      
        modalTargets = ""
        for targetItems in modalItem_dict["targets"]:
          if "active" in targetItems.keys() and targetItems["active"]:
            active = "btn btn-primary"
          else:
            active = "btn btn-secondary"
          
          if "target" in targetItems.keys():
            if len(targetItems["target"].strip()) > 0 and targetItems["target"][0] != "#":
              modalTargets += """
                       <a class="${{__active__}}" href="${{__target__}}">${{__label__}}</a>
              """.replace("${{__active__}}", active).replace("${{__target__}}", targetItems["target"].strip()).replace("${{__label__}}",  targetItems["label"])
            else:
              modalTargets += """
                       <button class="${{__active__}} type="button" data-dismiss="modal">${{__label__}}</button>
              """.replace("${{__active__}}", active).replace("${{__target__}}", targetItems["target"].strip()).replace("${{__label__}}",  targetItems["label"])
          else:
            modalTargets += """
                     <button class="${{__active__}} type="button" data-dismiss="modal">${{__label__}}</button>
            """.replace("${{__active__}}", active).replace("${{__label__}}",  targetItems["label"])
        
            
        modalTags = modalTags.replace("${{__modalTargets__}}", modalTargets)
      
    #logDebug(modalTags)
    return modalTags
  
  def generateTemplates(self):
    core_cssTags = self.generateCssTags(self.cssConf_dict["core_css"])
    core_jsTags = self.generateJsTags(self.jsConf_dict["core_js"])
    core_modalTags = self.generateMoalTags(self.modalConf_dict["core_modal"])
    
    topBarTags_dict = self.generateTopBar()
    sideBarTags_dict = self.generateSideBar()
    #logDebug("self.sideBarTags_dict:[{}]".format(sideBarTags_dict.keys()))


    for ruleName in self.rules_dict.keys():
      logInfo("ruleName:[{}]->rule_dict:[{}]".format(ruleName, self.rules_dict[ruleName]))
      
      #for key in self.rules_dict[ruleName].keys():
      #  logDebug("{}:[{}]".format(key, self.rules_dict[ruleName][key]))
      
      
      if self.rules_dict[ruleName]["name"] == "_root":
        htmlTemplateName = join(self.template_dir, "{}.html".format("index"))
      else:
        htmlTemplateName = join(self.template_dir, "{}.html".format(self.rules_dict[ruleName]["name"]))
      
      
      try:
        cssTags = core_cssTags + self.generateCssTags(self.rules_dict[ruleName]["view"].css_dict)
        jsTags = core_jsTags + self.generateJsTags(self.rules_dict[ruleName]["view"].js_dict)                  
        modalTags = core_modalTags + self.generateMoalTags(self.rules_dict[ruleName]["view"].modal_dict)
        
        gcRender = GcRender()
        cardTags = gcRender.generateCardTags(self.rules_dict[ruleName]["view"].card_dict, form_dict=self.rules_dict[ruleName]["form"].form_dict)
        
        cardJsTags = gcRender.getJsTags()
        cardJsTags += self.gcForm.generateFormJsTags(self.rules_dict[ruleName]["form"].form_dict)
        
        thisHtmlTemplate = self.rules_dict[ruleName]["view"].html_template.strip().replace("${{__css__}}", cssTags).replace("${{__java_script__}}", jsTags).replace("${{__modal__}}", modalTags)
        
        if ruleName in sideBarTags_dict.keys():
          thisHtmlTemplate = thisHtmlTemplate.replace("${{__sidebar__}}", sideBarTags_dict[ruleName])
        else:
          thisHtmlTemplate = thisHtmlTemplate.replace("${{__sidebar__}}", sideBarTags_dict["default"])
        
        if ruleName in topBarTags_dict.keys():
          thisHtmlTemplate = thisHtmlTemplate.replace("${{__topSearchBar__}}", topBarTags_dict[ruleName]["searchBar"])
          thisHtmlTemplate = thisHtmlTemplate.replace("${{__topNavBar__}}", topBarTags_dict[ruleName]["navBar"])
        else:
          thisHtmlTemplate = thisHtmlTemplate.replace("${{__topSearchBar__}}", topBarTags_dict["default"]["searchBar"])
          thisHtmlTemplate = thisHtmlTemplate.replace("${{__topNavBar__}}", topBarTags_dict["default"]["navBar"])
        
        thisHtmlTemplate = thisHtmlTemplate.replace("${{__cards__}}", cardTags).replace("${{__card_java_script__}}", cardJsTags)
        
        thisForms_dict = self.gcForm.generateForms(self.rules_dict[ruleName]["form"].form_dict)
        for formName in thisForms_dict.keys():
          #logDebug("formName:[{}]->[{}]".format(formName, thisForms_dict[formName]))
          thisHtmlTemplate = thisHtmlTemplate.replace("${{__form_"+formName+"__}}", thisForms_dict[formName])
          
        f = open(htmlTemplateName, "w")
        f.write(thisHtmlTemplate)
        f.close()
      except:
        logException("ruleName:[{}]->unable to write html tmeplate:[{}]".format(self.rules_dict[ruleName]["name"], htmlTemplateName))
      