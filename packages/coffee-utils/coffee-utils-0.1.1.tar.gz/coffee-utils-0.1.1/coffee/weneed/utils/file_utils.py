import os
import string

class FileUtils:
    """
    A utility class for working with files.
    """
    @staticmethod
    def __strip_non_ascii_from_file(file_path, ascii_chars):
        """
        Internal method that reads a file, removes any non-ASCII characters,
        and writes the clean content back to the file.
        
        Parameters:
        file_path (str): The path to the file to be processed.
        ascii_chars (set): Set of ASCII characters.
        """
        with open(file_path, 'r') as file:
            contents = file.read()

        ascii_contents = ''.join(c for c in contents if c in ascii_chars)
        if contents != ascii_contents:
            with open(file_path, 'w') as file:
                file.write(ascii_contents)

    @staticmethod
    def strip_non_ascii(directory, file_extension=None, recursive=False):
        """
        Strips non-ASCII characters from all appropriate files in a given directory.

        Parameters:
        directory (str): The directory to be processed.
        file_extension (str): An optional extension of the files to be processed. 
                              All files will be processed if not specified. 
        recursive (bool): A flag indicating whether to process files recursively in  
                          all subdirectories (True), or only in the given directory (False). 
                          Default is False.
        """
        ascii_chars = set(string.printable)
        file_processing_method = FileUtils.__strip_non_ascii_from_file

        for root, _, filenames in os.walk(directory) if recursive else [(directory, [], os.listdir(directory))]:
            for filename in filenames:
                if file_extension is None or filename.endswith(file_extension):
                    file_processing_method(os.path.join(root, filename), ascii_chars)