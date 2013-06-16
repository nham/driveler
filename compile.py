from driveler import Driveler

d = Driveler()
d.site_title = 'Driveler'
d.include_dir = 'includes/'
d.css_file = '/css/style.css'
d.out_folder = 'docs/'


d.copy_folder('css/')
d.convert_folder('', bl=['readme'])
