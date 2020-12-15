import os.path
from pathlib import Path


def findMatchBySubstring(substring, matches):
    results = [match for match in matches if substring in match.path_string]
    if not len(results):
        return None
    if len(results) == 1:
        return results[0]
    return results


def getFileOrDefault(path, defaultPath):
    return path if os.path.isfile(path) else defaultPath


def getDirOrDefault(path, defaultPath):
    return path if Path(path).is_dir() else defaultPath
