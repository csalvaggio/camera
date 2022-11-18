import json
import os.path
import sys
import time

import gphoto2 as gp

class Camera(object):

   def __init__(self, filename=None, verbose=False):
      self._connection = None
      self._settings = None

      self.connect_and_initialize(verbose=verbose)

      if filename:
         self.ingest_parameters(filename, verbose=verbose)
         self.set_parameters(verbose=verbose)

   def connect_and_initialize(self, verbose=False):
      if self._connection:
         return
      else:
         # Connect to the gphoto2 camera
         if verbose:
            msg = 'initialize: '
            msg += 'Connecting to the gphoto2 camera ...'
            msg += '\n'
            sys.stdout.write(msg)
            sys.stdout.flush()
         self._connection = gp.Camera()

        # Initialize the gphoto2 camera
      if verbose:
         msg = 'initialize: '
         msg += 'Initializing the gphoto2 camera ...'
         msg += '\n'
         sys.stdout.write(msg)
         sys.stdout.flush()
      while True:
         try:
            self._connection.init()
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

   def ingest_parameters(self, filename, verbose=False):
      if os.path.exists(filename):
         if verbose:
           msg = 'ingest_parameters: '
           msg += 'Ingesting gphoto2 camera parameters from '
           msg += '{0} ...'.format(filename)
           msg += '\n'
           sys.stdout.write(msg)
           sys.stdout.flush()
         f = open(filename)
         self._settings = json.load(f)
         f.close()
      else:
         msg = 'ingest_parameters: '
         msg += 'Camera parameters file not found, exiting ...'
         msg += '\n'
         sys.stdout.write(msg)
         sys.stdout.flush()
         sys.exit()

   def _set_config(config, parameter, field_name, error_message):
      try:
         node = \
            gp.check_result(gp.gp_widget_get_child_by_name(config, parameter))
      except:
         msg = 'set_config: '
         msg += 'Specified parameter not found in camera: '
         msg += '{0}'.format(parameter)
         msg += '\n'
         sys.stdout.write(msg)
         sys.stdout.flush()
         sys.exit()

      choices = ['implicit auto', 'auto']
      for idx in range(gp.gp_widget_count_choices(node)):
         choice = gp.check_result(gp.gp_widget_get_choice(node, idx))
         choices.append(choice)

      if self._settings[field_name] in choices:
         try:
            node.set_value(self._settings[field_name])
            self._settings['connection'].set_config(config)
         except:
            msg = 'set_config: '
            msg = 'Problem occurred when setting camera configuration: '
            msg += '{0}'.format(parameter)
            msg += '\n'
            sys.stdout.write(msg)
            sys.stdout.flush()
            sys.exit()
      else:
         sys.stdout.write(error_message)
         sys.stdout.flush()
         sys.exit()

   def set_parameters(self, verbose=False):
      if self._connection:
         config = self._connection.get_config()
         for label in self._settings:
            value = self._settings[label]
            if verbose:
               msg = 'set_parameters: '
               msg += 'Setting "{0}" '.format(label)
               msg += 'to "{0}"'.format(value)
               msg += '\n'
               sys.stdout.write(msg)
               sys.stdout.flush()
            error_message = 'set_parameters: '
            error_message += '{0} '.format(label)
            error_message += 'is not a valid parameter label for this camera'
            _set_config(config, value, label, error_message)
      else:
         msg = 'set_parameters: '
         msg += 'gphoto2 camera object not defined'
         msg += '\n'
         sys.stdout.write(msg)
         sys.stdout.flush()
         sys.exit()

   def capture():
      pass



if __name__ == '__main__':
   filename = 'settings/canon_eos_rebel_xsi.json'
   c = Camera(filename, verbose=True)
