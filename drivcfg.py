from driveler import Driveler

d = Driveler()
d.site_title = 'site'
d.include_dir = 'includes/'
d.out_folder = '_out/'


d.copy_folder('css/')
d.convert_folder('', bl=['readme'])
d.convert_folder('blov/')
d.convert_folder('notes/', wl=['linalg'])
