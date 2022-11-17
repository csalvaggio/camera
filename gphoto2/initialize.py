import sys
import time

import gphoto2 as gp

def initialize(settings, verbose=False):

   if settings:
      # Connect to the gphoto2 camera
      if verbose:
         msg = 'initialize: '
         msg += 'connecting to the gphoto2 camera ...'
         msg += '\n'
         sys.stdout.write(msg)
         sys.stdout.flush()
      connection = gp.Camera()
    
     # Initialize the gphoto2 camera
     if verbose:
        msg = 'initialize: '
        msg += 'Initializing the gphoto2 camera ...'
        msg += '\n'
        sys.stdout.write(msg)
        sys.stdout.flush()
     while True:
        try:
           connection.init()
        except gp.GPhoto2Error as exception:
           if exception.code == gp.GP_ERROR_MODEL_NOT_FOUND:
              msg = 'initialize: '
              msg += 'gphoto2 camera not found, please connect and switch '
              msg += 'on camera'
              msg += '\n'
              sys.stdout.write(msg)
              sys.stdout.flush()
              try:
                 time.sleep(2)
              except KeyboardInterrupt:
                 msg = '\n'
                 msg += 'initialize: '
                 msg += 'CTRL-C detected, exiting ...'
                 msg += '\n'
                 sys.stdout.write(msg)
                 sys.stdout.flush()
                 sys.exit()
              continue
           raise
        break






  else:
    msg = 'initialize: '
    msg += 'camera settings dictionary does not exist, exiting ...'
    msg += '\n'
    sys.stdout.write(msg)
    sys.stdout.flush()
    sys.exit()
