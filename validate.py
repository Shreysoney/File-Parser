""" This module validates whether the file is valid or not.

Checks the filename and if it extracts valid file_month,file_year then file 
is valid otherwise not.
"""
from datetime import datetime
import shutil
from flask import render_template
from pydantic import BaseModel, validator

class FileModel(BaseModel):
    """Checks if File-name is valid or not."""
    file_name: str
    file_month=0
    file_year=0
    @validator('file_name')
    def check_file(cls,file):
        """ Checks if filename is valid or not.

        Takes file as an argument that is containg the file-name and checks if it is valid or not.
        Returns:
         Valid File-name
        Raises:
         Error When File-name is not valid
        """
        #file=str(file)
        file_month,file_year=FileModel.file_name_check(file)
        if file_month and file_year:
            return file 
        else:
             raise ValueError("Wrong File Name Wrong")
    def give_month_year(self,file):
        """ Moves File to Archive Folder if filename is valid.

        Args:
         File-name
        """
        FileModel.file_month,FileModel.file_year=FileModel.file_name_check(file)
        if FileModel.file_month and FileModel.file_year:
            src_path = f"/vagrant/project_flask/ClientFolder/{file}"
            dst_path = f"/vagrant/project_flask/ArchiveFolder/{file}"
            shutil.copy(src_path, dst_path)
    @classmethod
    def check_for_month(cls,name):
        """Gives the index for the Month"""
        months=["january","february","march",
        "april","may","june",
        "july","august","september",
        "october","november","december"]
        for i in range(len(months)):
            if name.lower()==months[i]:
                return i+1
        return 0

    @classmethod
    def file_name_check(cls,file):
        """Checks if filename is valid or not.

        Takes file as an argument that is containg the file-name and extracts file_year and file_month.
        If both are extracted filename is valid else not.
        Args:
         File-name
        Returns:
         Valid file_month,file_year
        """
        filename=f"{file}"
        filenames=filename.split(".")
        filenames=filenames[0].split("_")
        file_month=0
        file_year=0
        for name in filenames:
            if not file_month:
                file_month=FileModel.check_for_month(name)
            try:
                if int(name) and len(name)==4 and (name.startswith("19") or name.startswith("20") ):
                    file_year=int(name)
            except:
                pass
        return(file_month,file_year)



















        




