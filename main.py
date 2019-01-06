import argparse

from util import *

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument('-s', '--show', action='store_true')
ap.add_argument('-v', '--verbose', action='store_true')
ap.add_argument('-a', '--answers', required=True, help='path to csv file containg correct question-answer pairs')
ap.add_argument('-i', '--images', required=True, nargs='+', help="path to the input images")
args = vars(ap.parse_args())


# iterate through images
for image_path in args['images']:
	image, gray, lined = preprocess(image_path)

	if args['show']:
		show_image(image)
		show_image(gray)
		show_image(lined)

	doc_contours = find_page(lined)

	# apply a four point perspective transform
	page_color = remove_edges(four_point_transform(image, doc_contours.reshape(4, 2)))
	page_gray = remove_edges(four_point_transform(gray, doc_contours.reshape(4, 2)))

	if args['show']:
		show_image(page_color)
		show_image(page_gray)

	# apply Otsu's thresholding method to binarize the page_gray
	thresholded_image = cv2.threshold(page_gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

	if args['show']:
		show_image(thresholded_image)

	question_contours = find_bubbles(thresholded_image)

	get_answers(page_color, thresholded_image, question_contours, args['answers'], num_answers=10, num_questions=15)


