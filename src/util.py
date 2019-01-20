import imutils
from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import cv2
import os
import pandas as pd


def show_image(image):

    img = imutils.resize(image, width=600)

    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def remove_edges(image):
    h, w = image.shape[0:2]
    new_h = int(0.01*h)
    new_w = int(0.01*w)

    return image[new_h:h-new_h, new_w:w-new_w]


def read_answers(path_to_answers):
    ans = pd.read_csv(path_to_answers, sep=',')
    d = {}

    for _, row in ans.iterrows():
        d[row[0]] = row[1]

    return d


def preprocess(path_to_image):
    '''
    Open image and create grayscale and lined (canny edge detected) version.

    Args:
        path_to_image: String path to image to open

    Returns:
        Normal, grayscale and lined (canny edge detected) version
    '''

    image = cv2.imread(path_to_image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 75, 200)

    return (image, gray, edged)


def find_page(lined):
    '''
    Find contours in the edge map, then initialize the contour that corresponds to the document. Sort the contours according to their size in descending order, loop over them and if currently observed contour has 4 corners, it's assumed that it's the paper contour.

    Args:
        lined: OpenCV image object (numpy array) of Canny image

    Returns:
        4-point list with coordinates for edges of the document
    '''

    page_contours = cv2.findContours(lined.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    page_contours = imutils.grab_contours(page_contours)
    doc_contours = None

    if len(page_contours) > 0:
        page_contours = sorted(page_contours, key=cv2.contourArea, reverse=True)

        for c in page_contours:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)

            if len(approx) == 4:
                doc_contours = approx
                break

    return doc_contours


def find_bubbles(thresholded_image):
    '''
    Find contours in the thresholded image, then initialize the list of contours that correspond to questions. Loop over the contours, get the bounding box of that contour and then use the bounding box to compute the aspect ratio. To label the contour as a question, region should be wide and tall enough and have an aspect ratio approximately equal to 1.

    Args:
        thresholded_image: Numpy array of thresholded image.

    Returns:
        List of question contours.
    '''

    bubble_contours = cv2.findContours(thresholded_image.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    bubble_contours = imutils.grab_contours(bubble_contours)
    question_contours = []

    for c in bubble_contours:
        (x, y, w, h) = cv2.boundingRect(c)
        aspect_ratio = w / float(h)

        if w >= 20 and h >= 20 and aspect_ratio >= 0.9 and aspect_ratio <= 1.1:
            question_contours.append(c)

    return question_contours


def get_answers(page_color, thresholded_image, question_contours,
                path_to_answers, num_answers, num_questions):
    '''
    Sort the question contours top-to-bottom, then initialize the total number of correct answers. Each question has `num_answers` possible answers, to loop over the question in batches of `num_questions`. Then sort the contours for the current question from left to right and loop over the sorted contours. Construct a mask that reveals only the current "bubble" for the question, apply the mask to the thresholded image and count the number of non-zero pixels in the bubble area.

    Args:
        page_color: numpy array of colored image.
        thresholded_image: numpy array of thresholded image.
        question_contours: list of question contours.
        path_to_answers: path to csv file with correct question-answers pairs
        num_answers: number of bubbles for a single question.
        num_questions: number of questions on a sheet of paper.
    '''

    answers = read_answers(path_to_answers)

    question_contours = imutils.contours.sort_contours(
        question_contours, method="top-to-bottom")[0]
    correct = 0
    correct_color = (0, 255, 0)
    incorrect_color = (0, 0, 255)

    for (question, i) in enumerate(np.arange(0, len(question_contours), 10)):
        contours = imutils.contours.sort_contours(
            question_contours[i:i + num_answers])[0]
        bubbled = None

        for (j, contour) in enumerate(contours):
            mask = np.zeros(thresholded_image.shape, dtype="uint8")
            cv2.drawContours(mask, [contour], -1, 255, -1)

            mask = cv2.bitwise_and(thresholded_image, thresholded_image, mask=mask)
            total = cv2.countNonZero(mask)

            # if the current total has a larger number of total non-zero pixels, then this is selected answer
            if bubbled is None or total > bubbled[0]:
                bubbled = (total, j)

        if answers[question+1] == bubbled[1]:
            correct += 1
            cv2.drawContours(page_color, [contours[bubbled[1]]], -1, correct_color, 8)
            show_image(page_color)
        else:
            cv2.drawContours(page_color, [contours[bubbled[1]]], -1, incorrect_color, 8)
            cv2.drawContours(page_color, [contours[answers[question+1]]], -1, correct_color, 8)
            show_image(page_color)

    print('*************************')
    print('Final score: ' + str(int(correct/len(answers.keys()) * 100)) + '%')
    print('*************************')