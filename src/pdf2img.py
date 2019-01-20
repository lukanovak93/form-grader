import argparse

import pdf2image


'''
Utility script for transforming the pdf into the image. Transwer to utility function later maybe.

Parameters: -pdf: path to pdf to be converted to the image.
'''

ap = argparse.ArgumentParser()
ap.add_argument('-pdf', required=True)
args = vars(ap.parse_args())

pages = pdf2image.convert_from_path(args['pdf'], dpi=300)

for page in pages:
    page.save('data/new_form.jpg', 'JPEG')