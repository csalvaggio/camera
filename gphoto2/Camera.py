import json
import os.path
import sys
import time

import gphoto2 as gp

class Camera(object):

   def __init__(self, filename=None):
      self._connection = None
      self._settings = None

      connect_and_initialize()

      if filename:
         ingest_camera_parameters(filename)
         set_camera_parameters()

   def connect_and_initialize(self, verbose=False):
      if self._connection:
         return
      else:
         # Connect to the gphoto2 camera
         if verbose:
            msg = 'initialize: '
            msg += 'connecting to the gphoto2 camera ...'
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

   def ingest_camera_parameters(self, filename):
      if os.path.exists(filename):
         f = open(filename)
         self._settings = json.load(f)
         f.close()
      else:
         msg = '\n'
         msg += 'ingest_camera_parameters: '
         msg += 'camera parameters file not found, exiting ...'
         msg += '\n'
         sys.stdout.write(msg)
         sys.stdout.flush()
         sys.exit()

   def set_camera_parameters(self, filename, verbose=False):
      pass










def set_config(config, parameters, parameter, field_name, error_message):
   try:
      node = gp.check_result(gp.gp_widget_get_child_by_name(config, parameter))
   except:
      msg = 'Specified parameter not found in camera: '
      msg += '{0}'.format(parameter)
      raise ValueError(msg)

   choices = ['implicit auto', 'auto']
   for idx in range(gp.gp_widget_count_choices(node)):
      choice = gp.check_result(gp.gp_widget_get_choice(node, idx))
      choices.append(choice)

   if parameters[field_name] in choices:
      try:
         node.set_value(parameters[field_name])
         parameters['connection'].set_config(config)
      except:
         msg = 'A problem occurred when setting camera configuration: '
         msg += '{0}'.format(parameter)
         raise RuntimeError(msg)
   else:
      raise ValueError(error_message)

def set_parameters_for_gphoto2_camera(parameters):
   if parameters['connection']:
      if parameters['configurable']:
         config = parameters['connection'].get_config()

         parameter = 'capturetarget'
         field_name = 'captureTarget'
         error_message = \
            'Specified capture target is not a valid option for this camera'
         set_config(config, parameters, parameter, field_name, error_message)

         parameter = 'imageformat'
         field_name = 'imageFormat'
         error_message = \
            'Specified image format is not a valid option for this camera'
         set_config(config, parameters, parameter, field_name, error_message)

         parameter = 'iso'
         field_name = 'ISO'
         error_message = \
            'Specified ISO is not a valid option for this camera'
         set_config(config, parameters, parameter, field_name, error_message)

         parameter = 'whitebalance'
         field_name = 'whiteBalance'
         error_message = \
            'Specified white balance is not a valid option for this camera'
         set_config(config, parameters, parameter, field_name, error_message)

         parameter = 'colorspace'
         field_name = 'colorSpace'
         error_message = \
            'Specified color space is not a valid option for this camera'
         set_config(config, parameters, parameter, field_name, error_message)

         parameter = 'exposurecompensation'
         field_name = 'exposureCompensation'
         error_message = \
            'Specified exposure compensation is not valid for this camera'
         set_config(config, parameters, parameter, field_name, error_message)

         parameter = 'focusmode'
         field_name = 'focusMode'
         error_message = \
            'Specified focus mode is not a valid option for this camera'
         set_config(config, parameters, parameter, field_name, error_message)

         parameter = 'continuousaf'
         field_name = 'continuousAF'
         error_message = \
            'Specified continuous auto focus setting not valid for this camera'
         set_config(config, parameters, parameter, field_name, error_message)

         parameter = 'aspectratio'
         field_name = 'aspectRatio'
         error_message = \
            'Specified aspect ratio is not a valid option for this camera'
         set_config(config, parameters, parameter, field_name, error_message)

         parameter = 'autoexposuremode'
         field_name = 'autoExposureMode'
         error_message = \
            'Specified auto exposure mode is not a valid option for this camera'
         set_config(config, parameters, parameter, field_name, error_message)

         parameter = 'drivemode'
         field_name = 'driveMode'
         error_message = \
            'Specified drive mode is not a valid option for this camera'
         set_config(config, parameters, parameter, field_name, error_message)

         parameter = 'picturestyle'
         field_name = 'pictureStyle'
         error_message = \
            'Specified picture style is not a valid option for this camera'
         set_config(config, parameters, parameter, field_name, error_message)

         parameter = 'aperture'
         field_name = 'aperture'
         error_message = \
            'Specified aperture (F-stop) is not a valid option for this camera'
         set_config(config, parameters, parameter, field_name, error_message)

         parameter = 'shutterspeed'
         field_name = 'shutterSpeed'
         error_message = \
            'Specified shutter speed is not a valid option for this camera'
         set_config(config, parameters, parameter, field_name, error_message)

         parameter = 'meteringmode'
         field_name = 'meteringMode'
         error_message = \
            'Specified metering mode is not a valid option for this camera'
         set_config(config, parameters, parameter, field_name, error_message)

   else:
      msg = '*** ERROR *** gPhoto2 camera object not defined'
      msg += '\n'
      sys.stderr.write(msg)
      sys.stderr.flush()
      sys.exit()
