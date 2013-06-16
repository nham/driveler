from driveler import Driveler

d = Driveler()
d.site_title = 'site'
d.include_dir = 'includes/'
d.css_file = '/css/style.css'


d.copy_folder('css/')
d.convert_folder('', bl=['readme'])
d.convert_folder('blog/')
d.convert_folder('notes/', wl=['linalg'])
