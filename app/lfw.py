"""
    LFW methods to management the dataset of Veriff challenge.

    This code is following the best practices of PEP 20, PEP 8,
    and 'The Best of the Best Practices (BOBP) Guide for Python'

    Reference: https://gist.github.com/sloria/7001839#file-bobp-python-md
"""
import hashlib
import requests
import os

from shutil import unpack_archive


URL = 'http://vis-www.cs.umass.edu/lfw/lfw.tgz'
MD5SUM = 'a17d05bd522c52d84eca14327a23d494'



def lfw_acquisition(url, md5sum, path=None):
    """
    LFW acquisition is the method to download, validate,
    extract the main LFW dataset.

    :param url: LFW url to download the dataset.
                Included the file name in the url.
    :param md5sum: the md5sum code to validate the dataset file.
    :param path: the path that will be used to extract the content
                 of the dataset. Default value is ".".

    :return: array with all faces/photos in the format of the path
             of files.
    """
    if path is None:
        path = "."

    dataset_file = url.split('/')[-1]
    dataset_file_name = dataset_file.split('.')[0]

    if len(url) > 0 and len(md5sum) > 0 and len(dataset_file) > 0:
        req = requests.get(url)

        with open(dataset_file, "wb") as data:
            data.write(req.content)

        get_md5 = hashlib.md5(open(dataset_file, "rb").read()).hexdigest()

        if get_md5 != md5sum:
            raise FileExistsError("The file is not validated")

        else:
            unpack_archive(dataset_file, path)
            files = []

            # r=root, d=directories, f = files
            for r, f in os.walk('{0}/'.format(dataset_file_name)):

                for file in f:

                    if '.jpg' in file:
                        files.append(os.path.join(r, file))

            return files

    else:
        raise AttributeError("Check the parameters passed to the function")



if __name__ == "__main__":
    print(lfw_acquisition(url=URL, md5sum=MD5SUM, path='.'))[0]
