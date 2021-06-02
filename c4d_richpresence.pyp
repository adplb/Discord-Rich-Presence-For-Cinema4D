import os
import c4d
from c4d.threading import C4DThread
from pypresence import Presence
from c4d import plugins, utils
import time

#Current plugin version - 1.0 - Made by Jonte#4200
#Global
RPC = Presence("843479489245872130")
project_name = ""
thread = None
starttime = time.time()
#Plugin ID from Maxon's PluginCafe Forum
PLUGIN_ID = 1057290

class BGThread(c4d.threading.C4DThread):
    def Main(self):
        while True:
            if self.TestBreak():
                return
            Update()
            time.sleep(15)

def Update():
    doc = c4d.documents.GetActiveDocument()
    global project_name
    global starttime
    project_name = doc.GetDocumentName()
    if not project_name:
        return
    RPC.update(state=project_name, large_image="logo", start=starttime)

def PluginMessage(id, data):
    global thread
    global starttime
    if id == c4d.C4DPL_PROGRAM_STARTED:
        thread = BGThread()
        thread.Start()
    elif id == c4d.C4DPL_ENDPROGRAM:
        thread.End()
        RPC.close()
    elif id == c4d.C4DPL_RELOADPYTHONPLUGINS:
        Update()

# Main function
def main():
    print("RPC Connected")
    RPC.connect()

# Execute main()
if __name__=='__main__':
    main()