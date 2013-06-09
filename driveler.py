import os, shutil, subprocess
import logging
import argparse

class Driveler:
    def __init__(self):
        args = self.parse_arguments()
        logging.basicConfig(level=args.verbosity)

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
        logging.info('generated page {0}'.format(out_file))
        return


    def is_page(self, fname):
        pages = ['.md', '.rst']
        return ('.' in fname) \
            and (fname[fname.index('.'):] in pages)


    def convert_folder(self, folder, wl=None, bl=None):
        if folder == '':
            folder = './' 

        fname_no_ext = lambda fn: fn[:fn.index('.')]

        if wl is not None:
            filter = lambda fn: fname_no_ext(fn) in wl
        elif bl is not None: 
            filter = lambda fn: fname_no_ext(fn) not in bl
        else:
            filter = lambda fn: True

        new_out_folder = self.out_path(folder)

        for fname in os.listdir(folder):
            if self.is_page(fname) and filter(fname):
                self.create_folder_if_not_exists(new_out_folder)
                self.convert_file(folder, fname)


    def create_folder_if_not_exists(self, folder):
        if not os.path.exists(folder):
            logging.info('folder {0} does not exist, creating'.format(folder))
            os.makedirs(folder)
            

    def copy_folder(self, folder):
        new_out_folder = self.out_path(folder)

        self.create_folder_if_not_exists(new_out_folder)

        for fname in os.listdir(folder):
            site_file = folder + fname
            out_file =  new_out_folder + fname
            shutil.copy(site_file, out_file)
            logging.info('copied {0} to {1}'.format(site_file, out_file))


    def parse_arguments(self):
        parser = argparse.ArgumentParser(description="""A stupid 
        static site generator/glorified pandoc wrapper.""",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

        parser.add_argument('-v', '--verbose', action='store_const',
            const=logging.INFO, dest='verbosity',
            help='Show all messages.')

        parser.add_argument('-q', '--quiet', action='store_const',
            const=logging.CRITICAL, dest='verbosity',
            help='Show only critical errors.')

        parser.add_argument('-D', '--debug', action='store_const',
            const=logging.DEBUG, dest='verbosity',
            help='Show all message, including debug messages.')

        return parser.parse_args()
