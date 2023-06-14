import os
import argparse
from processing import processing
from os import listdir
from os.path import isfile, join

# 1  Запускаем скрипрт из терминала передавая ему как параметр файл или директорию
def mainscript(fileordir):
# def mainscript(fileordir):
    a_file = os.path.isfile(fileordir)
    a_dir = os.path.isdir(fileordir)
    if a_file is True:
        processing(fileordir)
        # запускаем функцию "processing" (проходит файл построчно и сохраняет результат в json)
    elif a_dir is True:
        onlyfiles = [f for f in listdir(fileordir) if isfile(join(fileordir, f)) and f.endswith(".log")]
        files = [fileordir+i for i in onlyfiles]
        processing(*files)
        # Запускаем функцию "processing" для каждого файла в директории
    else:
        print('Incorrect path')


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Process access.log')
    parser.add_argument('-f', dest='fileordir', action='store', help='Path to logfile or folder with many logfiles')
    args = parser.parse_args()
    mainscript(args.fileordir)
