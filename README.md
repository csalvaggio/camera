# INTRODUCTION #
This repository defines a class that attempts to abstract the GPhoto2 camera module.

# INSTALLATION #
This is setup to be a Python module.  Clone this repository in your PYTHONPATH directory.  The module may be imported with "import camera" in any of your Python codes.

# DEPENDENCIES #
* datetime
* json
* os.path
* sys
* time

Non-Standard Modules
* gphoto2

   * Make sure the gphoto2 command-line program and library are installed on your machine.
   * Install the Python gphoto2 binding ...

         pip3 install gphoto2

# TESTING #
Each file contains a test harness.  Testing may be done by typing "python <file>.py".  On some machine, these routines may need to be execute with root privileges.

# NOTES #
To list the camera's parameter field names, issue the command ...

      gphoto2 --list-config

(you may need to use sudo on the above command)
