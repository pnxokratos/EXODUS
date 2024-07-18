from subprocess import call

#Class to execute commands on the browser
#It only works on Windows
class PcCommand():
    def __init__(self):
        pass
    
    def open_chrome(self, website):
        website = "" if website is None else website
        #Works for Windows
        call("C:/Program Files/Google/Chrome/Application/chrome.exe " + website)