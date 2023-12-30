import glob
import os
import zipfile

import fire
from pypdf import PdfReader


def test_pdf(filepath):
    try:
        PdfReader(filepath)
    except:
        return False
    return True


def test_epub(filepath):
    try:
        the_zip_file = zipfile.ZipFile(filepath)
        ret = the_zip_file.testzip()
        if ret is not None:
            return False
        return True
    except:
        return False


def validate_files(path, report_path):
    with open(report_path, 'w') as report_file:
        for infile in glob.iglob(os.path.join(path, '*.*')):
            filename = os.path.basename(infile)
            _, extension = infile.rsplit('.', 1)
            match extension:
                case 'pdf':
                    if not test_pdf(infile):
                        report_file.write(filename + '\n')
                        print('broken', infile)
                        continue
                case 'epub':
                    if not test_epub(infile):
                        report_file.write(filename + '\n')
                        print('broken', infile)
                        continue
                case _:
                    print('unknown file', filename)
                    continue
            print('tested', infile)


def main():
    fire.Fire(validate_files)
