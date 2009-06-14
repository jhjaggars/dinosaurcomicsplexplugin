from PMS import Plugin, Log, DB, Thread, XML, HTTP, JSON, RSS, Utils
from PMS.MediaXML import MediaContainer, DirectoryItem, PhotoItem

PLUGIN_PREFIX   = "/photos/dinosaurcomics"
BASE_URL = "http://www.qwantz.com"
CACHE_TIME = 3600
archived = "new"

def Start():
    Plugin.AddRequestHandler(PLUGIN_PREFIX, HandlePhotosRequest, "dinosaurcomics", "icon-default.png", "art-default.jpg")
    Plugin.AddViewGroup("InfoList", viewMode="InfoList", contentType="items")

def HandlePhotosRequest(pathNouns, count):
    dir_ = MediaContainer("art-default.jpg", "InfoList", "dinosaurcomics")
    global archived
    if archived == "new":
        archived = XML.ElementFromString(HTTP.GetCached(BASE_URL + "/archive.php", CACHE_TIME), True).xpath('//a[contains(@href, "www.qwantz.com/index.php?comic=")]')

    for item in archived[count*10:count*10+10]:
        try:
            title = item.text
            imgHTML = XML.ElementFromString(HTTP.GetCached(item.get("href"), CACHE_TIME), True).xpath('//img[contains(@class, "comic")]')[0]
            img = imgHTML.get("src")
            desc = imgHTML.get("title")
            ph = PhotoItem(img, title, desc, img)
            dir_.AppendItem(ph)
        except Exception, e:
            Log.Add("Exception caught when trying to fetch comic:")
            Log.Add("\t" + str(e))
            Log.Add("\t" + item.get("href"))

    dir_.AppendItem(DirectoryItem("next10","Next 10...",""))

    return dir_.ToXML()
