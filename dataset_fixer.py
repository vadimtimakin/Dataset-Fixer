# Dataset-fixer

import shutil
import os
import filetype


def folder_unpacker(current_root, new_root, target_type=None):
    """
    Extracts all files of the desired type from a hierarchy of folders of
    indeterminate size.

    Args:

        current_root (str): The source folder from which files are extracted,
        at the top of the hierarchy.

        new_root (str): The folder to which the extracted files will be copied,
        must be created in advance.

        target_type (str or tuple or list):
        Optional, defaults to None. The type of the target files.
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

        target_type (str or tuple or list):
        Optional, defaults to None. The type of the target files;
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


def splitter_numerical(current_root, new_root, relation):
    """Splitter function with relation_type='numerical'."""

    # Checking the validity of the split.
    files = os.listdir(path=current_root)
    assert_message = "The number of files in the separated parts of the "
    assert_message += "dataset does not match the original number of files:"
    assert_message += " {0} != {1}.".format(sum(relation), len(files))
    assert sum(relation) == len(files), assert_message

    # Checking for the absence of fractional values.
    for number in relation:
        assert_message = "the relation argument "
        assert_message += "can only contain integer values."
        assert type(number) == int, assert_message

    # Creating a new folder for each part of the dataset.
    for i in range(len(relation)):
        os.mkdir(os.path.join(new_root, (str(i+1) + "_part")))

    # Splitting.
    part_number = 0
    iter_point = 0
    for part in relation:
        part_number += 1
        for root, dirs, files in os.walk(current_root):
            for file in files[iter_point:(iter_point + part)]:
                shutil.copy(os.path.join(current_root, file),
                            os.path.join(new_root,
                                         (str(part_number) + "_part")))
        iter_point += part


def splitter_percentage(current_root, new_root, relation):
    """Splitter function with relation_type='percentage'."""
    pass


def splitter_mutual(current_root, new_root, relation):
    """Splitter function with relation_type='mutual'."""

    # Reducing the ratio to a percentage form
    # and pass it to the corresponding function.
    percentage = list()
    for item in relation:
        item = item/sum(relation)
        percentage.append(item)

    splitter_percentage(current_root, new_root, percentage)


def splitter(current_root, new_root, relation, relation_type='numerical'):
    """
    Splits the existing dataset into several parts in the ratio specified
    by the user.

    Args:

        current_root (str): Source folder with the dataset.

        new_root (str): The target folder where the split dataset will appear.

        relation (tuple or list): The ratio of parts that the
        dataset is divided into. The split ratio can be passed in different ways
        (in all cases, it is a tuple or list containing all the values inside):
        1) Numerical (int) -  A list or tuple containing the number of files
        in each part of the split dataset. For example, (1000, 2000, 3000) if
        there are 6000 files in total in current_root.
        If the sum of files in different parts of the dataset does not match the
        number of files in the source folder, you will get an error.
        2) Mutual relation (float) - A list or tuple containing the ratio of the
        number of files in different parts of a divided dataset to each other.
        For example, (1, 1.5, 2) means 1 : 1.5 : 2. In this case, if the source
        dataset has 4500 files, they will be distributed as 1000, 1500, 2000
        files respectively.
        3) Percentage ratio (float) - A list or tuple containing the percentage
        of the number of files in different parts of the split dataset.
        Instead of percentages, parts of the whole are used here.
        For example, (0.5, 0.25, 0.25) means 50%, 25%, 25%.
        In this case, if the source dataset has 1000 files, they will be
        distributed as 500, 250, 250 respectively. Make sure that the sum of all
        the numbers in the list or tuple is equal to 1,
        otherwise you will get an error.
        To select one of these types, pass the corresponding value of the
        relation_type argument to the function (read more about this below).

        relation_type (str): The type of ratio that the dataset
        will be divided by. This parameter is directly related to the relation
        parameter. Read the description of the latter to understand what this
        parameter is for. Each type of relationship corresponds to the following
        value of the relation_type parameter:
        1) Numerical - relation_type='numerical'
        2) Mutual relation - relation_type='mutual'
        3) Percentage ratio - relation_type='percentage'

    The function does not perform any conversions to the original folder,
    files are not deleted after copying to a new folder.
    """

    # Check out the type of relation argument.
    assert_message = "the relation argument must be a list or tuple."
    assert type(relation) in (tuple, list), assert_message

    # Making sure that the lenght of relation argument less than the number
    # files in the source dataset.
    files = os.listdir(path=current_root)
    assert_message = "the length of the relation argument cannot be greater "
    assert_message += "than the number of files in the source folder."
    assert len(relation) < len(files), assert_message
    
    # Checking for the absence of negative values and zeros.
    for number in relation:
        assert_message = "the relation argument "
        assert_message += "can only contain positive values."
        assert number > 0, assert_message

    # Select the type of relationship interpretations.
    if relation_type == 'numerical':
        splitter_numerical(current_root, new_root, relation)
    elif relation_type == 'mutual':
        splitter_mutual(current_root, new_root, relation)
    elif relation_type == 'percentage':
        splitter_percentage(current_root, new_root, relation)
    else:
        assert_message = "invalid relation_type value. Choose one of "
        assert_message += "'numerical'(default), 'mutual', 'percentage'."
        assert False, assert_message
