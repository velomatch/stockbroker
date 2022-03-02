import pysftp
import os
import requests
import json
from datetime import datetime

class FileImporter(object):
    '''
        config = {'sftp':{'hostname':<hostname>,'Username':<Username>,'Password':<Password>,'Directory':<Directory>},
                  'local':{}
                  }
        Data will be imported from the remote server and will be saved in our server and will delete the remote file.
    '''
    
    def __init__(self, config):
        self.endPointUrl = 'http://178.79.157.171:8000/api/v1/endpoints/'
        self.sftphostname = config['sftp']['hostname']
        self.sftpUsername = config['sftp']['Username']
        self.sftpPassword = config['sftp']['Password']
        self.sftpDirectory = os.path.join('/',config['sftp']['Username'])
        #self.localDirectory = config['local']['Directory']
        self.localdirpath = f"stockupdates/{self.sftphostname}_{self.sftpUsername}/{datetime.now().strftime('%d%m%Y')}"
    
    @property
    def getendPointDetails(self):
        responseRaw = requests.get(url=self.endPointUrl)
        responseRaw.raise_for_status()
        if (responseRaw.headers['Content-Type'] != 'application/json'):
            raise ValueError("Response header not json.")

        responseContent = responseRaw.content
        responseJson = json.loads(responseContent)
        endpoint_data = responseJson['results']
        import pdb;pdb.set_trace()

    @property
    def getdirectory(self):
        
        datadir = os.path.join(self.localdirpath,datetime.now().strftime('%M%H%S'))
        if not os.path.exists(datadir):
            os.makedirs(datadir)
            
        with self.sftp.cd(self.sftpDirectory):
            self.sftp.get_d(self.sftpDirectory, datadir, preserve_mtime=True)

        return f"copied folder - {self.sftpDirectory} to {datadir}"
    
    '''
        Requires path of the file to be imported to the local server.
        ToDo:
        do we need to store the filename mapping inorder to do the investigation later,as we are renaming the files provided?
    '''
    def getfile(self, remotefilepath):
        #Extracting the filename and replacing the file with the newfilename in remote system.
        filename = remotefilepath.split('.')[0].split('/')[-1]
        filextension = remotefilepath.split('.')[-1]
        # [year][month][day][hour][minute][second]
        newfilename = f'{datetime.now().strftime("%Y%m%d%M%H%S")}-{self.sftpUsername}'
        # newfilename = datetime.now().strftime('%M%H%S')
        newfilepath = remotefilepath.replace(filename,newfilename)
        self.sftp.rename(remotefilepath,newfilepath)

        if not os.path.exists(self.localdirpath):
            os.makedirs(self.localdirpath)

        localfilepath = f'{self.localdirpath}/{newfilename}.{filextension}'
        self.sftp.get(newfilepath,localfilepath,preserve_mtime=True)

        self.sftp.remove(newfilepath)
        if not self.sftp.exists(newfilepath):
            print(f"copied file from {self.sftphostname} to {localfilepath} & removed")
            return f"copied file from {self.sftphostname} to {localfilepath} & removed"
        else:
            print(f"copied file from {self.sftphostname} to {localfilepath} but not removed")
            return f"copied file from {self.sftphostname} to {localfilepath} but not removed"
    

    @property
    def getdatafromsftp(self):

        with pysftp.Connection(self.sftphostname, username=self.sftpUsername, password=self.sftpPassword) as self.sftp:

            if self.sftp.exists(self.sftpDirectory):

                if self.sftp.isdir(self.sftpDirectory):
                    files_to_import = len(self.sftp.listdir(self.sftpDirectory))

                    if files_to_import > 0:                        
                        importlogs = []
                        for i,j in enumerate(self.sftp.listdir(self.sftpDirectory)[:3]):
                            # Excluding the files starting with a .
                            if not j.startswith('.'):
                                response = self.getfile(os.path.join(self.sftpDirectory,j))
                                importlogs.append(response)
                        return "\n".join(importlogs)
                    else:
                        return "No files are available to import"

                else:
                    return self.getfile(self.sftpDirectory)

            else:
                return f"File/Directory '{self.sftpDirectory}' not found"