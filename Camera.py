import json
import os.path
import sys
import time

import gphoto2 as gp

class Camera(object):

   def __init__(self, filename=None, verbose=False):
      self._connection = None
      self._settings = None

      self._connect_and_initialize(verbose=verbose)

      if filename:
         self.ingest_parameters(filename, verbose=verbose)

      if self._settings:
         self.set_parameters(verbose=verbose)

   def _connect_and_initialize(self, verbose=False):
      if self._connection:
         return
      else:
         # Connect to the gphoto2 camera
         if verbose:
            msg = 'initialize: '
            msg += 'Connecting to the gphoto2 camera'
            msg += '\n'
            sys.stdout.write(msg)
            sys.stdout.flush()
         self._connection = gp.Camera()

      # Initialize the gphoto2 camera
      if verbose:
         msg = 'initialize: '
         msg += 'Initializing the gphoto2 camera'
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
               sys.stderr.write(msg)
               sys.stderr.flush()
               try:
                  time.sleep(2)
               except KeyboardInterrupt:
                  msg = '\n'
                  msg += 'initialize: '
                  msg += 'CTRL-C detected, exiting'
                  msg += '\n'
                  sys.stderr.write(msg)
                  sys.stderr.flush()
                  sys.exit()
               continue
            raise
         break

   def ingest_parameters(self, filename, verbose=False):
      if os.path.exists(filename):
         if verbose:
           msg = 'ingest_parameters: '
           msg += 'Ingesting gphoto2 camera parameters from'
           msg += '\n'
           msg += '   {0}'.format(filename)
           msg += '\n'
           sys.stdout.write(msg)
           sys.stdout.flush()
         try:
            f = open(filename)
            self._settings = json.load(f)
            f.close()
         except:
            msg = 'ingest_parameters: '
            msg += 'Possible syntax error encountered in JSON file'
            msg += '\n'
            sys.stderr.write(msg)
            sys.stderr.flush()
            sys.exit()
      else:
         msg = 'ingest_parameters: '
         msg += 'Camera parameters file not found, exiting'
         msg += '\n'
         sys.stderr.write(msg)
         sys.stderr.flush()
         sys.exit()

   def _set_config(self, config, field, value, error_message):
      try:
         node = gp.check_result(gp.gp_widget_get_child_by_name(config, field))
      except:
         msg = 'set_config: '
         msg += 'The parameter field "{0}" '.format(field)
         msg += 'was not found on attached camera'
         msg += '\n'
         sys.stderr.write(msg)
         sys.stderr.flush()
         sys.exit()

      choices = ['implicit auto', 'auto']
      for idx in range(gp.gp_widget_count_choices(node)):
         choice = gp.check_result(gp.gp_widget_get_choice(node, idx))
         choices.append(choice)

      if value in choices:
         try:
            node.set_value(value)
            self._connection.set_config(config)
         except:
            msg = 'set_config: '
            msg += 'Unknown error occurred while setting "{0}"'.format(field)
            msg += '\n'
            sys.stderr.write(msg)
            sys.stderr.flush()
            sys.exit()
      else:
         msg = 'set_config: '
         msg += 'The provided value "{0}" '.format(value)
         msg += 'is not a valid choice for the '
         msg += '\n'
         msg += '            parameter field "{0}" '.format(field)
         msg += 'on attached camera'
         msg += '\n'
         sys.stderr.write(msg)
         sys.stderr.flush()
         sys.exit()

   def set_parameters(self, verbose=False):
      if self._connection:
         config = self._connection.get_config()
         for field in self._settings:
            value = self._settings[field]
            if verbose:
               msg = 'set_parameters: '
               msg += 'Setting "{0}" '.format(field)
               msg += 'to "{0}"'.format(value)
               msg += '\n'
               sys.stdout.write(msg)
               sys.stdout.flush()
            self._set_config(config, field, value, None)
      else:
         msg = 'set_parameters: '
         msg += 'gphoto2 camera not found/connected'
         msg += '\n'
         sys.stderr.write(msg)
         sys.stderr.flush()
         sys.exit()

   def capture(self, basename=None, delete=False, verbose=False):
      """
      IMPORTANT NOTE:
      When using this capture method, the camera must be set to capture RAW or
      JPEG only, NOT BOTH
      """
      # Capture image from gphoto2 camera
      if verbose:
         msg = 'capture: '
         msg += 'Triggering camera'
         msg +=  '\n'
         sys.stdout.write(msg)
         sys.stdout.flush()
      try:
         camera_filepath = \
            self._connection.capture(gp.GP_CAPTURE_IMAGE)
      except:
         msg = 'capture: '
         msg += 'gphoto2 capture unsuccessful, try power cycling the camera'
         msg += '\n'
         sys.stderr.write(msg)
         sys.stderr.flush()
         return None

      # Add extension to the basename to match the image file on the
      # camera's SD card
      filepath = None
      if basename:
         extension = os.path.splitext(camera_filepath.name)[1].lower()
         filepath = basename + extension

         # Extract image from the camera's SD card and save to local disk
         if verbose:
            msg = 'capture: '
            msg += 'Extracting image from camera\'s SD card to'
            msg += '\n'
            msg += '   {0}'.format(filepath)
            msg += '\n'
            sys.stdout.write(msg)
            sys.stdout.flush()
         try:
            camera_file = self._connection.file_get(camera_filepath.folder,
                                                    camera_filepath.name,
                                                    gp.GP_FILE_TYPE_NORMAL)
         except:
            msg = 'capture: '
            msg += 'Image extraction from camera\'s SD card was unsuccessful'
            msg += '\n'
            sys.stderr.write(msg)
            sys.stderr.flush()
            return None

         if verbose:
            msg = 'capture: '
            msg += 'Saving extracted image to local disk'
            msg += '\n'
            sys.stdout.write(msg)
            sys.stdout.flush()
         try:
            camera_file.save(filepath)
         except:
            msg = 'capture: '
            msg += 'The save operation to local disk was unsuccessful'
            msg += '\n'
            sys.stderr.write(msg)
            sys.stderr.flush()
            return None

      # Delete image from the camera's SD card
      if delete:
         if verbose:
            msg = 'capture: '
            msg += 'Deleting image from camera\'s SD card'
            msg += '\n'
            sys.stdout.write(msg)
            sys.stdout.flush()
         try:
            self._connection.file_delete(camera_filepath.folder,
                                         camera_filepath.name)
         except:
            msg = 'capture: '
            msg += 'Image deletion operation from camera\'s SD card was '
            msg += 'unsuccessful'
            msg += '\n'
            sys.stderr.write(msg)
            sys.stderr.flush()
            return None

      # Clean up memory
      if basename:
         if verbose:
            msg = 'capture: '
            msg += 'Cleaning up memory'
            msg += '\n'
            sys.stdout.write(msg)
            sys.stdout.flush()
         del camera_file
         del camera_filepath

      if verbose:
         msg = 'capture: '
         msg += 'Complete'
         msg += '\n'
         sys.stdout.write(msg)
         sys.stdout.flush()

      return filepath



if __name__ == '__main__':
   import camera
   import datetime

   camera_parameter_filename = \
      'camera_parameter_files/nikon_dsc_d3500.json'
#      'camera_parameter_files/canon_eos_rebel_xsi.json'

   verbose = True
   delete_from_sd_card = True

   extracted_basename = \
      datetime.datetime.utcnow().isoformat(timespec='milliseconds') + 'Z'
   extracted_basename = extracted_basename.replace(":", "-" )
   extracted_basename = extracted_basename.replace(".", "-" )

   c = camera.Camera(camera_parameter_filename, verbose=verbose)

   filepath = \
      c.capture(basename=extracted_basename, \
                delete=delete_from_sd_card, \
                verbose=verbose)
