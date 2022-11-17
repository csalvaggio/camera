import json

def get_settings(filename):
  f = open(filename)
  settings = json.load(f)
  f.close()

  return settings



if __name__ == '__main__':
  settings = get_settings('../settings/gphoto2_camera_settings.json')

  for label in settings:
    print('{0}: {1}'.format(label, settings[label]))
