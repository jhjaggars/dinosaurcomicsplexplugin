from PMS import Plugin, Log, DB, Thread, XML, HTTP, JSON, RSS, Utils
from PMS.MediaXML import MediaContainer, DirectoryItem, PhotoItem

PLUGIN_PREFIX   = "/photos/dinosaurcomics"
BASE_URL = "http://www.qwantz.com"
CACHE_TIME = 3600
archived = "new"

####################################################################################################
def Start():
  Plugin.AddRequestHandler(PLUGIN_PREFIX, HandlePhotosRequest, "dinosaurcomics", "icon-default.png", "art-default.jpg")
  Plugin.AddViewGroup("InfoList", viewMode="InfoList", contentType="items")

####################################################################################################
def HandlePhotosRequest(pathNouns, count):
  dir_ = MediaContainer("art-default.jpg", "InfoList", "dinosaurcomics")
  global archived
  if archived == "new":
      archived = XML.ElementFromString(HTTP.GetCached(BASE_URL + "/archive/list.html", CACHE_TIME), True).xpath('//li//a[1]')[::-1]

  for item in archived[count*10:count*10+10]:
    title = item.text
    imgHTML = XML.ElementFromString(HTTP.GetCached(BASE_URL + item.get("href"), CACHE_TIME), True).xpath('//img[contains(@src, "comics")]')[0]
    img = imgHTML.get("src")
    desc = imgHTML.get("title")
    ph = PhotoItem(img, title, desc, img)
    dir_.AppendItem(ph)
  dir_.AppendItem(DirectoryItem("next10","Next 10...",""))

  return dir_.ToXML()
