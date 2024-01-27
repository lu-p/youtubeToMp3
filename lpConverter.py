# -*- coding: utf-8 -*-

import PySimpleGUI as sg 
import pyperclip, time, threading, os, pytube



# Funzione di copia
def copy_clipboard():
# Restituisce il contenuto degli appunti come stringa e li cancella 
    clipboard=pyperclip.paste()
    pyperclip.copy("")
    return clipboard


# Thread di selezione degli url
def selectVideoUrl():
    global listaUrl
    global testoConsole
    global window, values
    
    print("Start selection thread")
    while selVideoUrlVar==True:
        time.sleep(0.1)
    # testoConsole=testoConsole + "\n" + "Start selecting video"
    # window["testoConsole"].update(testoConsole)    
    
        urlGuess=""
        while selectVar==True:
            time.sleep(1)
                        
            clipboard=copy_clipboard()
            # print("urlGuess: ", urlGuess)
            # print("clipboard: ", clipboard)
        
            if urlGuess != clipboard:
                urlGuess = clipboard
                
                # single video
                try:
                    ytObj = pytube.YouTube(urlGuess)
                    testoConsole=testoConsole + urlGuess + "selected.\n"
                    window["testoConsole"].update(testoConsole)

                    downloadVideo(ytObj, values["formatCombo"], values["folderBrowse"])
                    
                except:
                    
                    #  playlist
                    try:
                        play_list = pytube.Playlist(urlGuess)
                        
                        for video in play_list.videos:
                            downloadVideo(video, values["formatCombo"], values["folderBrowse"])

                    
                    except:
                        testoConsole=testoConsole + urlGuess + " is invalid\n"
                        window["testoConsole"].update(testoConsole)
                    
                urlGuess=""


    print("Brake selectVideoUrl thread")


# Funzione di download
def downloadVideo(ytObj, outputFormat, destinationFolder):
    global testoConsole
    global window
    
    testoConsole=testoConsole + "\n" + "Starting new download..."
    window["testoConsole"].update(testoConsole)


    # extract only audio
    video = ytObj.streams.filter(only_audio=True).first()

    # # download the file
    out_file = video.download(output_path=destinationFolder)

    # save the file
    base, ext = os.path.splitext(out_file)
    new_file = base + '.'+outputFormat
    
    if not os.path.isfile(new_file):
        os.rename(out_file, new_file)
    else:
        testoConsole=testoConsole + "\n" + "ERROR: file " + new_file + " already exists. Conversion failed.\n"
        window["testoConsole"].update(testoConsole)
  
    # result of success
    testoConsole = testoConsole + "\n" + ytObj.title + " successfully downloaded.\n"
    window["testoConsole"].update(testoConsole)
   
   
    testoConsole=testoConsole + "\n" + "Download ended.\n"
    window["testoConsole"].update(testoConsole)
   
    
# GUI function (main thread)
def eventLoop():
    global selectVar
    global listaUrl
    global selVideoUrlVar
    global window, values, testoConsole
    
    
    while True:
        time.sleep(0.1)
        event, values = window.read()
        
        
        # Start copying youtube url into clipboard to convert and download videos
        if event == "startButton":
            
            pyperclip.copy("")
            selectVar=True

            window["startButton"].update(disabled=True)
            window["stopButton"].update(disabled=False)
            window["folderBrowse"].update(disabled=True)
            window["formatCombo"].update(disabled=True)
            
            testoConsole=testoConsole + "- Open your youtube video\n- Copy video url\n- Download will start automatically\n(copy only required, paste unnecessary)\n"
            window["testoConsole"].update(testoConsole)
            
            
        # Stop url selection, enable option editing
        elif event=="stopButton":
            selectVar=False

            window["startButton"].update(disabled=False)
            window["stopButton"].update(disabled=True)
            window["folderBrowse"].update(disabled=False)
            window["formatCombo"].update(disabled=False)


        # Edit destination folder
        elif event=="folderBrowse":
            print("jndfkj")
            testoConsole=testoConsole + "Destination folder set to " + values["folderBrowse"] + ".\n"
            window["testoConsole"].update(testoConsole)
        
        
        # Edit output format
        elif event=="formatCombo":
            testoConsole=testoConsole + "Output format set to " + values["formatCombo"] + ".\n"
            window["testoConsole"].update(testoConsole)


        # Show help
        elif event=="helpButton":
            testoConsole=testoConsole + "Help coming soon. Please, don't get angry =D.\n"
            window["testoConsole"].update(testoConsole)
        
        
        # End program if user closes window
        elif event == sg.WIN_CLOSED:
            selectVar=False
            selVideoUrlVar=False
            break
    
    window.close()
    
    


# Graphic set up
testoConsole="Welcome to the converter.\n"
formatList=["mp3", "mp4"]
frameLayout=[
             sg.Column([[sg.Text(testoConsole,
                                  key="testoConsole",
                                  background_color='white',
                                  text_color='black',
                                  size=(300, 200),
                                  pad=False)]],
                                  pad=False,
                                   scrollable=True,
                                   expand_y=True)#,
                                  # vertical_scroll_only=True)
             ]

mainLayout = [
          [sg.Text("Output format"), sg.Combo(formatList, formatList[0], key="formatCombo", enable_events=True), sg.Text("\t\t"), sg.Button("Help", key='helpButton')],
          [sg.Text("Destination folder: ", key="destinationFolder"), sg.FolderBrowse(key="folderBrowse", button_text="Select folder", enable_events=True, initial_folder=os.getcwd())],
          [sg.Button("Start", key="startButton", disabled=False), sg.Button("Stop", key="stopButton", disabled=True, pad=20)],
          [sg.Text("Runtime output")],
          [sg.Frame(title="",
                    layout=[frameLayout],
                    title_color='black',
                    size=(325, 150),
                    pad=False,
                    title_location='nw')
          ]
         ]

window = sg.Window(title="Youtube to audio converter", layout=mainLayout, margins=(40,40), size=(400, 400), element_padding=5)


# Conversion thread
global values
selectVar=False
selVideoUrlVar=True
selVideoUrl = threading.Thread(target=selectVideoUrl)
selVideoUrl.start()


# Graphic loop
eventLoop()




