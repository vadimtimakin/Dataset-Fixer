import shutil
import os
import filetype


def folder_unpacker(current_root, new_root, target_type=None):
    """
    Retrieves all files of the desired type from a hierarchy of folders of
    indeterminate size.

    Args:

        current_root (str): The source folder from which files are extracted,
        at the top of the hierarchy.

        new_root (str): The folder to which the extracted files will be copied,
        must be created in advance.

        target_type (:obj: ('str', 'tuple', list'), optional):
        Defaults to None. The type of the target files.
        (Example: jpg, pdf, png; without a dot at the beginning);
        if you want to extract files of the diffrent type at the same type,
        pass their types as a tuple or a list;
        if you don't select the type, all files will be extracted.
        To determine the file type, I used the filetype
        package, in particular the 'guess' function with 'mime'.
        To select the file type you need, see how the above function denotes
        types and pass them to the already given function as an argument.
        List of possible types here:
        "https://pypi.org/project/filetype/"
        Or here:
        "https://github.com/t0efL/Dataset-Fixer/blob/master/README.md"

    The function does not perform any conversions to the original folder,
    files are not deleted after copying to a new folder.
    """

    # Extracting only certain types.
    if target_type:

        # Working with multiple file types.
        if type(target_type) is not str:
            def flag(x, y):
                file_type = filetype.guess(x).mime
                for i in y:
                    if file_type == i:
                        return True
                return False

        # Working with a single file type.
        else:
            def flag(x, y):
                file_type = filetype.guess(x).mime
                return file_type == y

    # Extracting all files that are not folders.
    else:
        target_type = True

        def flag(x, y):
            return bool(x or y)

    for root, dirs, files in os.walk(current_root):
        for file in files:
            if flag(os.path.join(root, file), target_type):
                # File copying.
                shutil.copy(os.path.join(root, file), new_root)
            else:
                # Extracting files from detected folders.
                if os.path.isdir(root):
                    folder_unpacker(file, new_root, target_type)


def sorter(current_root, new_root, target_type=None):
    """
    Sorts files by their types.

    This function extracts all files from the source folder and sorts them in
    the target folder. The sorting process consists of creating several
    new folders in the target folder with names of different file types
    and then copying the corresponding files there.

    The function ignores other folders with files inside the source folder.
    If you also need to sort them, use the folder_unpacker function from
    the same module to extract files from them in advance.

    Args:

        current_root (str): Source folder with unsorted files

        new_root (str): The target folder where the sorted files will be
        located, must be created in advance.

        target_type (:obj: ('str', 'tuple', list'), optional):
        Defaults to None. The type of the target files;
        if you want to sort files of the diffrent type at the same type,
        pass their types as a tuple or a list;
        if you don't select the type, all files will be sorted.
        To determine the file type, I used the filetype
        package, in particular the 'guess' function with 'mime'.
        To select the file type you need, see how the above function denotes
        types and pass them to the already given function as an argument.
        List of possible types here:
        "https://pypi.org/project/filetype/"
        Or here:
        "https://github.com/t0efL/Dataset-Fixer/blob/master/README.md"


    The function does not perform any conversions to the original folder,
    files are not deleted after copying to a new folder.
    """

    # Sorting only certain types.
    if target_type:

        # Working with multiple file types.
        if type(target_type) is not str:
            def flag(x, y):
                return x in y

        # Working with a single file type.
        else:
            def flag(x, y):
                return x == y

    # Sorting all files that are not folders.
    else:
        target_type = True

        def flag(x, y):
            return bool(x or y)

    for root, dirs, files in os.walk(current_root):
        for file in files:
            # This flag checks that our file is not a folder,
            # which would give an error.
            if os.path.isfile(os.path.join(root, file)):
                # Find out the file type.
                file_type = filetype.guess(os.path.join(root, file)).mime
                # This flag checks that the file_type variable is not
                # 'NoneType', which helps avoid TypeError. It sometimes
                # happens that filetype defines the type of a normal file
                # (for example, a jpg image) as None.
                if file_type and flag(file_type, target_type):
                    # Create a folder with a name containing the type of
                    # files inside it, if this folder has not been
                    # created yet.
                    # Next, I use a little formatting, replacing the
                    # '\'characters with '_'characters to avoid a path error.
                    if not os.path.exists(
                            os.path.join(new_root,
                                         file_type.replace('/', '_'))):
                        os.mkdir(os.path.join(new_root,
                                              file_type.replace('/', '_')))
                    # Copying file.
                    shutil.copy(os.path.join(root, file),
                                os.path.join(new_root,
                                             file_type.replace('/', '_')))
