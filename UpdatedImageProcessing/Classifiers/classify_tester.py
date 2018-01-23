import sys
from os import walk
import numpy as np
import json
import timeit

from classify_color import ColorClassifier

class ClassifierTester(object):
	"""
	Provides convenience functions to extended classes.
	"""

	def str_is_int(self, s):
		"""

		Borrowed from:
			https://stackoverflow.com/a/1267145
		"""
		try: 
			int(s)
			return True
		except ValueError:
			return False

	def compare_results(self, answer_dir, answer_field, results, verbose=False):
		"""
		Check to see if the results generated by a classifier are correct/not.

		:param answer_dir:		directory of the answers in JSON files.
		:param answer_field:	field within the JSON file where the answer is.

								accepts multiple fields. for example, if the
								answer field is in ["targets"][0]["shape_color"],
								then you pass in answer_field:

								"targets.0.shape_color"
		:param results:			one-dimensional list with each index
								corresponding with the answer file.
		:param verbose:			highly detailed output. default: false for off.
		"""
		start = timeit.default_timer()

		# load answers
		answers_files = []

		for(dirpath, dirnames, filenames) in walk(answer_dir):
			answers_files = filenames

		answers_files.sort(key=lambda f: int(filter(str.isdigit, f)))

		answers_files = answers_files[0:len(results)]

		if verbose:
			print("classifier.py: Loading in answer files...")

		answers = []

		for answer_file in answers_files:
			p = json.load(open(answer_dir + answer_file))

			for i in answer_field.split("."):
				if self.str_is_int(i):
					p = p[int(i)]
				else:
					p = p[i]

			answers.append(p)

			if verbose:
				print("classifier.py: Loaded answer '" + str(p) + "' for image #" + str(len(answers)) + " from '" + answer_dir + answer_file + "' .")

		print("classifier.py: Loaded " + str(len(answers)) + " answers.")

		if verbose:
			print("classifier.py: Starting answer result comparison.")

		# compare
		i = 0 

		correct = 0
		false   = 0

		for result in results:
			if str(result) == str(answers[i][0]):
				correct += 1

				if verbose:
					print("classifier.py: CORRECT: image #" + str(i + 1) + " identified CORRECTLY as " + str(answers[i][0]) + ".")
			else:
				false += 1

				if verbose:
					print("classifier.py: WRONG:   image #" + str(i + 1) + " identified INCORRECTLY as " + str(result) + ". Answer was " + str(answers[i][0]) + ".")

			i += 1

		if verbose:
			print("classifier.py: Completed comparison.")
			print("")

		print("### COMPARE RESULTS ###")

		end = timeit.default_timer()

		print("Compared " + str(i) + " results in " + str(round(end - start, 7) * 1000000) + " ms")
		print("Looked at field " + answer_field)
		print("")
		print("Results:")
		print("  Correctly identified images:   " + str(correct))
		print("  Incorrectly identified images: " + str(false))
		print("")
		print("  Success rate: " + str( round( float(correct) / float(len(answers)), 4 ) * 100.0 ) + "%")
		print("")


def load_images(image_dir, count=sys.maxint):
	"""
	Import all (or a specific number of) the target images from a specified 
	directory.
	:param image_dir:	target images dir. ex: "targets/single_targets"
	:param count:		number of images to load, starting from the lowest
						file name ascending.
						ex: 
						when count=3:
						["1.jpg", "2.jpg", "3.jpg"]
	"""
	for (dirpath, dirnames, filenames) in walk(image_dir):
		imgs = filenames
		break

	imgs.sort(key=lambda f: int(filter(str.isdigit, f)))

	imgs = np.array(imgs)

	if count != sys.maxint:
		imgs = imgs[0:count]

	return imgs


if __name__ == '__main__':
	main = ClassifierTester()
	
	directory = "../../../image-processing/targets_new/single_targets"

	imgs = load_images(directory, count=10)
	results = []

	for img in imgs:
		test = ColorClassifier(directory + "/" + img)
		results.append(test.get_color()[0]) # [0] for shape_color, [1] for alphanumeric_color

	# for shape color: "targets.0.shape_color"
	# for text color:  "targets.0.alphanumeric_color"
	main.compare_results(directory + "_answers/", "targets.0.shape_color", results, verbose=True)

