import shutil
import os


def folder_unpacker(current_root, new_root, target_type=None):
    """
    Retrieves all files of the desired type from a hierarchy of folders of
    indeterminate size.

    Arguments:
        current_root - The source folder from which files are extracted,
        at the top of the hierarchy.
        new_root - The folder to which the extracted files will be copied.
        target_type - The type of the target files
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
