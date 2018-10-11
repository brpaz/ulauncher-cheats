""" Cheats manager module """

import os
import errno
import glob2


class CheatsManager(object):
    """ Class that manages the cheat sheets """

    def __init__(self, cheats_dir, urls_file=''):
        """ Constructor method"""
        self.cheats_dir = cheats_dir
        self.urls_file = urls_file
        self.create_default_cheats_dir()

    def find(self, query=None):
        """ Llooks for a cheat sheet, optionally filtered by the query argument """

        files = glob2.glob('%s/**/*' % self.cheats_dir)
        result = []

        if os.path.isfile(self.urls_file):
            with open(self.urls_file) as f:
                try:
                    for line in f.readlines():
                        name, url = line.split()
                except ValueError:
                    result.append({
                        'path': '',
                        'name': '',
                        'normalized_name': '!!! URLs files formatting error !!!'
                    })
                else:
                    result.append({
                        'path': url,
                        'name': name,
                        'normalized_name': name,
                        'url': True
                    })

        for file_path in files:
            if file_path != self.urls_file:
                filename = os.path.basename(file_path)
                filename_without_ext = os.path.splitext(
                    filename)[0].replace('-', ' ').title()

                if not os.path.isfile(file_path):
                    continue
                if query and query.lower() not in filename.lower():
                    continue

                result.append({
                    'path': file_path,
                    'name': filename,
                    'normalized_name': filename_without_ext
                })

        return result

    def create_default_cheats_dir(self):
        """ creates the cheats dir if it does not exist """
        try:
            os.makedirs(self.cheats_dir)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(self.cheats_dir):
                pass
            else:
                raise

    def set_cheats_dir(self, path):
        """ Sets the cheats dir, overriding the default one """
        self.cheats_dir = path

    def set_urls_file(self, path):
        """ Sets the urls file path, if file exists """
        print('sets_urls_file:', path)
        if os.path.exists(path):
            self.urls_file = path
        elif os.path.exists(os.path.join(self.cheats_dir, path)):
            self.urls_file = os.path.join(self.cheats_dir, path)
        else:
            self.urls_file = ''
        print(self.urls_file)
