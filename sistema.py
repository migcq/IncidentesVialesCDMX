import os
from dataclasses import dataclass

@dataclass
class Directorio():
    path : str

    def read_file_names(self, ext="csv"):
        list_files = os.listdir(self.path)

        files_with_ext = [ file_ for file_ in list_files if file_.endswith(ext)]
        
        return files_with_ext
