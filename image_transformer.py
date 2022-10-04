import cv2
import os
import numpy as np

class ImageTransformer:
	def __init__(self):

		self.table = {
			200 : '░',
			150 : '▒',
			100: '▓	',
			50: '█',
		}


	def __call__(self, image: np.uint8, size: tuple = (128, 64)):
		image = self.__pre_process(image, size)
		text_img = self.__transform(image, size)
		
		return text_img
	
	def __pre_process(self, image: np.uint8, size: tuple):
		"""
			Takes:
				Image
			Process:
				Grayscale > AdaptiveThreshold > Resize > Reshape
			Returns:
				Image
		"""
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 199, 5)
		thresh = cv2.resize(thresh, size)
		input_image = thresh.flatten()

		return input_image

	def __transform(self, image: np.uint8, size: tuple):
		"""
			Takes 
				Image, Size
			Returns
				Text As Image
		"""
		text_list = np.full(size[0] * size[1], " ", dtype=str)
		
		for key, value in self.table.items():
			text_list[np.where(image < key)] = value
		
		text_list = text_list.reshape((size[1],size[0]))
		text_img = '\n'.join([''.join(text) for text in text_list])

		return text_img


if __name__ == '__main__':
	import time
	def image_example():
		it = ImageTransformer()
		image = cv2.imread('sinanengin.jpg')
		text_img = it(image)
		print(text_img)
	
	def video_example():
		it = ImageTransformer()
		filename = "sinanengin.mp4"
		cap = cv2.VideoCapture(filename)
		while True:
			ret, image = cap.read()
			if ret:
				text_img = it(image, (200, 60))
				#os.system('cls')
				print('\n'*80)
				print(text_img)
				time.sleep(0.1)
			else:
				raise(f'Could\'nt get frames from {filename}')
		
	video_example()
		