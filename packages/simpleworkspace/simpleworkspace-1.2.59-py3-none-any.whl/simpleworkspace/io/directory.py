from typing import Callable as _Callable, Iterator as _Iterator
import os as _os

def Create(path: str):
    '''Create all non existing directiores in specified path, ignores if exists.'''
    _os.makedirs(path, exist_ok=True)

def Scan(
        searchDirectory: str,
        includeDirs=True, includeFiles=True,
        filter:str|_Callable[[str],bool]=None,
        maxRecursionDepth: int=None
        ) -> _Iterator[str]:
    """
    Recursively iterate all directories in a path.
    All encountered exceptions are ignored

    :param filter: Callback or Regex string
        * callback that takes the fullpath and returns true for paths that should be included
        * regex string which searches full path of each file, if anyone matches a callback is called. Example: "/mySearchCriteria/i"
    :param maxRecursionDepth: Specify how many levels down to list folders, level/depth 1 is basically searchDir entries

    :returns: an iterator of full matching paths
    """
    from simpleworkspace.utility import regex

    if not _os.path.isdir(searchDirectory):
        raise NotADirectoryError(f'Supplied path is not a valid directory: "{searchDirectory}"')

    currentFolderDepth = 1 #this is basically the base directory depth with its entries and therefore the minimum value
    folderQueue = [searchDirectory]
    while (len(folderQueue) > 0):
        if (maxRecursionDepth is not None) and (currentFolderDepth > maxRecursionDepth):
            break
        currentFolderQueue = folderQueue
        folderQueue = []
        for currentFolder in currentFolderQueue:
            try:
                with _os.scandir(currentFolder) as entries:
                    for entry in entries:
                        filePath = entry.path

                        if(filter is None):
                            pathMatchesFilter = True
                        elif(isinstance(filter, str)):
                            pathMatchesFilter = regex.Match(filter, filePath) is not None
                        else: #callback
                            pathMatchesFilter = filter(filePath)
                        if entry.is_file():
                            if (includeFiles and pathMatchesFilter):
                                yield filePath
                        elif(entry.is_dir()):
                            if (includeDirs and pathMatchesFilter):
                                yield filePath
                            folderQueue.append(filePath)
                        else:
                            pass #skip symlinks
            except (PermissionError, FileNotFoundError, NotADirectoryError) as ex: 
                #common raises that can safely be skipped!

                #PermissionError: not enough permission to browse folder, a common error when recursing unkown dirs, simply skip if no exception callback

                #FileNotFound or NotADirectory errors:
                #   since we know we had a valid path from beginning, this is most likely that a file or folder
                #   was removed/modified by another program during our search
                pass
            except (OSError, InterruptedError, UnicodeError):
                #this one is tricker and might potentially be more important, eg a file can temporarily not be accessed being busy etc.
                #this is still a common exception when recursing very deep, so we don't act on it

                #InterruptedError: Raised if the os.scandir() call is interrupted by a signal.
                #UnicodeError: Raised if there are any errors while decoding the file names returned by os.scandir().
                pass
            except Exception as e:
                #here something totally unexpected has happened such as a bad callback supplied by user etc,
                #this one always raises exception

                #an completely invalid input supplied to os.scandir() such as empty string or a string not representing a directory
                #might raise TypeError and ValueError, we dont specifically handle these since we in these cases want to fully
                #raise an exception anyway

                raise e
        currentFolderDepth += 1
    return

def Remove(path: str) -> None:
    '''removes a whole directory tree'''
    import shutil
    shutil.rmtree(path, ignore_errors=True)
