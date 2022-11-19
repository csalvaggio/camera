# INTRODUCTION #
This repository defines a class that abstracts the GPhoto2 camera module.

# INSTALLATION #
This is setup to be a Python module.  Clone this repository in your PYTHONPATH directory.  The module may be imported with "import camera" in any of your Python codes.

# DEPENDENCIES #
* json
* os.path
* sys
* time

Non-Standard Modules
* gphoto2

   * Make sure the gphoto2 command-line program and library are installed on your machine
   * Install the Python gphoto2 binding ...

            pip3 install gphoto2

# TESTING #
Each file contains a test harness.  Testing may be done by typing "python3 \<file\>.py".  On some machine, these routines may need to be execute with root privileges (sudo).

# NOTES #
To list the camera's parameter field names, issue the following instruction on the command line ...

      gphoto2 --list-config

(you may need to use sudo on the above command on some machines).

# USAGE #
The *Camera* class may be imported as

    import camera

and a *Camera* object instantiated as

    c = camera.Camera(camera_parameter_filename)

where the *camera\_parameter\_filename* is a string object containing the path to the JSON file containing the camera configuration parameters.

This member function has one optional parameter to adjust it's behavior ...

    verbose=True|False

where *verbose* is a boolean that indicates whether the member function should be "chatty" during it's operation (useful during debugging).

The camera configuration JSON file, for a Canon EOS Rebel Xsi, looks like ... 

    {
       "capturetarget": "Memory card",
       "imageformat": "RAW",
       "iso": "Auto",
       "whitebalance": "Auto",
       "colorspace": "AdobeRGB",
       "exposurecompensation": "0",
       "focusmode": "Manual",
       "autoexposuremode": "TV",
       "drivemode": "Single",
       "picturestyle": "Neutral",
       "aperture": "implicit auto",
       "shutterspeed": "1/125",
       "meteringmode": "Center-weighted average"
    }

If this *camera\_parameter\_filename* parameter is omitted from the call to the constructor, then one can programatically modify the settings dictionary (private data member) for the *Camera* object, specifically ...

    c._settings = {"capturetarget": "Memory card",
                   "imageformat": "RAW",
                   "iso": "Auto",
                   "whitebalance": "Auto",
                   "colorspace": "AdobeRGB",
                   "exposurecompensation": "0",
                   "focusmode": "Manual",
                   "autoexposuremode": "TV",
                   "drivemode": "Single",
                   "picturestyle": "Neutral",
                   "aperture": "implicit auto",
                   "shutterspeed": "1/125",
                   "meteringmode": "Center-weighted average"}

If this settings dictionary is create/modified programatically, the program must call 

    self.set_parameters()

to enact these settings on the camera.

This member function has one optional parameter to adjust it's behavior ...

    verbose=True|False

where *verbose* is a boolean that indicates whether the member function should be "chatty" during it's operation (useful during debugging).

Once the camera is configured, a photograph may be captured by issuing the command ...

    filepath = c.capture()

This member function has several optional parameters to adjust it's behavior ...

    basename=<string>

where \<sting\> is a string object containing the basename for the filename to extract the photograph to in the local filesystem from the camera.  The default value is *None* which indicates that the image is not to be extracted from the camera.

    delete=True|False

where *delete* is a boolean that indicates whether the file should be deleted from the camera's SD card once the capture operation is completed.  The default behavior is to keep the file on the SD card.

    verbose=True|False

where *verbose* is a boolean that indicates whether the member function should be "chatty" during it's operation (useful during debugging).
