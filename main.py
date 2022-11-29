from pdf2image import convert_from_path, convert_from_bytes
from PIL import Image
import argparse
from glob import glob
import os

from tqdm import tqdm


def parser_fn():

    parser = argparse.ArgumentParser(description='Converts PDF to JPG, automation code.')
    parser.add_argument('--source', type=str, required=True,  help='This can be a single file, or an entire folder of PDFs')
    parser.add_argument('--pages', type=int, default=0, help="Pass the page no to convert to JPG. Pass 0 if you want all pages to be converted")
    parser.add_argument('--dump', type=str, default=".", help="Save path.")

    args = parser.parse_args()
    return args


if __name__ == "__main__":

    opts = parser_fn()

    # print(opts.source)
    assert os.path.exists(opts.source), "File doesn't exist. Please check the path"
    
    if not os.path.exists(opts.dump):
        os.makedirs(opts.dump)

    path = opts.source


    if os.path.isfile(path):
        print(f'Generating JPG from pdf {opts.source} for page# {opts.pages}')
        images = convert_from_path(path)

    elif os.path.isdir(path):
        filelist = glob( os.path.join( path, "*.pdf" ) )
        filecount = len(filelist)
        print(f'{filecount} PDF files found in the folder. Saving to {os.path.abspath(opts.dump)} ')
        for file in tqdm(filelist):
            images = convert_from_path(file)
    
    assert images != [], "Some error occured. Please report the error with logs"
    
    print('Images generated. Saving files')
    
    count = 0
    if opts.pages == 0:
        for image in tqdm(images):
            image.save(os.path.join(opts.dump, f"{count+1}.jpg"))
            count += 1
    else:
        dumppath = os.path.join(opts.dump, f"{opts.pages }.jpg")
        images[opts.pages - 1].save(dumppath)
        print(f"Image saved at {dumppath}")
