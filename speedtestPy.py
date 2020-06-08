""" 
SPEEDTEST Application
Author: elfersar
"""


# Imports
import _thread as td
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sys, speedtest, datetime, time, platform

# Global Var
global root, version, me
version = "1.1"
me = "https://github.com/elfersar"


class speedapp:
	# Is the prgram working (w), is there a result to work with in the calculator (t)
	w = True
	r = False
	# Define farme in root window
	def __init__(self, window):
		frame = tk.Frame(window)
		frame.grid()

		# Header
		self.label_1 = tk.Label(frame, text="Speedtest by elfersar", width=35)
		self.label_1.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

		# Text Box
		self.text = tk.Text(frame, borderwidth=2, relief="groove", width=35, height=20)
		self.text.config(state="disabled")
		self.text.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

		# Calculate Button
		self.btn_calc = tk.Button(frame, text="Calculator", width=20, command=self.show_calculator)
		self.btn_calc.grid(row=2,column=0, padx=5, pady=5)

		# Start Button
		self.btn_start = tk.Button(frame, text="Start", width=10, command=lambda: td.start_new_thread(self.speedtestPy, ()))
		self.btn_start.grid(row=3, stick="s", padx=5, pady=5)

		# About Button
		self.btn_about = tk.Button(frame, text="About", width=10, command=self.msgboxAbout)
		self.btn_about.grid(row=3, stick="w", padx=5, pady=5)

		# Exit Button
		self.btn_exit = tk.Button(frame, text="Exit",  width=10, command=frame.quit)
		self.btn_exit.grid(row=3, sticky="e", padx=5, pady=5)

		# Status Bar
		self.info = tk.StringVar()
		self.info.set(" Version: {}".format(version))
		self.statusbar = tk.Label(frame, textvariable=self.info, bd=1, relief="sunken", anchor="w", width=43)
		self.statusbar.grid(row=5)

		# Say hello world
		self.welcometext()

	# Change content in text Box
	def writetext(self, line):
		self.text.config(state="normal")
		self.text.insert(tk.INSERT, line + "\n")
		self.text.config(state="disabled")

	# Clear the whole text
	def cleartext(self):
		self.text.config(state="normal")
		self.text.delete("1.0", "end")
		self.text.config(state="disabled")

	# Display welcome message
	def welcometext(self):
		msg = "Welcome to my little script.\n\nThis programm will show your\ncurrent state of your\ninternet connection.\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nPress start to test the connection!" 

		self.text.config(state="normal")
		self.text.insert(tk.INSERT, msg)
		self.text.config(state="disabled")

	def msgboxAbout(self):
		messagebox.showinfo("About","Version: {}\nAuthor: elfersar\n\nFeel free to give me feedback on\n{}".format(version, me))

	# Show the user that the speedtest is running
	def showProcess(self):
		self.w = True
		while self.w == True:
			self.info.set(" Working |")
			time.sleep(0.3)
			self.info.set(" Working /")
			time.sleep(0.3)
			self.info.set(" Working -")
			time.sleep(0.3)
			self.info.set(" Working \\")
			time.sleep(0.3)
		self.info.set(" Version: {}".format(version))

	def speedtestPy(self):

		# Start timestamp
		start_total = time.time()

		# Clear text Box an disable START / CALC Button
		self.cleartext()
		self.btn_start.config(state="disable")
		self.btn_calc.config(state="disable")

		# Call showProcess() in new Thread
		td.start_new_thread(self.showProcess, ())

		self.writetext("SPEEDTEST | Version: {}".format(version))
		time.sleep(1)
		self.writetext("\n1. Connecting to Server ...")

		# Building connection and when not quit method
		try:
			server = speedtest.Speedtest()
			server.get_best_server()
		except:
			self.writetext("ERROR: Cant't connect to Server.\nPlease check your Connecting!\n")
			quit()

		# Measure download
		self.writetext("2. Measure...	'DOWNLOAD'")
		start_download = time.time()
		server.download()
		end_download = time.time()

		# Measure upload
		self.writetext("3. Measure...	'UPLOAD'")
		start_upload = time.time()
		server.upload()
		end_upload = time.time()

		# Sum up results
		ergebnisse = server.results.dict()
		time_download = time.strftime("%S s", time.gmtime(end_download - start_download))
		time_upload = time.strftime("%S s", time.gmtime(end_upload - start_upload))

		# Converting results from str to int an convert bit/s in mbits/s
		self.mbit_download = int(ergebnisse["download"]/1000000)
		self.mbit_upload = int(ergebnisse["upload"]/1000000)
		ping_in_ms = int(ergebnisse["ping"])

		# Break the loop in showProcess() and tell that we have tested
		self.w = False
		self.r = True

		# Display results
		self.writetext("\n---RESULTS---\n")
		time.sleep(1.5)
		self.writetext("\nDOWNLOAD: {} Mbit/s".format(self.mbit_download))
		self.writetext("UPLOAD: {} Mbits/s".format(self.mbit_upload))
		self.writetext("PING: {} ms\n".format(ping_in_ms))
		self.writetext("Date: {} ".format(datetime.datetime.now().strftime("%H:%M:%S Uhr - %d.%m.%Y \n")))

		# End timestamp
		end_total = time.time()
		time_total = time.strftime("%S s", time.gmtime(end_total - start_total))
		time_download = time.strftime("%S s", time.gmtime(end_download - start_download))
		time_upload = time.strftime("%S s", time.gmtime(end_upload - start_upload))

		self.writetext("\nFinished Download: {} ".format(time_download))
		self.writetext("Finished Upload: {} ".format(time_upload))
		self.writetext("Finished Test in: {} ".format(time_total))

		# Enable START / CALC Button
		self.btn_start.config(state="normal")
		self.btn_calc.config(state="normal")

	def show_calculator(self):
		# Calculator window
		self.root_calc = tk.Tk()
		self.root_calc.resizable(width=False, height=False)
		self.root_calc.title("Connection Calculator")
		# System check for icon
		s = str(platform.system())
		if s == "Windows":
			self.root_calc.iconbitmap("images/speedicon.ico")
		# Window position
		windowWidth = self.root_calc.winfo_reqwidth()
		windowHeight = self.root_calc.winfo_reqheight()
		positionRight = int(self.root_calc.winfo_screenwidth()/2 - windowWidth/3.1)
		positionDown = int(self.root_calc.winfo_screenheight()/2 - windowHeight)
		self.root_calc.geometry("+{}+{}".format(positionRight, positionDown))


		# Place Widgets in Calculator Frame
		frame_calc = tk.Frame(self.root_calc)
		frame_calc.grid()

		# Topic
		label_calc = tk.Label(frame_calc, text="Connection Calculator \n WORK IN PROGRESS", width=30)
		label_calc.grid(row=0, padx=5, pady=5)

		# Exit Button
		btn_exitCalc = tk.Button(frame_calc, text="Exit", width=53, command=lambda: self.root_calc.destroy())
		btn_exitCalc.grid(row=10, padx=2, pady=3)

		# Is there a result to work with?
		if self.r == False:
			# Show Info
			info = "Please run the test first."
			label_testresults = tk.Label(frame_calc, text=info)
			label_testresults.grid(row=1, padx=5, pady=5)

		else:
			# Show the Results ones more
			testresults = "Download: {} Mbits, Upload: {} Mbits".format(self.mbit_download, self.mbit_upload)
			label_testresults = tk.Label(frame_calc, text=testresults)
			label_testresults.grid(row=1, padx=5, pady=5)

			# Text Box
			self.box = tk.Text(frame_calc, borderwidth=2, relief="groove", width=47, height=13)
			self.box.config(state="disabled")
			self.box.grid(row=2, padx=2, pady=5)

			# Say the user what to do
			label_maual = tk.Label(frame_calc, text="Enter a number in MB...")
			label_maual.grid(row=3, padx=2, pady=2, sticky="w")

			# Calculate DOWNLOAD Button
			btn_calculate = tk.Button(frame_calc, text="Calculate -- DOWNLOAD", width=25, command= self.calc_user_download_input)
			btn_calculate.grid(row=5, padx=5, pady=1, sticky="w")

			# Calculate UPLOAD Button
			btn_calculate = tk.Button(frame_calc, text="Calculate -- UPLOAD", width=25, command= self.calc_user_upload_input)
			btn_calculate.grid(row=5, padx=5, pady=1, sticky="e")

			# Entry form
			self.inp_user = tk.Entry(frame_calc, bg="white", width=20)
			self.inp_user.grid(row=4, padx=2, pady=2)

			# Calculate the Data
			self.mbps_download = (self.mbit_download / 0.8) / 10
			self.mbps_upload = (self.mbit_upload / 0.8) / 10
			self.gb_1_download = round(float((1000 / self.mbps_download) / 60), 2)
			self.gb_10_download = round(float((10000 / self.mbps_download) / 60), 2)
			self.gb_1_upload = round(float((1000 / self.mbps_upload) / 60), 2)
			self.gb_10_upload = round(float((10000 / self.mbps_upload) / 60), 2)

			# Display calculation in box
			self.box.config(state="normal")
			self.box.insert(tk.INSERT, "Download: {} Mbps\nUpload: {} Mbps\n\n".format(self.mbps_download, self.mbps_upload))
			self.box.insert(tk.INSERT, "DOWNLOAD:\n1GB needs {} min, 10GB needs {} min\n\n".format(self.gb_1_download, self.gb_10_download))
			self.box.insert(tk.INSERT, "UPLOAD:\n1GB needs {} min, 10GB needs {} min\n".format(self.gb_1_upload, self.gb_10_upload))
			self.box.insert(tk.INSERT, "_______________________________________________\n\n")
			self.box.config(state="disabled")


		# Start calculator Window
		self.root_calc.mainloop()

	# Calculate the user input DOWNLOAD
	def calc_user_download_input(self):
		try:
			userMB = round(float(self.inp_user.get()), 2)
			userCalc = round(float((userMB / self.mbps_download) / 60), 2)
			self.box.config(state="normal")
			self.box.insert(tk.INSERT, "You need {} min to download {} MB!\n".format(userCalc, userMB))
			self.box.config(state="disabled")
			self.box.yview_pickplace("end")
		except:
			messagebox.showinfo("Information",'Please enter a valid number!\n\nUse " . " instead of " , " ! ')


	# Calculate the user input UPLOAD
	def calc_user_upload_input(self):
		try:
			userMB = round(float(self.inp_user.get()), 2)
			userCalc = round(float((userMB / self.mbps_upload) / 60), 2)
			self.box.config(state="normal")
			self.box.insert(tk.INSERT, "You need {} min to upload {} MB!\n".format(userCalc, userMB))
			self.box.config(state="disabled")
			self.box.yview_pickplace("end")
		except:
			messagebox.showinfo("Information",'Please enter a valid number!\n\nUse " . " instead of " , " ! ')

	


if __name__ == '__main__':
	# Mainwindow
	root = tk.Tk()

	root.resizable(width=False, height=False)
	root.title("Speedtest")

	# System check for icon
	s = str(platform.system())
	if s == "Windows":
		root.iconbitmap("images/speedicon.ico")

	# Window position
	windowWidth = root.winfo_reqwidth()
	windowHeight = root.winfo_reqheight()
	positionRight = int(root.winfo_screenwidth()/2 - windowWidth/1.2)
	positionDown = int(root.winfo_screenheight()/2 - windowHeight)
	root.geometry("+{}+{}".format(positionRight, positionDown))


	# Run Application
	speedapp(root)
	root.mainloop()
