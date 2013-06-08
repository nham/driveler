import sys
import os, shutil, subprocess
from glob import glob

site_title = 'wabbo'
include_dir = 'includes/'
out_folder = '_out/'


fname_no_ext = lambda fn: fn[:fn.index('.')]

def pandocConvert(pathto, fname):
    dothtml = fname[:fname.index('.')] + '.html'
    in_file = pathto + fname
    out_file = out_folder + pathto + dothtml

    pandoc_call = ['pandoc', '-s', in_file, '-t', 'html5', '-o', out_file,
                          '--include-in-header', include_dir+'header.html',
                          '--include-before-body', include_dir+'cover.html',
                          '--include-after-body', include_dir+'footer.html',
                          '--mathjax', '--smart', '--title-prefix', site_title]

    p = subprocess.call(pandoc_call)

    return


def isPage(fname):
    pages = ['.md', '.rst']
    return ('.' in fname) \
        and (fname[fname.index('.'):] in pages)


def convert_folder(folder, wl=None, bl=None):
    if folder == '':
        folder = './' 

    if wl is not None:
        filter = lambda fn: fname_no_ext(fn) in wl
    else:
        filter = lambda fn: True

    if bl is not None:
        filter = lambda fn: fname_no_ext(fn) not in bl
    else:
        filter = lambda fn: True


    out_path = out_folder + folder

    for fname in os.listdir(folder):
        if isPage(fname) and filter(fname):
            if not os.path.exists(out_path):
                os.makedirs(out_path)

            pandocConvert(folder, fname)
    

# Compilation script begins here
convert_folder('', bl=['readme'])
convert_folder('blov/')
convert_folder('notes/', wl=['linalg'])
