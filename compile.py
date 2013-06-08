import sys
import os, shutil, subprocess
from glob import glob

site_title = 'wabbo'
include_dir = 'includes/'
exclude_files = ['readme.md']
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
    #return bytes.decode(p.communicate(bytes(source, 'UTF-8'))[0])


def isPage(fname):
    pages = ['.md', '.rst']
    return ('.' in fname) \
        and (fname[fname.index('.'):] in pages) \
        and fname not in exclude_files



# Compilation script begins here
for fname in os.listdir('./'):
    if isPage(fname):
        pandocConvert('', fname)


for fname in os.listdir('./blov/'):
    if isPage(fname):
        pandocConvert('blov/', fname)

for fname in os.listdir('./notes/'):
    if isPage(fname) and fname_no_ext(fname) in ['linalg']:
        out_dir = out_folder + 'notes/'
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        pandocConvert('notes/', fname)
