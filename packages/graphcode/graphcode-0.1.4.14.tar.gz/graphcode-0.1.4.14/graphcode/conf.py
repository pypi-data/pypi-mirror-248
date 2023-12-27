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
Created on June 21, 1998

@author: Ryeojin Moon
'''
import json
from os import mkdir
from os.path import join, abspath, exists, expanduser
from graphcode.path import createDir

# Utility function to load JSON configuration files
def loadJsonConfig(file_path):
  with open(file_path, 'r') as fp:
    return json.load(fp)

# Load service configurations from the 'service.json' file
def loadDefaultServiceConfigurations(name="moduaws"):
  """Load default service configurations."""
  
  config_path = join(abspath('./conf'), 'service.json')
  if exists(config_path):
    return loadJsonConfig(config_path)
  
  else:
    conf_dict = {
      "name": f"{name}",
      "version": "1.0.0",
      "buildNumber": 2430994,
      "copyRight": "2002-2024",
      "root":f"~/{name}",
      "aws":f"~/{name}/.aws/",
      "atk":f"~/{name}/.atk/",
      "localCookie": "~/.midway/cookie",
      "credentials":f"~/{name}/.basic/",
      "temporary":f"~/{name}/tmp/",
      "downloads":f"~/{name}/downloads/",
      "logs":f"~/{name}/logs/",
      "logLevel":"DEBUG", # DEBUG, INFO, WARNING, ERROR, CRITICAL

      "homeURL":"https://localhost:5000",
      
      "css":"./conf/css/",
      "js":"./conf/js/",
      "modal":"./conf/modal/",
      "rules":"./codex",
      "static":"./static",
      "templates":"./templates",

      "cookies":{
        "awsAccountId":"",
        "userName":"",
        "firstName":"",
        "lastName":"",
        "orgName":"",
        "emailVerification":False
      },

      "codex": {
        "homeURL":"localhost",
        "host": "localhost",
        "port": 8080,
        "debug": False,
        "ssl": True,
        "cert": "./certs/default.cert",
        "key": "./certs/default.key"
      },

      "pathway": {
        "homeURL":"localhost",
        "host": "localhost",
        "port": 8000,
        "debug": False,
        "ssl": True,
        "cert": "./certs/default.cert",
        "key": "./certs/default.key"
      }
    }

    return saveDefaultServiceConfigurations(conf_dict)

def getLocalCookiePath():
  return loadDefaultServiceConfigurations()["localCookie"]

def loadLocalCookie():
  file_path = abspath(expanduser(getLocalCookiePath()))
  if exists(file_path):
    with open(file_path, 'r') as fp:
      return fp.read()
  else:
    return ""
  
# Save ItemDB configurations
def saveDefaultServiceConfigurations(conf_dict):
  """Save Default Service Configurations."""
  config_path = join(abspath('./conf'), 'service.json')
  with open(config_path, 'w') as fp:
    json.dump(conf_dict, fp, indent=2)
  return conf_dict

# get service name
def getServiceName():
  """get service name from configuration."""
  return loadDefaultServiceConfigurations()["name"]

# get version
def getVersion():
  """get version from configuration."""
  return loadDefaultServiceConfigurations()["version"]

# get buildNumber
def getBuildNumber():
  """get Build Number from configuration."""
  return loadDefaultServiceConfigurations()["buildNumber"]

# get Copy Rights
def getCopyRight():
  """get copyRight from configuration."""
  return loadDefaultServiceConfigurations()["copyRight"]

# Get root path
def getRoot():
  """Get root path."""
  rootDir = loadDefaultServiceConfigurations()["root"]
  if not exists(expanduser(rootDir)):
    createDir(rootDir)
  return rootDir

# Get ATK path
def getATKPath():
  """Get root path."""
  atkDir = loadDefaultServiceConfigurations()["atk"]
  if not exists(expanduser(atkDir)):
    createDir(atkDir)
  return atkDir

# Get rules path
def getRulesPath():
  """Get root path."""
  rulesDir = loadDefaultServiceConfigurations()["rules"]
  if not exists(expanduser(rulesDir)):
    createDir(rulesDir)
  return rulesDir

# Get static path
def getStaticPath():
  """Get static path."""
  statidDir = loadDefaultServiceConfigurations()["static"]
  if not exists(expanduser(statidDir)):
    createDir(statidDir)
  return statidDir

# Get template path
def getTemplatePath():
  """Get template path."""
  templateDir = loadDefaultServiceConfigurations()["templates"]
  if not exists(expanduser(templateDir)):
    createDir(templateDir)
  return templateDir

# Get temp path
def getTemporaryPath():
  """Get temporary path."""
  temporaryDir = loadDefaultServiceConfigurations()["temporary"]
  if not exists(expanduser(temporaryDir)):
    createDir(temporaryDir)
  return temporaryDir

# Get temp path
def getDownloadPath():
  """Get Download path."""
  downloadDir = loadDefaultServiceConfigurations()["downloads"]
  if not exists(expanduser(downloadDir)):
    createDir(downloadDir)
  return downloadDir

# Get log path
def getLogPath():
  """Get log path."""
  logDir = loadDefaultServiceConfigurations()["logs"]
  if not exists(expanduser(logDir)):
    createDir(logDir)
  return logDir

# Get log level
def getLogLevel():
  """Get log level."""
  try:
    logLevel = loadDefaultServiceConfigurations()["logLevel"]
  except KeyError:
    logLevel = "DEBUG"
  return logLevel

# Get cert path
def getCertPath():
    """Get cert path."""
    certDir = loadDefaultServiceConfigurations()["certs"]
    if not exists(expanduser(certDir)):
        createDir(certDir)
    return certDir

# Get credentials path
def getCredentialsPath():
  """Get credentials path."""
  credDir = loadDefaultServiceConfigurations()["credentials"]
  if not exists(expanduser(credDir)):
      createDir(credDir)
  return credDir

# Get default accounts
def getCredentials():
  """Get default accounts."""
  config_path = join(expanduser(getCredentialsPath()), 'credentials.json')
  if not exists(config_path):
    credentials_dict = {
      "default":{
        "username":"",
        "password":""
        },
        "default2":{
          "accessKey":"",
          "secretKey":""
        }
      }
    with open(config_path, 'w') as fp:
      json.dump(credentials_dict, fp, indent=2)
  else:
    credentials_dict = loadJsonConfig(config_path)

  return credentials_dict

# set password with username
def setPasswordWithUsername(name, username, password):
  """Set Password with username """
  credentials_dict = getCredentials()
  if name in credentials_dict.keys():
    credentials_dict[name]["username"] = username
    credentials_dict[name]["password"] = password
    
  else:
    credentials_dict[name] = {
      "username": username,
      "password": password
    }

  config_path = join(expanduser(getCredentialsPath()), 'credentials.json')
  with open(config_path, 'w') as fp:
    json.dump(credentials_dict, fp, indent=2)
  
  return credentials_dict

# set password with username
def setSecretKeyWithAccessKey(name, accessKey, secretKey):
  """Set Password with username """
  credentials_dict = getCredentials()
  if name in credentials_dict.keys():
    credentials_dict[name]["accessKey"] = accessKey
    credentials_dict[name]["secretKey"] = secretKey
    
  else:
    credentials_dict[name] = {
      "accessKey": accessKey,
      "secretKey": secretKey
    }

  config_path = join(expanduser(getCredentialsPath()), 'credentials.json')
  with open(config_path, 'w') as fp:
    json.dump(credentials_dict, fp, indent=2)
  
  return credentials_dict

def getAccountsPath():
  """Get credentials path."""
  credDir = loadDefaultServiceConfigurations()["aws"]
  if not exists(expanduser(credDir)):
      createDir(credDir)
  return credDir

# Get default accounts
def getDefaultAccounts():
  """Get default accounts."""
  config_path = join(expanduser(getAccountsPath()), 'accounts.json')
  if not exists(config_path):
    accounts_dict = {
      "aws": None,
      "aws-cn": None,
      "aws-us-gov": None
      }
    with open(config_path, 'w') as fp:
      json.dump(accounts_dict, fp, indent=2)
  else:
    accounts_dict = loadJsonConfig(config_path)

  return accounts_dict

# Save default accounts
def setDefaultAccounts(partition, accountId):
  """Set Default Accounts."""
  accounts_dict = getDefaultAccounts()
  if partition in accounts_dict.keys():
    accounts_dict[partition] = accountId
    
    config_path = join(expanduser(getAccountsPath()), 'accounts.json')
    with open(config_path, 'w') as fp:
      json.dump(accounts_dict, fp, indent=2)

  else:
    raise ValueError(f"Invalid partition: {partition}")

# get Default Cookies
def getDefaultCookies():
  """get default cookies."""
  return loadDefaultServiceConfigurations()["cookies"]

# get Home URL
def getHomeURL():
  """get default cookies."""
  return loadDefaultServiceConfigurations()["homeURL"]

# Load frame configurations from the 'core_modal.json' file
def loadFrame():
  """Load modal configurations."""
  config_path = join(abspath("./conf"), 'frame.json')
  return loadJsonConfig(config_path)

# Load CSS configurations from the 'core_css.json' file
def loadCSS():
  """Load CSS configurations."""
  config_path = join(abspath(loadDefaultServiceConfigurations()["css"]), 'core.json')
  return loadJsonConfig(config_path)

# Load JavaScript configurations from the 'core_js.json' file
def loadJS():
  """Load JavaScript configurations."""
  config_path = join(abspath(loadDefaultServiceConfigurations()["js"]), 'core.json')
  return loadJsonConfig(config_path)

# Load modal configurations from the 'core_modal.json' file
def loadModal():
  """Load modal configurations."""
  config_path = join(abspath(loadDefaultServiceConfigurations()["modal"]), 'core.json')
  return loadJsonConfig(config_path)

# Load navigation configurations from various JSON files
def loadNav():
  """Load navigation configurations."""
  nav_configs = {}
  for position in ["top", "left", "right", "bottom"]:
    config_path = join(abspath('./conf'), f'nav/{position}.json')
    nav_configs[position] = loadJsonConfig(config_path)
  return nav_configs

# get Codex Home URL
def getCodexHomeURL():
  """get pathway home url."""
  return loadDefaultServiceConfigurations()["pathway"]["homeURL"]

# get Codex Host
def getCodexHost():
  """get codex host."""
  return loadDefaultServiceConfigurations()["codex"]["host"]

# get Codex Port
def getCodexPort():
  """get codex host."""
  return loadDefaultServiceConfigurations()["codex"]["host"]

# get Codex HTTP Method
def getCodexMethod():
  """get codex method."""
  return loadDefaultServiceConfigurations()["codex"]["method"]

# get Codex Debug Mode
def getCodexDebugMode():
  """get codex debug mode."""
  return loadDefaultServiceConfigurations()["codex"]["debug"]

# get Codex SSL Mode
def getCodexSSLMode():
  """get codex ssl mode."""
  return loadDefaultServiceConfigurations()["codex"]["ssl"]

# get Codex SSL Cert
def getCodexSSLCert():
  """get codex ssl cert."""
  return loadDefaultServiceConfigurations()["codex"]["cert"]

# get Codex SSL Key
def getCodexSSLKey():
  """get codex ssl key."""
  return loadDefaultServiceConfigurations()["codex"]["key"]

# get Codex Static Directory
def getCodexStaticPath():
  """get codex static directory."""
  return loadDefaultServiceConfigurations()["codex"]["static"]

# get Codex Templates Directory
def getCodexTemplatesPath():
  """get codex templates directory."""
  return loadDefaultServiceConfigurations()["codex"]["templates"]

# get Pathway Home URL
def getPathwayHomeURL():
  """get pathway home url."""
  return loadDefaultServiceConfigurations()["pathway"]["homeURL"]

# get Pathway Host
def getPathwayHost():
  """get pathway host."""
  return loadDefaultServiceConfigurations()["pathway"]["host"]

# get Pathway Port
def getPathwayPort():
  """get pathway host."""
  return loadDefaultServiceConfigurations()["pathway"]["host"]

# get Pathway Debug Mode
def getPathwayDebugMode():
  """get pathway debug mode."""
  return loadDefaultServiceConfigurations()["pathway"]["debug"]

# get Pathway Rule
def getPathwayRule():
  """get pathway rule."""
  return loadDefaultServiceConfigurations()["pathway"]["rule"]

# get Pathway HTTP Method
def getPathwayMethod():
  """get pathway method."""
  return loadDefaultServiceConfigurations()["pathway"]["method"]

# get Pathway SSL Mode
def getPathwaySSLMode():
  """get pathway ssl mode."""
  return loadDefaultServiceConfigurations()["pathway"]["ssl"]

# get Pathway SSL Cert
def getPathwaySSLCert():
  """get pathway ssl cert."""
  return loadDefaultServiceConfigurations()["pathway"]["cert"]

# get Pathway SSL Key
def getPathwaySSLKey():
  """get pathway ssl key."""
  return loadDefaultServiceConfigurations()["pathway"]["key"]

# get Pathway Static Directory
def getPathwayStaticPath():
  """get pathway static directory."""
  return loadDefaultServiceConfigurations()["pathway"]["static"]

# get Pathway Templates Directory
def getPathwayTemplatesPath():
  """get pathway templates directory."""
  return loadDefaultServiceConfigurations()["pathway"]["templates"]

# Load ItemDB configurations, with fallback to user home directory
def loadDefaultPermissions(name="graphcode"):
  """Load ItemDB configurations."""

  config_path = join(abspath('./conf'), 'permissions.json')
  if exists(config_path):
    return loadJsonConfig(config_path)
  
  else:
    permissions_dict = {
      "method": "ldap",
      "host": "ldap.moduaws.com",
      "port": "389",
      "principal": "moduaws.com",
      "cmd": {
        "cmd":"/usr/bin/ldapsearch",
        "user":"${CMD} -l 3 -t -H ${HOST} -x -b \"o=${O}\" -s sub \"uid=${USER_NAME}\" 2> /dev/null",
        "group":"${CMD} -x -H ${HOST} -b \"ou=Groups,o=${O}\" -s sub -a always -z 1000 \"(&(cn=${GROUP_NAME}))\" \"memberuid\""
      },
      "primaryAllowedGroup": [
        "moduaws-access"
      ]
    }

    return saveDefaultPermissions(permissions_dict)

# Save default permissions configurations
def saveDefaultPermissions(permissions_dict):
  """Save ItemDB configurations."""
  config_path = join(abspath('./conf'), 'permissions.json')
  with open(config_path, 'w') as fp:
    json.dump(permissions_dict, fp, indent=2)
  
  return permissions_dict

def getPermissionMethod():
  """Get Permission Method."""
  return loadDefaultPermissions()["method"]

def getPermissionHost():
  """Get Permission Host."""
  return loadDefaultPermissions()["host"]

def getPermissionPort():
  """Get Permission Port."""
  return loadDefaultPermissions()["port"]

def getPermissionPrincipal():
  """Get Permission Port."""
  return loadDefaultPermissions()["principal"]

def getPermissionCMD():
  """Get Permission CMD."""
  return loadDefaultPermissions()["cmd"]["cmd"]


def getPermissionUserProfileCMD(userName="${USER_NAME}"):
  """Get Permission User Profile."""

  permission_dict = loadDefaultPermissions()
  method = permission_dict["method"]
  host = permission_dict["host"]
  port = permission_dict["port"]
  principal = permission_dict["principal"]
  permissionCMD = permission_dict["cmd"]["cmd"]
  userProfileCMD = permission_dict["cmd"]["user"]

  if method in ["ldap"]:
    hostURL = f"{method}://{host}:{port}"
  else:
    raise ValueError(f"method:[{method}] is yet to support yet")
    
  
  return userProfileCMD.replace("${CMD}", permissionCMD).replace("${HOST}", hostURL).replace("${PRINCIPAL}", principal).replace("${USER_NAME}", userName)


def getPermissionGroupProfileCMD(groupName="${GROUP_NAME}"):
  """Get Permission User Profile."""

  permission_dict = loadDefaultPermissions()
  method = permission_dict["method"]
  host = permission_dict["host"]
  port = permission_dict["port"]
  principal = permission_dict["principal"]
  permissionCMD = permission_dict["cmd"]["cmd"]
  groupProfileCMD = permission_dict["cmd"]["group"]

  if method in ["ldap"]:
    hostURL = f"{method}://{host}:{port}"
  else:
    raise ValueError(f"method:[{method}] is yet to support yet")
    
  
  return groupProfileCMD.replace("${CMD}", permissionCMD).replace("${HOST}", hostURL).replace("${PRINCIPAL}", principal).replace("${GROUP_NAME}", groupName)

def getPrimaryAllowsGroups():
  """Get primary allows groups."""
  return loadDefaultPermissions()["primaryAllowedGroup"]

def getAllowedGroups(ruleName):
  """Get allowed groups."""
  if ruleName not in loadDefaultPermissions().keys():
    return loadDefaultPermissions()[ruleName]
  else:
    return getPrimaryAllowsGroups()

# Load ItemDB configurations, with fallback to user home directory
def loadItemDBConfiguration(name="itemDB"):
  """Load ItemDB configurations."""

  config_path = join(abspath('./conf'), 'itemDB.json')
  if exists(config_path):
    return loadJsonConfig(config_path)
  
  else:
    itemDBConf_dict = {
      "name": f"{name}",
      "dbRoot":join(loadDefaultServiceConfigurations()["root"],f".{name}"),
      "tables":{
        "itemDB":{}
      },
      "queues":{
        "itemDB":{}
      }
    }

    return saveItemDBConfiguration(itemDBConf_dict)

# Save ItemDB configurations
def saveItemDBConfiguration(itemDBConf_dict):
  """Save ItemDB configurations."""
  config_path = join(abspath('./conf'), 'itemDB.json')
  with open(config_path, 'w') as fp:
    json.dump(itemDBConf_dict, fp, indent=2)
  
  return itemDBConf_dict

def getItemDBPath():
  """Get ItemDB path."""
  itemDBDir = loadItemDBConfiguration()["dbRoot"]
  if not exists(expanduser(itemDBDir)):
    createDir(itemDBDir)
  return itemDBDir

# Load SMTP Server configurations, with fallback to user home directory
def loadSMTPServerConfiguration():
  """Load SMTP Server configurations."""

  config_path = join(abspath('./conf'), 'smtp.json')
  if exists(config_path):
    return loadJsonConfig(config_path)
  
  else:
    smtp_dict = {
      "server": None,
      "username": None,
      "password": None,
      "domainName": None,
      "fromEmailAddress": None,
      "bccEmailAddress": None,
      "registerationEmailAddress": None
    }

    return saveSTMPServerConfiguration(smtp_dict)

# Save STMP Server configurations
def saveSTMPServerConfiguration(smtp_dict):
  """Save STMP Server configurations."""
  config_path = join(abspath('./conf'), 'smtp.json')
  with open(config_path, 'w') as fp:
    json.dump(smtp_dict, fp, indent=2)
  
  return smtp_dict

def getSessionKey():
  """Load Session Key."""
  config_path = join(abspath('./conf'), 'sessionKey.json')
  if exists(config_path):
    return loadJsonConfig(config_path)["key"]
  else:
    return None
  
def saveSessionKey(key):
  """Save Session Key."""
  config_path = join(abspath('./conf'), 'sessionKey.json')
  with open(config_path, 'w') as fp:
    json.dump({"key":key}, fp, indent=2)
  
  return key

def getSMTPServer():
  """Get SMTP Server configurations."""
  return loadSMTPServerConfiguration()["server"]

def getSMTPUsername():
  """Get SMTP Server configurations."""
  return loadSMTPServerConfiguration()["username"]

def getSMTPPassword():
  """Get SMTP Server configurations."""
  return loadSMTPServerConfiguration()["password"]

def getSMTPDomainName():
  """Get SMTP Server configurations."""
  return loadSMTPServerConfiguration()["domainName"]

def getSMTPFromEmailAddress():
  """Get SMTP Server configurations."""
  return loadSMTPServerConfiguration()["fromEmailAddress"]

def getSMTPBCCedEmailAddress():
  """Get SMTP Server configurations."""
  return loadSMTPServerConfiguration()["bccEmailAddress"]

def getSMTPRegisterationEmailAddress():
  """Get SMTP Server configurations."""
  return loadSMTPServerConfiguration()["registerationEmailAddress"]

def initRequest(gc_dict):
  return {
    "async":False,
    "apiName": None,
    "metadata": {
      "awsAccountId":gc_dict["cookies"]["awsAccountId"],
      "userName":gc_dict["cookies"]["userName"],
      "firstName":gc_dict["cookies"]["firstName"],
      "lastName":gc_dict["cookies"]["lastName"],
      "orgName":gc_dict["cookies"]["orgName"],
      "homeURL":gc_dict["homeURL"],
      "ruleName":gc_dict["ruleName"],
      "accessKey":"reserved",
      "secretKey":"reserved",
      "localCookies":loadLocalCookie(),
      },
    "attributes": {
      **gc_dict["form"]
    }
  }

def getInvalidUserErrorMessageLink():
  return "https://w.amazon.com/bin/view/AWS/Teams/TAM/Excellence/moduAWS/DeveloperGuide/Errors/#HInvalidUser"

def getExipiredLocalCookieMessageLink():
  return "https://w.amazon.com/bin/view/AWS/Teams/TAM/Excellence/moduAWS/DeveloperGuide/Errors/#HInvalidUser"

# Load tammyAPIs configurations, with fallback to user home directory
def loadTammyAPIConfiguration():
  """Load SMTP Server configurations."""

  config_path = join(abspath('./conf'), 'tammy.json')
  if exists(config_path):
    return loadJsonConfig(config_path)
  
  else:
    tammy_dict = {
      "maxApiRetries": 10,
      "maxWaitTimeForRateExceeded": 30,
      "maxWaitTimeForExpiredLocalCookie": 3600 * 24,
      "maxPaginatingCount": -1,
      "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.89 Safari/537.36",
      "sessionTimeout": 15,
      "connectionTimeout": 60
    }

    return saveTammyAPIConfiguration(tammy_dict)

# Save STMP Server configurations
def saveTammyAPIConfiguration(tammy_dict):
  """Save STMP Server configurations."""
  config_path = join(abspath('./conf'), 'tammy.json')
  with open(config_path, 'w') as fp:
    json.dump(tammy_dict, fp, indent=2)
  
  return tammy_dict

def getMaxApiRetries():
  """Load MaxApiRetries."""
  config_path = join(abspath('./conf'), 'tammy.json')
  if exists(config_path):
    return loadJsonConfig(config_path)["maxApiRetries"]
  else:
    return 10
  
def getWaitTimeForRateExceeded():
  """Load WaitTimeForRateExceeded."""
  config_path = join(abspath('./conf'), 'tammy.json')
  if exists(config_path):
    return loadJsonConfig(config_path)["maxWaitTimeForRateExceeded"]
  else:
    return 30
  
def getMaxWaitTimeForExpiredLocalCookie():
  """Load WaitTimeForRateExceeded."""
  config_path = join(abspath('./conf'), 'tammy.json')
  if exists(config_path):
    return loadJsonConfig(config_path)["maxWaitTimeForExpiredLocalCookie"]
  else:
    return 3600*24
  
def getMaxPaginatingCount():
  """Load WaitTimeForRateExceeded."""
  config_path = join(abspath('./conf'), 'tammy.json')
  if exists(config_path):
    return loadJsonConfig(config_path)["maxPaginatingCount"]
  else:
    return -1
  
def getUserAgent():
  """Load UserAgent."""
  config_path = join(abspath('./conf'), 'tammy.json')
  if exists(config_path):
    return loadJsonConfig(config_path)["userAgent"]
  else:
    return 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.89 Safari/537.36'

def getConnectionTimeout():
  """Load UserAgent."""
  config_path = join(abspath('./conf'), 'tammy.json')
  if exists(config_path):
    return loadJsonConfig(config_path)["connectionTimeout"]
  else:
    return 15
  
def getSessionTimeout():
  """Load UserAgent."""
  config_path = join(abspath('./conf'), 'tammy.json')
  if exists(config_path):
    return loadJsonConfig(config_path)["sessionTimeout"]
  else:
    return 60
  