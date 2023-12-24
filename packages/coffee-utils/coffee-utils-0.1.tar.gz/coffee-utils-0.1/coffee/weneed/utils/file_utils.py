import os
import string

class FileUtils:
    @staticmethod
    def strip_non_ascii(directory, file_extension=None, recursive=False):
        if recursive:
            for dirpath, dirnames, filenames in os.walk(directory):
                for filename in filenames:
                    if file_extension is None or filename.endswith(file_extension):
                        file_path = os.path.join(dirpath, filename)
                        with open(file_path, 'r') as file:
                            contents = file.read()
                            ascii_contents = ''.join(c for c in contents if c in string.printable)
                            with open(f"{file_path}_new", 'w') as new_file:
                                new_file.write(ascii_contents)
        else:
            for filename in os.listdir(directory):
                if file_extension is None or filename.endswith(file_extension):
                    file_path = os.path.join(directory, filename)
                    with open(file_path, 'r') as file:
                        contents = file.read()
                        ascii_contents = ''.join(c for c in contents if c in string.printable)
                        with open(f"{file_path}_new", 'w') as new_file:
                            new_file.write(ascii_contents)