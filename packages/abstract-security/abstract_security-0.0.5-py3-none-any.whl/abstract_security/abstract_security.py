#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from abstract_utilities.string_clean import eatAll,eatOuter
def split_eq(line):
    """
    Splits a string at the first equals sign '=' and cleans up the key and value.

    Args:
        line (str): The string to be split.

    Returns:
        list: A list containing the cleaned key and value. If '=' is not found, returns [line, None].
    """
    if '=' in line:
        key_side = line.split('=')[0]
        value_side = line[len(key_side+'='):]
        return [eatOuter(key_side,[' ','','\t']),eatAll(value_side,[' ','','\t','\n'])]
    return [line,None]
def dotenv_load(path:str=None):
    """
    Safely load the .env file if it exists at a specified path.

    Args:
        path (str): The path to load the .env file from. If None, no operation is performed. 

    Returns:
        bool: True if the .env file is successfully loaded, otherwise False.
    """
    if path and os.path.isfile(path) and os.path.basename(path)[0] == '.':
        load_dotenv(path)
        return True
class AbstractEnv:
    def __init__(self,key='MY_PASSWORD',file_name='.env',path=os.getcwd()):
        self.re_initialize(file_name=file_name,key=key,path=path)
    def re_initialize(self,key='MY_PASSWORD',file_name='.env',path=os.getcwd()):
        """
        Initializes an AbstractEnv object to manage environment variables.

        Args:
            key (str, optional): The key to search for in the .env file. Defaults to 'MY_PASSWORD'.
            file_name (str, optional): The name of the .env file. Defaults to '.env'.
            path (str, optional): The path where the .env file is located. Defaults to the current working directory.
        """
        self.key = key or 'MY_PASSWORD'
        self.current_folder = os.getcwd()
        if path and os.path.isfile(path):
            self.file_name = os.path.basename(path)
            self.path = os.path.dirname(path)
        else:
            self.path = path or self.current_folder
            self.file_name = file_name or '.env'
        self.start_path_env = os.path.join(self.path,self.file_name)
        self.home_folder = os.path.expanduser("~")
        self.envy_all = os.path.join(self.home_folder,'.envy_all')
        self.directories = self.get_directories()
        self.env_value = self.find_and_read_env_file(key=self.key,file_name=self.file_name, path=self.path,initialize=False)
    def find_and_read_env_file(self,key:str=None, file_name:str=None, path=None,initialize=True):
        """
        Search for an environment file and read a specific key from it.

        Args:
            file_name (str): Name of the .env file to be searched. Defaults to '.env'.
            key (str): Key to be retrieved from the .env file. Defaults to 'MY_PASSWORD'.
            start_path (str): Directory path to start the search from. If None, search starts from current directory. 

        Returns:
            str: The value corresponding to the key if found, otherwise None.
        """
        # Set the default start_path to the current directory if it's None
        # Try to find the file in the start_path
        key = key or self.key
        path = path or self.start_path_env
        file_name = file_name or self.file_name
        if initialize:
            self.re_initialize(key=key,file_name=file_name,path=path)
        for directory in self.directories:
            if directory and os.path.isdir(directory) and self.file_name:
                env_path = os.path.join(directory,self.file_name)
                if os.path.isfile(env_path):
                    value = self.search_for_env_key(key=key,path=env_path)
                    if value:
                        return value
    def get_directories(self):
        """
        Retrieves a list of directories to search for the .env file.

        Returns:
            list: A list of directories including the specified path, current folder, home folder, and '.envy_all' directory.
        """
        directories=[]
        for directory in [self.path,self.current_folder,self.home_folder,self.envy_all]:
            if os.path.isdir(directory) and directory not in directories:
                directories.append(directory)
        return directories
    
    def search_for_env_key(self,key:str=None,path:str=None):
        """
        Retrieves the value of a specified environment variable from a .env file.

        Args:
            key (str, optional): The key to search for in the .env file. Defaults to None.
            path (str, optional): The path to the .env file. Defaults to None.
            file_name (str, optional): The name of the .env file. Defaults to None.

        Returns:
            str: The value of the environment variable if found, otherwise None.
        """
        key = key or self.default_env_key
        path = path or self.start_path_env
        if path and os.path.isfile(path):
            with open(path, "r") as f:
                for line in f:
                    line_key,line_value = split_eq(line)
                    # If the line contains the key, return the value after stripping extra characters
                    if line_key == key:
                        return line_value

    def get_env_value(key:str=None,path:str=os.getcwd(),file_name:str=None):
        """
        Retrieves the value of the specified environment variable.

        Args:
            path (str): The path to the environment file. Defaults to None.
            file_name (str): The name of the environment file. Defaults to '.env'.
            key (str): The key to search for in the .env file. Defaults to 'MY_PASSWORD'.

        Returns:
            str: The value of the environment variable if found, otherwise None.
        """
        if safe_env_load(path):
            return os.getenv(key)
        return find_and_read_env_file(file_name=file_name, key=key, path=path_ls)

def get_env_value(key:str=None,path:str=None,file_name:str=None):
    abstract_env = AbstractEnv(key=key, file_name=file_name, path=path)
    """
    Retrieves the value of a specified environment variable from a .env file.

    Args:
        key (str, optional): The key to search for in the .env file. Defaults to None.
        path (str, optional): The path to the .env file. Defaults to None.
        file_name (str, optional): The name of the .env file. Defaults to None.

    Returns:
        str: The value of the environment variable if found, otherwise None.
    """
    return abstract_env.env_value

input(get_env_value('pass'))
