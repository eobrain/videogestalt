# Need to `pip install --upgrade --editable .` before running `pytest`, otherwise it will not work because the command `videogestalt` won't be in the environment.
# To run pytest with a coverage report, use the following commands:
# 	coverage run --branch -m pytest -v
#	coverage report -m
#
# TODO: implement visual similarity to check that two video files are similar: https://stackoverflow.com/questions/23982960/fast-and-efficient-way-to-detect-if-two-images-are-visually-identical-in-python

import os
import shlex
import shutil
import subprocess

""" Auxiliary functions for unit tests """
def check_eq_files(path1, path2, blocksize=65535, startpos1=0, startpos2=0):
    """ Return True if both files are identical, False otherwise """
    flag = True
    with open(path1, 'rb') as f1, open(path2, 'rb') as f2:
        buf1 = 1
        buf2 = 1
        f1.seek(startpos1)
        f2.seek(startpos2)
        while buf1 and buf2:
            buf1 = f1.read(blocksize)
            buf2 = f2.read(blocksize)
            if buf1 != buf2 or (buf1 and not buf2) or (buf2 and not buf1):
                # Reached end of file or the content is different, then return false
                flag = False
                break
            elif (not buf1 and not buf2):
                # End of file for both files
                break
    return flag
    #return filecmp.cmp(path1, path2, shallow=False)  # does not work on Travis

def check_eq_dir(path1, path2):
    """ Return True if both folders have same structure totally identical files, False otherwise """
    # List files in both directories
    files1 = []
    files2 = []
    for dirpath, dirs, files in os.walk(path1):
        files1.extend([os.path.relpath(os.path.join(dirpath, file), path1) for file in files])
    for dirpath, dirs, files in os.walk(path2):
        files2.extend([os.path.relpath(os.path.join(dirpath, file), path2) for file in files])
    # Ensure the same order for both lists (filesystem can spit the files in whatever order it wants)
    files1.sort()
    files2.sort()

    # Different files in one or both lists: we fail
    if files1 != files2:
        return False
    # Else we need to compare the files contents
    else:
        flag = True
        for i in range(len(files1)):
            #print("files: %s %s" % (files1[i], files2[i]))  # debug
            # If the files contents are different, we fail
            if not check_eq_files(os.path.join(path1, files1[i]), os.path.join(path2, files2[i])):
                flag = False
                break
        # Else if all files contents were equal and all files are in both lists, success!
        return flag

def fullpath(relpath):
    '''Relative path to absolute'''
    if (type(relpath) is object or hasattr(relpath, 'read')): # relpath is either an object or file-like, try to get its name
        relpath = relpath.name
    return os.path.abspath(os.path.expanduser(relpath))

def path_sample_files(type=None, path=None, createdir=False):
    """ Helper function to return the full path to the test files """
    subdir = ''
    if not type:
        return ''
    elif type == 'input':
        subdir = 'examples'
    elif type == 'results':
        subdir = 'results'
    elif type == 'output':
        subdir = 'out'

    dirpath = ''
    scriptpath = os.path.dirname(os.path.realpath(__file__))
    if path:
        dirpath = fullpath(os.path.join(scriptpath, subdir, path))
    else:
        dirpath = fullpath(os.path.join(scriptpath, subdir))

    if createdir:
        create_dir_if_not_exist(dirpath)

    return dirpath

def create_dir_if_not_exist(path):
    """Create a directory if it does not already exist, else nothing is done and no error is return"""
    if not os.path.exists(path):
        os.makedirs(path)

def remove_if_exist(path):
    """Delete a file or a directory recursively if it exists, else no exception is raised"""
    if os.path.exists(path):
        if os.path.isdir(path):
            shutil.rmtree(path)
            return True
        elif os.path.isfile(path):
            os.remove(path)
            return True
    return False

""" Unit tests """
def setup_module():
    """ Initialize the tests by emptying the out directory """
    outfolder = path_sample_files('output')
    shutil.rmtree(outfolder, ignore_errors=True)
    create_dir_if_not_exist(outfolder)

def test_gif_module():
    """ test gif generation as a module """
    # Import videogestalt as a module
    from videogestalt import videogestalt as vg
    # Prepare filepaths
    filein = path_sample_files('input', 'countdown.mp4')
    fileout = path_sample_files('output', 'countdown-gestalt-module')
    fileoutwithext = path_sample_files('output', 'countdown-gestalt-module.gif')
    fileresult = path_sample_files('results', 'countdown-gestalt.gif')
    # Call videogestalt as a Python module
    vg.main(fr'-i {filein!r} -o {fileout!r} --gif')  # need to specify !r to get the repr() of paths, otherwise all backslashes are removed in f-strings: https://peps.python.org/pep-0498/#raw-f-strings
    # Check that the output file is the same as a pregenerated one
    assert check_eq_files(fileoutwithext, fileresult)

#def test_video_module():
#    """ test video mp4 generation as a module """
    # Import videogestalt as a module
#    from videogestalt import videogestalt as vg
    # Prepare filepaths
#    filein = path_sample_files('input', 'countdown.mp4')
#    fileout = path_sample_files('output', 'countdown-gestalt-module')
#    fileoutwithext = path_sample_files('output', 'countdown-gestalt-module.mp4')
#    fileresult = path_sample_files('results', 'countdown-gestalt.mp4')
    # Call videogestalt as a Python module
#    vg.main(fr'-i {filein!r} -o {fileout!r} --video')  # need to specify !r to get the repr() of paths, otherwise all backslashes are removed in f-strings: https://peps.python.org/pep-0498/#raw-f-strings
    # Check that the output file is the same as a pregenerated one
#    assert check_eq_files(fileoutwithext, fileresult)

def test_gif_cmd():
    """ test gif generation from a command call """
    # Import videogestalt as a module
    from videogestalt import videogestalt as vg
    # Prepare filepaths
    filein = path_sample_files('input', 'countdown.mp4')
    fileout = path_sample_files('output', 'countdown-gestalt-cmd')
    fileoutwithext = path_sample_files('output', 'countdown-gestalt-cmd.gif')
    fileresult = path_sample_files('results', 'countdown-gestalt.gif')
    # Call videogestalt as a command
    process = subprocess.run(shlex.split(fr'videogestalt -i {filein!r} -o {fileout!r} --gif'),
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         universal_newlines=True)
    # Check that the output file is the same as a pregenerated one
    print(process.stdout)  # print in case of exception, we will see the output
    print(process.stderr)
    # Check that the output file is the same as a pregenerated one
    assert check_eq_files(fileoutwithext, fileresult)

#def test_video_cmd():
#    """ test video mp4 generation from a command call """
    # Import videogestalt as a module
#    from videogestalt import videogestalt as vg
    # Prepare filepaths
#    filein = path_sample_files('input', 'countdown.mp4')
#    fileout = path_sample_files('output', 'countdown-gestalt-cmd')
#    fileoutwithext = path_sample_files('output', 'countdown-gestalt-cmd.mp4')
#    fileresult = path_sample_files('results', 'countdown-gestalt.mp4')
    # Call videogestalt from as a command
#    process = subprocess.run(shlex.split(fr'videogestalt -i {filein!r} -o {fileout!r} --video'),
#                         stdout=subprocess.PIPE,
#                         stderr=subprocess.PIPE,
#                         universal_newlines=True)
    # Check that the output file is the same as a pregenerated one
#    print(process.stdout)  # print in case of exception, we will see the output
#    print(process.stderr)
#    assert check_eq_files(fileoutwithext, fileresult)
