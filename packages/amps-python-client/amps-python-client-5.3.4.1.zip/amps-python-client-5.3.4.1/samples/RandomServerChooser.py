from AMPS import DefaultAuthenticator, DisconnectedException
import random

class RandomServerChooser:

  def __init__(self, seed = None):
     self.servers = []
     self.current_server = None
     self.random = random.Random(seed)
     self.authenticator = DefaultAuthenticator()

  def add(self, server):
     self.servers.append(server)

  def get_current_uri(self):
     if len(self.servers) == 0:
        return None

     if self.current_server == None:
        self.set_current_server()
 
     return self.current_server

  def next(self):
     self.set_current_server()  

  def get_current_authenticator(self):
    return self.authenticator

  def report_failure(self, exception, info):
    if ( (type(exception) is DisconnectedException) == False):
       self.next() 

  def report_success(self, info):
      pass

  def set_current_server(self):
     if len(self.servers) == 0:
        return None

     self.current_server = self.random.choice(self.servers) 
