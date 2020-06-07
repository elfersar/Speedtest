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
global version, me
version = "1.0"
me = "https://github.com/elfersar"


class speedapp:
	w = True
	# Define Window
	def __init__(self, window):
		frame = tk.Frame(window)
		frame.grid()

		# Überschrift
		self.label_1 = tk.Label(frame, text="Speedtest by elfersar", width=35)
		self.label_1.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

		# Text Box
		self.text = tk.Text(frame, borderwidth=2, relief="groove", width=35, height=20)
		self.text.config(state="disabled")
		self.text.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

		# Hinweis
		self.label_1 = tk.Label(frame, text="Press start to test your connection...", width=35)
		self.label_1.grid(row=2,column=0, padx=5, pady=5)

		# Start Button
		self.btn_start = tk.Button(frame, text="Start", width=10, command=self.speedtestPy_Thread)
		self.btn_start.grid(row=3, stick="s", padx=5, pady=5)

		# About Button
		self.btn_about = tk.Button(frame, text="About", width=10, command=self.msgboxAbout)
		self.btn_about.grid(row=3, stick="w", padx=5, pady=5)

		# Exit Button
		self.btn_exit = tk.Button(frame, text="Exit",  width=10, command=frame.quit)
		self.btn_exit.grid(row=3, sticky="e", padx=5, pady=5)

		# Progress Bar
		#self.progressBar = ttk.Progressbar(frame, length=345, mode="indeterminate", orient="horizontal")

		# Status Bar
		self.info = tk.StringVar()
		self.info.set(" Version: {}".format(version))
		self.statusbar = tk.Label(frame, textvariable=self.info, bd=1, relief="sunken", anchor="w", width=38)
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
		msg = "Welcome to my little script.\n\nThis programm will show your\ncurrent state of your\ninternet connection." 

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

		# Clear text Box an disable START Button
		self.cleartext()
		self.btn_start.config(state="disable")

		# Call showProcess() in new Thread
		td.start_new_thread(self.showProcess, ())

		# Progress Bar start
		#self.progressBar.grid(row=4)
		#self.progressBar.start()

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
		mbit_download = int(ergebnisse["download"]/1000000)
		mbit_upload = int(ergebnisse["upload"]/1000000)
		ping_in_ms = int(ergebnisse["ping"])

		# Break the loop in showProcess()
		self.w = False

		# Progress Bar stop
		#self.progressBar.grid_forget()
		#self.progressBar.stop()

		# Display results
		self.writetext("\n---RESULTS---\n")
		time.sleep(1.5)
		self.writetext("\nDOWNLOAD: {} Mbit/s".format(mbit_download))
		self.writetext("UPLOAD: {} Mbits/s".format(mbit_upload))
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

		# Enable START Button
		self.btn_start.config(state="normal")

	# Run the speedtest in new Thread
	def speedtestPy_Thread(self):
		td.start_new_thread(self.speedtestPy, ())
		


if __name__ == '__main__':
	# Mainwindow
	root = tk.Tk()
	root.resizable(width=False, height=False)
	root.title("Speedtest")

	# System check
	s = str(platform.system())
	if s=="Windows":
		root.iconbitmap("images/speedicon.ico")

	# Window position
	windowWidth = root.winfo_reqwidth()
	windowHeight = root.winfo_reqheight()
	positionRight = int(root.winfo_screenwidth()/2 - windowWidth/1.2)
	positionDown = int(root.winfo_screenheight()/2 - windowHeight)
	root.geometry("+{}+{}".format(positionRight, positionDown))


	# Run Application
	sui = speedapp(root)
	root.mainloop()




