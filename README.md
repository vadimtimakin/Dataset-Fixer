# Dataset Fixer

![alt text](https://github.com/t0efL/Dataset-Fixer/blob/master/logo.jpg)

**Dataset Fixer is a utility for sorting, filtering, and transformation of datasets.**

## What are the features of this software?
The current version of the module has 7 different functions. Here is a list containing all these functions and comments explaining the task of each of the functions:
* folder_unpacker - Extracts all files of the desired type from a hierarchy of folders of indeterminate size.
* sorter - Sorts files by their types.
* splitter - Splits the existing dataset into several parts in the ratio specified by the user.
* shuffler - Shuffles files in the dataset.
* cleaner - Deletes files of a certain type from the dataset.
* cutter - Reduces the dataset by deleting unnecessary files.
* color_type_detector - Detects images of a specific color model and copies them to a new folder.

For more information about each function and its parameters, see the docstrings of these functions. You can find it in the [main module](https://github.com/t0efL/Dataset-Fixer/blob/master/dataset_fixer.py) or just get a docstring in code using special **\_\_doc\_\_** attribute. Pay attention to which functions copy files and which ones delete.

## How can I start using it?
First download this repository or clone it to your virtual environment:

`$ git clone https://github.com/t0efL/Dataset-Fixer`

Then install the necessary packages:

`$ pip install requirements.txt`

Then you can import the functions you need from the module **dataset_fixer.py** and start using them.

## Documentation
As I said above, all information about functions, parameters, and other documentation is contained in the corresponding docstrings.
In some functions, you will need to pass target file or color type as a parameter. Here are the full lists of possible values for these parameters:

[file_types.txt](https://github.com/t0efL/Dataset-Fixer/blob/master/file_types.txt) | [color_types.txt](https://github.com/t0efL/Dataset-Fixer/blob/master/color_types.txt)

## License 
This project is released under the [Apache 2.0 license](https://github.com/t0efL/Dataset-Fixer/blob/master/LICENSE).

## Additional information
Project logo was made by www.designevo.com 

If you have any questions or suggestions you can contact me using email: `vdm.timakin@yandex.ru`

Feel free to contribute.
