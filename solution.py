import json
import os
import sys
import requests
from multiprocessing import Pool


def main():
    global __location__
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
    _file1 = sys.argv[1]
    _file2 = sys.argv[2]
    testcomparator(_file1, _file2)


def testcomparator(_file1,_file2):
    pool = Pool()
    with open(os.path.join(__location__,_file1)) as textfile1, open(os.path.join(__location__,_file2)) as textfile2:
        _urlList_1 = textfile1.read().splitlines()
        _urlList_2 = textfile2.read().splitlines()
    for _urlFile1, _urlFile2 in zip(_urlList_1, _urlList_2):
        pool.apply_async(match(_urlFile1,_urlFile2))


def match(_urlFile1, _urlFile2):
    response_1 = get(_urlFile1)
    response_2 = get(_urlFile2)
    try:
        a = json.loads(response_1.content)
        b = json.loads(response_2.content)
        print (_urlFile1, "---------", _urlFile2, " ", ordered(a) == ordered(b))
    except Exception, err:
        print ("error during json loads : ", err)


def get(_url):
    response = None
    try:
        response = requests.get(_url)
        print(response.content)
    except Exception, err:
        print (err)
    return response


def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj


if __name__ == "__main__":
    main()
