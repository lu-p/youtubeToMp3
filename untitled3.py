# -*- coding: utf-8 -*-

import PySimpleGUI as sg 
import pyperclip, time, threading, os, pytube



# Funzione di copia
def copy_clipboard():
# Restituisce gli appunti come stringa e li cancella 
    clipboard=pyperclip.paste()
    pyperclip.copy("")
    return clipboard


# Thread di selezione degli url
def selectVideoUrl():
    global listaUrl
    global testoConsole
    global window
    
    print("Start selection thread")
    while selVideoUrlVar==True:
        time.sleep(0.1)
    # testoConsole=testoConsole + "\n" + "Start selecting video"
    # window["testoConsole"].update(testoConsole)    
    
        urlGuess=""
        while selectVar==True:
            time.sleep(0.1)
        
            urlGuess = copy_clipboard()
            
            if urlGuess!="" and (listaUrl==[] or urlGuess != listaUrl[-1]):
                
                try:
                    yt = pytube.YouTube(urlGuess)
                    print(urlGuess)
                    testoConsole=testoConsole + "\n" + urlGuess + "selected"
                    window["testoConsole"].update(testoConsole)
                    listaUrl.append(urlGuess)
                    print("ok")
                except:
                    testoConsole=testoConsole + "\n" + urlGuess + "is invalid"
                    window["testoConsole"].update(testoConsole)
    
    print("Brake thread selectVideoUrl")


# Funzione di download
def downloadVideo(outputFormat, destinationFolder):
    global listaUrl
    global testoConsole
    global window
    
    print("Start downloading videos")
    testoConsole=testoConsole + "\n" + "Start downloading video"
    window["testoConsole"].update(testoConsole)  
    
    
    destination=destinationFolder

    for url in listaUrl:

        yt = pytube.YouTube(url) # ripetizione

        # extract only audio
        video = yt.streams.filter(only_audio=True).first()

        # # download the file
        out_file = video.download(output_path=destination)

        # save the file
        base, ext = os.path.splitext(out_file)
        new_file = base + '.'+outputFormat
        os.rename(out_file, new_file)
      
        # result of success
        testoConsole = testoConsole + "\n" + yt.title + " has been successfully downloaded"
        window["testoConsole"].update(testoConsole)
        print(yt.title + " has been successfully downloaded.")
   
   
    print("Downloading ended")
    testoConsole=testoConsole + "\n" + "Downloading ended"
    window["testoConsole"].update(testoConsole)
   
    
def eventLoop():
    global selectVar
    global listaUrl
    global selVideoUrlVar
    global window, testoConsole
    
    
    while True:
        time.sleep(0.1)
        event, values = window.read()
        print(event)
        print(values)
        if event == "selectButton":
            
            window["selectButton"].update(disabled=True)

            selectVar=True
            
            testoConsole=testoConsole + "\n" + "Start video selection"
            window["testoConsole"].update(testoConsole)
            
        elif event=="downloadButton":

            window["downloadButton"].update(disabled=True)
            window["folderBrowse"].update(disabled=True)
            window["formatCombo"].update(disabled=True)

            selectVar=False
            downloadVideo(values["formatCombo"], values["folderBrowse"])
            listaUrl=[]
            
            window["downloadButton"].update(disabled=False)
            window["selectButton"].update(disabled=False)
            window["folderBrowse"].update(disabled=False)
            window["formatCombo"].update(disabled=False)
            
        elif event=="folderBrowse":
            window["destinationFolder"].update("Destination folder: "+ values["folderBrowse"])
            testoConsole=testoConsole + "\n" + "Destination folder set to " + values["folderBrowse"]
            window["testoConsole"].update(testoConsole)
            
        elif event=="formatCombo":
            testoConsole=testoConsole + "\n" + "Output format set to " + values["formatCombo"]
            window["testoConsole"].update(testoConsole)
            
        elif event=="Help":
            pass
        
        # End program if user closes window
        elif event == sg.WIN_CLOSED:
            selectVar=False
            selVideoUrlVar=False
            break
    
    window.close()
    
    


# Grafica
testoConsole="Hello from the converter"
formatList=["mp3", "mp4"]
frameLayout=[
             sg.Column([[sg.Text(testoConsole,
                                  key="testoConsole",
                                  background_color='white',
                                  text_color='black',
                                  size=(300, 200),
                                  pad=False)]],
                                  pad=False,
                                   scrollable=True)#,
                                  # vertical_scroll_only=True)
             ]

layout = [
          [sg.Text("Ouput format"), sg.Combo(formatList, formatList[0], key="formatCombo", enable_events=True), sg.Text("\t\t"), sg.Button("Help")],
          [sg.Text("\n")],
          [sg.Text("Destination folder: ", key="destinationFolder")],
          [sg.FolderBrowse(key="folderBrowse", enable_events=True)],
          [sg.Text("\n")],
          [sg.Button("Select", key="selectButton", disabled=False), sg.Button("Download", key="downloadButton", disabled=False)],
          [sg.Text("\n\nRuntime output")],
          [sg.Frame(title="",
                    layout=[frameLayout],
                    title_color='black',
                    size=(300, 100),
                    pad=False,
                    title_location='nw')
          ]
         ]

margins=(40, 40)
size=(400, 400)
window = sg.Window(title="Python youtube converter", layout=layout, margins=margins, size=size)


# Thread di selezione
selectVar=False
selVideoUrlVar=True
listaUrl = []
selVideoUrl = threading.Thread(target=selectVideoUrl)
selVideoUrl.start()


eventLoop()



