import sys
import subprocess
import json
# usage example: py compare.py frm_name 39999 40000
#                              ^form    ^from ^to
# from and to being revisions that will be compared
# form should be given without the .fmb extension
# svn.exe, ifcmp60.exe and WinMergeU.exe should be defined under the PATH environment variable


def main(argv):
    # see conf_example.json
    with open('conf.json', mode='r', encoding='utf-8') as file:
        config = json.loads(file.read())
        forms_path = config['forms_path']

    # todo: consider renaming of variables
    form_name = argv[1].upper()
    form_location = forms_path + form_name
    svn_command = ['svn', 'update', form_location + '.FMB', '-r']
    object_list_command = ['ifcmp60', 'MODULE=' + form_location,
                           'MODULE_TYPE=FORM', 'logon=NO', 'forms_doc=YES']

    output_files = ['from.txt', 'to.txt']
    revisions = [argv[2], argv[3]]

    # clean up previous run, if any
    for output_file in output_files:
        subprocess.run(['del', forms_path + output_file])

    # create object list reports for both revisions
    subprocess.run(['cd', forms_path])
    for i in [0, 1]:
        subprocess.run(svn_command.copy() + [revisions[i]])
        subprocess.run(object_list_command)
        subprocess.run(['rename', form_location + '.txt', output_files[i]])

    # todo: check what the revision was, and update towards that instead
    # auto update to original revision, assuming it's revision we are checking to
    subprocess.run(svn_command.copy() + [revisions[1]])

    # launch winMerge with both of the created files as parameters
    subprocess.run(['WinMergeU', forms_path + 'from.txt', forms_path + 'to.txt'])


if __name__ == '__main__':
    # todo: test if script works after switch to subprocess
    main(sys.argv)
