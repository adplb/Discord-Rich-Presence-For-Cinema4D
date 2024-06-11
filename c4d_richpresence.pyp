import os
import c4d
from c4d.threading import C4DThread
from pypresence import Presence
from c4d import plugins, utils, gui
import time
import asyncio

# Current plugin version - 1.0.1 - Made by Jonte#4200 and updated to R2024 by adrianlarsson
# Global
RPC = Presence("YOUR_VALID_CLIENT_ID")
project_name = ""
thread = None
starttime = time.time()
# Plugin ID from Maxon's PluginCafe Forum
PLUGIN_ID = 1057290

class BGThread(c4d.threading.C4DThread):
    def Main(self):
        # Removed version check to make it version-agnostic
        while True:
            if self.TestBreak():
                return
            asyncio.run(Update())
            time.sleep(15)

async def Update():
    doc = c4d.documents.GetActiveDocument()
    version = c4d.GetC4DVersion()
    global project_name
    global starttime
    project_name = doc.GetDocumentName()
    if not project_name:
        return
    try:
        await RPC.update(state=project_name, large_image="logo", large_text=f"R{str(version)[:2]}", start=starttime)
    except Exception as e:
        print(f"Error updating RPC: {e}")

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
        asyncio.run(Update())

# Main function
def main():
    print("RPC Connected")
    RPC.connect()

# Execute main()
if __name__=='__main__':
    main()
