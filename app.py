import cv2
import time

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from threading import Thread

from image_transformer import ImageTransformer

class App:
	def __init__(self):
		self.it = ImageTransformer()
		self.supported_images = ['jpg', 'jpeg', 'png', 'tif', 'tiff']
		self.supported_videos = ['avi', 'mp4']
		self.text = ''
		self.size = (200, 60)
		self.is_image = False
		self.filename = ""
		self.thread_work = True

		self.process_thread = Thread(target = self.__process)
		self.process_thread.daemon = True

		self.__build_window()

	def __build_window(self):
		self.window = Tk()
		self.window.title("Image To Text App")
		self.window.geometry("1280x720")
		
		# Image Will Be Shown Here
		self.text_box = Text(self.window, bg = "light yellow", font=("Helvetica", 1))
		self.text_box.place(relx = 0.05, rely = 0.05, relwidth=.7,  relheight=.9, anchor = NW)
		self.text_box.config(state='disabled')
		
		# Open Button
		self.button = ttk.Button(self.window, text="Open File", command = self.__openfile)
		self.button.place(relx = 0.825, rely = 0.05, relwidth=.1,  relheight=.1, anchor = NW)

		# Zoom Buttons
		self.zoom_in = ttk.Button(self.window, text="Zoom In", command = self.__zoom_in)
		self.zoom_in.place(relx = 0.8, rely = 0.25, relwidth=.05,  relheight=.05, anchor = NW)

		self.zoom_out = ttk.Button(self.window, text="Zoom out", command = self.__zoom_out)
		self.zoom_out.place(relx = 0.9, rely = 0.25, relwidth=.05,  relheight=.05, anchor = NW)

		# Stop Button
		self.stop_button = ttk.Button(self.window, text="Stop", command = self.__stop)
		self.stop_button.place(relx = 0.825, rely = 0.4, relwidth=.1,  relheight=.1, anchor = NW)

		self.window.mainloop()
	
	def __run_thread(self):
		
		if self.process_thread.is_alive():
			self.thread_work = False
		time.sleep(0.2)

		self.process_thread = Thread(target = self.__process)
		self.process_thread.daemon = True
		self.process_thread.start()

	def __zoom_in(self):
		self.size = tuple([int(x*1.1) for x in self.size])
		if self.is_image:
			self.__run_thread()
	
	def __zoom_out(self):
		self.size = tuple([int(x*0.9) for x in self.size])
		if self.is_image:
			self.__run_thread()
	
	def __update_text(self):
		self.text_box.config(state='normal')
		self.text_box.delete('1.0', END)
		self.text_box.insert(END, self.text)
		self.text_box.config(state='disabled')

	def __openfile(self):
		self.thread_work = False
		self.filename = filedialog.askopenfilename()
		self.__run_thread()
	
	def __stop(self):
		self.thread_work = False
		  
	def __process(self):
		extension = self.filename.split(".")[-1]
		if extension in self.supported_images:
			self.__process_image(self.filename)
		elif extension in self.supported_videos:
			self.__process_video(self.filename)
		else:
			raise Exception("Not Supported Source Type")

	def __process_video(self, filename):
		self.thread_work = True
		self.is_image = False

		cap = cv2.VideoCapture(filename)

		while self.thread_work:
			ret, image = cap.read()
			if ret:
				text_img = self.it(image, self.size)
				self.text = text_img
				self.__update_text()
			else:
				break

	def __process_image(self, filename):
		self.is_image = True
		image = cv2.imread(filename)
		if image is not None:
			text_img = self.it(image, self.size)
			self.text = text_img
			self.__update_text()
		else:
			raise Exception(f'Could\'nt get image from {filename}')



app = App()