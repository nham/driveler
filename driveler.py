import sys
import os, shutil, subprocess

fname_no_ext = lambda fn: fn[:fn.index('.')]

class Driveler:
    def __init__(self):
        pass

    def out_path(self, relpath):
        return self.out_folder + relpath

    def incl_path(self, relpath):
        return self.include_dir + relpath

    def convert_file(self, pathto, fname):
        dothtml = fname[:fname.index('.')] + '.html'
        in_file = pathto + fname
        out_file = self.out_path(pathto + dothtml)

        pandoc_call = ['pandoc', '-s', in_file, '-t', 'html5', '-o', out_file,
                      '--include-in-header', self.incl_path('header.html'),
                      '--include-before-body', self.incl_path('cover.html'),
                      '--include-after-body', self.incl_path('footer.html'),
                      '--mathjax', '--smart',
                      '--title-prefix', self.site_title]

        p = subprocess.call(pandoc_call)
        return


    def is_page(self, fname):
        pages = ['.md', '.rst']
        return ('.' in fname) \
            and (fname[fname.index('.'):] in pages)


    def convert_folder(self, folder, wl=None, bl=None):
        if folder == '':
            folder = './' 

        if wl is not None:
            filter = lambda fn: fname_no_ext(fn) in wl
        elif bl is not None: 
            filter = lambda fn: fname_no_ext(fn) not in bl
        else:
            filter = lambda fn: True

        new_out_folder = self.out_path(folder)

        for fname in os.listdir(folder):
            if self.is_page(fname) and filter(fname):
                if not os.path.exists(new_out_folder):
                    os.makedirs(new_out_folder)

                self.convert_file(folder, fname)


    def copy_folder(self, folder):
        new_out_folder = self.out_path(folder)

        if not os.path.exists(new_out_folder):
            os.makedirs(new_out_folder)
            
        for fname in os.listdir(folder):
            site_file = folder + fname
            out_file =  new_out_folder + fname
            shutil.copy(site_file, out_file)
