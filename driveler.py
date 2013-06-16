import os, shutil, subprocess
import logging
import argparse
import sqlite3

class Comptroller:
    def __init__(self):
        self.conn = sqlite3.connect('driveler.sqlite')
        c = self.conn.cursor()
        sql = "SELECT 1 FROM sqlite_master WHERE type='table' AND name='mtimes'"
        c.execute(sql)
        
        if c.fetchone() is None:
            self.initdb()


    def initdb(self):
        init_sql = """
            CREATE TABLE mtimes (
              id integer primary key autoincrement,
              path text UNIQUE,
              mtime text);"""

        self.conn.executescript(init_sql)
        self.conn.commit()
        logging.info('sqlite database initialized')


    def dump(self):
        c = self.conn.cursor()
        sql = 'SELECT * FROM mtimes'
        c.execute(sql)
        return c.fetchall()

    def get_mtime(self, path):
        c = self.conn.cursor()
        sql = 'SELECT mtime FROM mtimes WHERE path = ?'
        c.execute(sql, (path,))
        return c.fetchone()
        

    def set_mtime(self, path, mtime):
        c = self.conn.cursor()

        if self.get_mtime(path) is None:
            sql = 'INSERT INTO mtimes (path, mtime) VALUES (?, ?)'
            c.execute(sql, (path, mtime))
        else:
            sql = 'UPDATE mtimes SET mtime = ? where path = ?'
            c.execute(sql, (mtime, path))

        self.conn.commit()

    def close(self):
        self.conn.close()



class Driveler:
    def __init__(self):
        args = self.parse_arguments()
        logging.basicConfig(level=args.verbosity)
        self.force_compile = args.force

        if self.force_compile is True:
            logging.info('Forcing compilation of all files.')

        self.comp = Comptroller()

    def out_path(self, relpath):
        return self.out_folder + relpath

    def incl_path(self, relpath):
        return self.include_dir + relpath

    def convert_file(self, pathto, fname):
        dothtml = fname[:fname.index('.')] + '.html'
        in_file = pathto + fname
        out_file = self.out_path(pathto + dothtml)

        pandoc_call = ['pandoc', '-s', in_file, 
                      '-t', 'html5+pandoc_title_block',
                      '-o', out_file,
                      '--include-in-header', self.incl_path('in_header.html'),
                      '--include-before-body', self.incl_path('before_body.html'),
                      '--include-after-body', self.incl_path('after_body.html'),
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
                new_mtime = self.changed(folder, fname)

                if self.force_compile is True or new_mtime is not False:
                    self.create_folder_if_not_exists(new_out_folder)
                    self.convert_file(folder, fname)

                    if new_mtime is not False:
                        self.comp.set_mtime(folder+fname, new_mtime)
                else:
                    logging.info('mtime for {0} is not newer than last compile.'.format(folder+fname))


    def changed(self, folder, fname):
        path = folder+fname
        logged_mtime = self.comp.get_mtime(path)

        if logged_mtime is not None:
            logged_mtime = logged_mtime[0]

        new_mtime = os.path.getmtime(path)

        if logged_mtime is None or new_mtime > float(logged_mtime):
            return str(new_mtime)
        else:
            return False



    def create_folder_if_not_exists(self, folder):
        if not os.path.exists(folder):
            logging.info('folder {0} does not exist, creating'.format(folder))
            os.makedirs(folder)
            

    def copy_folder(self, folder):
        new_out_folder = self.out_path(folder)

        self.create_folder_if_not_exists(new_out_folder)

        for fname in os.listdir(folder):
            new_mtime = self.changed(folder, fname)

            if self.force_compile is True or new_mtime is not False:
                site_file = folder + fname
                out_file =  new_out_folder + fname
                shutil.copy(site_file, out_file)

                if new_mtime is not False:
                    self.comp.set_mtime(folder+fname, new_mtime)

                logging.info('copied {0} to {1}'.format(site_file, out_file))
            else:
                logging.info('mtime for {0} is not newer than last compile.'.format(folder+fname))


    def parse_arguments(self):
        parser = argparse.ArgumentParser(description="""A stupid 
        static site generator/glorified pandoc wrapper.""",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

        parser.add_argument('-f', '--force', action='store_const',
            const=True, dest='force',
            help='Force recompilation of all files.')

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
