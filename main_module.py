import shutil
import os
import imghdr


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
        pass their types as a tuple; if you don't select the type, all files
        will be extracted.

    The function does not perform any conversions to the original folder,
    files are not deleted after copying to a new folder.
    """

    # Retrieving only certain types.
    if target_type:

        # Working with multiple file types.
        if len(target_type) > 1:
            for root, dirs, files in os.walk(current_root):
                for file in files:
                    for item in target_type:
                        if file.lower().__contains__(('.' + str(item))):
                            shutil.copy(os.path.join(root, file), new_root)
                            break
                        else:
                            if os.path.isdir(root):
                                folder_unpacker(file, new_root, target_type)

        # Working with a single file type.
        else:
            for root, dirs, files in os.walk(current_root):
                for file in files:
                    if file.lower().__contains__(('.' + str(target_type))):
                        shutil.copy(os.path.join(root, file), new_root)
                    else:
                        if os.path.isdir(root):
                            folder_unpacker(file, new_root, target_type)

    # Extract all files that are not folders.
    else:
        for root, dirs, files in os.walk(current_root):
            for file in files:
                if os.path.isdir(root):
                    shutil.copy(os.path.join(root, file), new_root)


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
        Defaults to None. The type of the target files
        (Example: jpg, pdf, png; without a dot at the beginning);
        if you want to sort files of the diffrent type at the same type,
        pass their types as a tuple; if you don't select the type, all files
        will be sorted.

    The function does not perform any conversions to the original folder,
    files are not deleted after copying to a new folder.
    """

    # The code for this function could be made much smaller if I just set the
    # check flag for the target_type variable inside the main loop. In this
    # case, the flag would have to be checked every time the cycle passes,
    # which would affect the performance, which is especially noticeable when
    # working with large datasets.

    # Sorting only certain types.
    if target_type:

        # Working with multiple file types.
        if len(target_type) > 1:
            for root, dirs, files in os.walk(current_root):
                for file in files:
                    # This flag checks that our file is not a folder,
                    # which would give an error.
                    if os.path.isfile(os.path.join(root, file)):
                        file_type = imghdr.what(os.path.join(root, file))
                        # This flag checks that the file_type variable is not
                        # 'NoneType', which helps avoid TypeError. It
                        # sometimes happens that imghdr defines the type of a
                        # normal file (for example, a jpg image) as None.
                        if file_type and (file_type in target_type):
                            # Create a folder with a name containing the type
                            # of files inside it, if this folder has not been
                            # created yet.
                            if not os.path.exists(
                                    os.path.join(new_root, file_type)):
                                os.mkdir(os.path.join(new_root, file_type))
                            # Copying file.
                            shutil.copy(os.path.join(root, file),
                                        os.path.join(new_root, file_type))

        # Working with a single file type.
        else:
            for root, dirs, files in os.walk(current_root):
                for file in files:
                    # This flag checks that our file is not a folder,
                    # which would give an error.
                    if os.path.isfile(os.path.join(root, file)):
                        file_type = imghdr.what(os.path.join(root, file))
                        # This flag checks that the file_type variable is not
                        # 'NoneType', which helps avoid TypeError. It
                        # sometimes happens that imghdr defines the type of a
                        # normal file (for example, a jpg image) as None.
                        if file_type and (file_type == target_type):
                            # Create a folder with a name containing the type
                            # of files inside it, if this folder has not been
                            # created yet.
                            if not os.path.exists(
                                    os.path.join(new_root, file_type)):
                                os.mkdir(os.path.join(new_root, file_type))
                            # Copying file.
                            shutil.copy(os.path.join(root, file),
                                        os.path.join(new_root, file_type))

    # Sorting all files that are not folders.
    else:
        for root, dirs, files in os.walk(current_root):
            for file in files:
                # This flag checks that our file is not a folder,
                # which would give an error.
                if os.path.isfile(os.path.join(root, file)):
                    file_type = imghdr.what(os.path.join(root, file))
                    # This flag checks that the file_type variable is not
                    # 'NoneType', which helps avoid TypeError. It sometimes
                    # happens that imghdr defines the type of a normal file
                    # (for example, a jpg image) as None.
                    if file_type:
                        # Create a folder with a name containing the type of
                        # files inside it, if this folder has not been
                        # created yet.
                        if not os.path.exists(
                                os.path.join(new_root, file_type)):
                            os.mkdir(os.path.join(new_root, file_type))
                        # Copying file.
                        shutil.copy(os.path.join(root, file),
                                    os.path.join(new_root, file_type))
