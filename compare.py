import subprocess
import configparser
import argparse


# svn.exe, ifcmp60.exe and WinMergeU.exe should be defined under the PATH environment variable

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('form_name', type=str,
                        help='Name of the form, whose revisions will be compared against each other.' +
                             'form should be given without the .fmb extension')
    parser.add_argument('revision_from', type=int, help='base revision')
    parser.add_argument('revision_to', type=int, help='revision that first one will be compared against')
    args = parser.parse_args()
    # see example.ini

    config = configparser.ConfigParser()
    config.read('config.ini')

    forms_path = config['app']['forms_path']

    # todo: consider renaming of variables
    form_name = args.form_name.upper()
    form_location = forms_path + form_name
    svn_command = ['svn', 'update', form_location + '.FMB', '-r']
    object_list_command = ['ifcmp60', 'MODULE=' + form_location,
                           'MODULE_TYPE=FORM', 'logon=NO', 'forms_doc=YES']

    output_files = ['from.txt', 'to.txt']
    revisions = [args.revision_from, args.revision_to]

    subprocess.run(['cmd', '/c', 'cd', forms_path])
    for file_name, revision_number in zip(output_files, revisions):
        subprocess.run(['cmd', '/c', 'del', forms_path + file_name])
        subprocess.run(svn_command + [revision_number])
        subprocess.run(object_list_command)
        subprocess.run(['cmd', '/c', 'rename', form_location + '.txt', file_name])

    # todo: check what the revision was, and update towards that instead
    # auto update to original revision, assuming it's revision we are checking to
    subprocess.run(svn_command + [revisions[-1]])

    # launch winMerge with both of the created files as parameters
    subprocess.run(['WinMergeU', forms_path + 'from.txt', forms_path + 'to.txt'])


if __name__ == '__main__':
    main()
