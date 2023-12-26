"""
Carsten Engelke (c) 2023
"""
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
import math
import time
from urllib import request
from threading import Thread


class URLDownloaderApp:
    def createURLList(app):
        listinput = list()
        if app.urlSourceEntry.get() != "":
            listinput.append(app.urlSourceEntry.get())
        if app.urlSourceFile.get() != "":
            with open(app.urlSourceFile.get()) as file:
                for line in file.readlines():
                    listinput.append(line)
        lowerRange = app.startNumber.get()
        upperRange = app.endNumber.get()
        useLeadingZeroes = app.leadingZeroes.get()
        listTxt = list()
        for txt in app.replacetxtText.get("1.0", "end").split("\n"):
            if txt != "":
                listTxt.append(txt)
        resultlist = list()
        for inputURL in listinput:
            for i in range(lowerRange, upperRange + 1):
                lead = ""
                if useLeadingZeroes:
                    maxlen = math.floor(math.log10(upperRange))
                    if i != 0:
                        lead = (maxlen - math.floor(math.log10(i))) * "0"
                    else:
                        lead = (maxlen - math.floor(math.log10(1))) * "0"
                replaceNumber = lead + str(i)
                resultstr = inputURL.replace("<>", replaceNumber)
                if len(listTxt) > 0 and "<txt>" in resultstr:
                    for txt in listTxt:
                        resultlist.append(resultstr.replace("<txt>", txt))
                else:
                    resultlist.append(resultstr)
        return resultlist

    def updatePreview(app):
        app.previewText.delete(0.0, "end")
        preview = ""
        for line in app.createURLList():
            preview += line + "\n"
        app.previewText.insert(0.0, preview)

    def resetMessage(app):
        app.statusMessage.set(
            "Replaces '<>' with numbers and '<txt>' with texts provided above"
        )

    def downloadFunction(app):
        for url in app.createURLList():
            filename = url.split("/")[-1]
            try:
                app.statusMessage.set(url + " downloading...")
                request.urlretrieve(url, filename)
            except Exception as e:
                app.statusMessage.set(
                    url + " download failed" + e.with_traceback()
                )
                time.sleep(500)
            app.statusMessage.set(url + " downloaded successfull")

    def download(app):
        Thread(target=app.downloadFunction).start()

    def loadURLFile(app):
        filetypes = (("text files", "*.txt"), ("All files", "*.*"))
        filename = filedialog.askopenfilename(
            title="Open a URL list text file", filetypes=filetypes
        )
        app.urlSourceFile.set(filename)
        app.statusMessage.set(filename)

    def __init__(self, master=None):
        # build ui
        frame1 = ttk.Frame(master)
        frame1.configure(padding=5)
        self.urlFrame = ttk.Labelframe(frame1)
        self.urlFrame.configure(text="URL(s)")
        self.urlSourceEntry = ttk.Entry(self.urlFrame)
        self.urlSourceEntry.configure(takefocus=False)
        self.urlSourceEntry.grid(column=0, columnspan=2, row=0, sticky="ew")
        _text_ = (
            "https://cdn.jsdelivr.net"
            "/gh/belaviyo/download-with/samples/"
            "sample.png"
        )
        self.urlSourceEntry.delete("0", "end")
        self.urlSourceEntry.insert("0", _text_)
        self.urlFileLabel = ttk.Label(self.urlFrame)
        self.urlFileLabel.grid(column=0, row=1, sticky="ew")
        self.loadURLFileButton = ttk.Button(self.urlFrame)
        self.loadURLFileButton.configure(text="load URL list file (*.txt)")
        self.loadURLFileButton.grid(column=1, row=1, sticky="ew")
        self.urlFrame.grid(column=0, columnspan=3, row=0, sticky="nsew")
        self.urlFrame.rowconfigure(0, weight=1)
        self.urlFrame.rowconfigure(1, weight=1)
        self.urlFrame.columnconfigure(0, weight=1)
        self.urlFrame.columnconfigure(1, weight=1)
        self.startNumberEntry = ttk.Entry(frame1)
        self.startNumber = tk.IntVar(value=0)
        self.startNumberEntry.configure(textvariable=self.startNumber)
        _text_ = "1"
        self.startNumberEntry.delete("0", "end")
        self.startNumberEntry.insert("0", _text_)
        self.startNumberEntry.grid(column=1, columnspan=2, row=3, sticky="ew")
        self.endNumberEntry = ttk.Entry(frame1)
        self.endNumber = tk.IntVar(value=100)
        self.endNumberEntry.configure(textvariable=self.endNumber)
        _text_ = "1"
        self.endNumberEntry.delete("0", "end")
        self.endNumberEntry.insert("0", _text_)
        self.endNumberEntry.grid(column=1, columnspan=2, row=4, sticky="ew")
        self.startNumberLabel = ttk.Label(frame1)
        self.startNumberLabel.configure(text="Start:")
        self.startNumberLabel.grid(column=0, row=3)
        self.endNumberLabel = ttk.Label(frame1)
        self.endNumberLabel.configure(text="End:")
        self.endNumberLabel.grid(column=0, row=4)
        self.txtLabel = ttk.Label(frame1)
        self.txtLabel.configure(text="Text:")
        self.txtLabel.grid(column=0, row=6)
        self.replacetxtText = tk.Text(frame1)
        self.replacetxtText.configure(height=5, takefocus=False, width=50)
        self.replacetxtText.grid(column=1, row=6, sticky="ew")
        scrollbar1 = ttk.Scrollbar(frame1)
        scrollbar1.configure(orient="vertical")
        scrollbar1.grid(column=2, row=6, sticky="ns")
        separator1 = ttk.Separator(frame1)
        separator1.configure(orient="horizontal")
        separator1.grid(column=0, columnspan=3, row=7, sticky="ew")
        label5 = ttk.Label(frame1)
        label5.configure(relief="flat", takefocus=False, text="Preview:")
        label5.grid(column=0, row=8, sticky="ew")
        button2 = ttk.Button(frame1)
        button2.configure(text="Update Preview")
        button2.grid(column=0, row=9, sticky="new")
        self.previewText = tk.Text(frame1)
        self.previewText.configure(height=5, width=50)
        self.previewText.grid(column=1, row=8, rowspan=2, sticky="ew")
        scrollbar2 = ttk.Scrollbar(frame1)
        scrollbar2.configure(orient="vertical")
        scrollbar2.grid(column=2, row=8, rowspan=2, sticky="ns")
        separator2 = ttk.Separator(frame1)
        separator2.configure(orient="horizontal")
        separator2.grid(column=0, columnspan=3, row=10, sticky="ew")
        self.downloadButton = ttk.Button(frame1)
        self.downloadButton.configure(takefocus=True, text="Download")
        self.downloadButton.grid(
            column=0, columnspan=3, ipady=10, row=11, sticky="nsew"
        )
        self.statusLabel = ttk.Label(frame1)
        self.statusMessage = tk.StringVar()
        self.statusLabel.configure(
            state="normal", takefocus=True, textvariable=self.statusMessage
        )
        self.statusLabel.grid(column=0, columnspan=3, row=12, sticky="ew")
        self.checkZeroes = ttk.Checkbutton(frame1)
        self.leadingZeroes = tk.BooleanVar()
        self.leadingZeroes.set(True)
        self.checkZeroes.configure(
            offvalue=False,
            onvalue=True,
            state="normal",
            text="leading zeros",
            variable=self.leadingZeroes,
        )
        self.checkZeroes.grid(column=0, columnspan=3, row=5, sticky="ew")
        frame1.pack(expand=True, fill="both", side="top")
        frame1.rowconfigure(10, weight=1)
        frame1.columnconfigure(1, weight=1)

        # set Scrollbars & Buttons
        self.urlSourceFile = tk.StringVar()
        self.urlFileLabel["textvariable"] = self.urlSourceFile
        self.previewText["yscrollcommand"] = scrollbar2.set
        scrollbar2["command"] = self.previewText.yview
        self.replacetxtText["yscrollcommand"] = scrollbar1.set
        scrollbar1["command"] = self.replacetxtText.yview
        button2["command"] = self.updatePreview
        self.downloadButton["command"] = self.download
        self.statusMessage.set(
            "Replaces '<>' with numbers and '<txt>' with texts provided above"
        )
        self.loadURLFileButton["command"] = self.loadURLFile
        frame1.bind("<KeyPress-F1>", self.resetMessage)

        # Main widget
        self.mainwindow = frame1

    def run(self):
        self.mainwindow.mainloop()


def main():  # pragma: no cover
    """
    The main function executes on commands:
    `python -m urldownloader` and `$ urldownloader `.

    This is your program's entry point.
    """
    root = tk.Tk()
    app = URLDownloaderApp(root)
    root.winfo_toplevel().title("pygmea URL batch download tool")
    app.run()


if __name__ == "__main__":
    main()
