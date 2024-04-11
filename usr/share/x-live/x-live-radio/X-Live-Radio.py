#!/usr/bin/python3

import os
import sys
import subprocess
import time
import atexit
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QListWidget, QSlider
from PyQt5.QtCore import QProcess, QTimer, Qt, QSize
from PyQt5.QtGui import QIcon, QPixmap
import json


# Pfad zum gewünschten Arbeitsverzeichnis
arbeitsverzeichnis = os.path.expanduser('/usr/share/x-live/x-live-radio/')

# Das Arbeitsverzeichnis festlegen
os.chdir(arbeitsverzeichnis)


class RadioWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.stream_url = ""
        self.radio_name = []
        self.radio_url = []
        self.new_widget = None

        faktor = app.desktop().height()/720
        self.faktor = app.desktop().height()/720
        sts= int(16 * faktor)
        btn_sel_color = '#1f8973'
        self.song = ""
        self.sswidget=str("""
            QWidget{
            font-size: """ + str(sts) + """px; 
            text-align: center;      
            border-radius: 5px;
            background-color: rgba(25, 25, 25, 115);
            border: 2px solid rgba(125, 125, 125, 115);
            padding-top: 0px;
            padding-left: 0px;
            padding-right: 0px;
            padding-bottom: 0px;
            margin-top: 0px;
            margin-left: 0px;
            margin-right: 0px;
            margin-bottom: 0px;
            color: white;
            }
            """)
        self.ssbtn1=str("""
            QPushButton {
            font-size: """ + str(sts) + """px; 
            text-align: left;      
            border-radius: 10px;
            background-color: rgba(25, 25, 25, 115);
            border: 2px solid rgba(125, 125, 125, 115);
            padding-top: 2px;
            padding-left: 5px;
            padding-right: 5px;
            padding-bottom: 2px;
            color: white;
            }
            QWidget{
            font-size: """ + str(sts) + """px; 
            text-align: center;      
            border-radius: 10px;
            background-color: rgba(125, 170, 125, 185);
            border: 2px solid rgba(125, 125, 125, 185);
            padding-top: 2px;
            padding-left: 5px;
            padding-right: 5px;
            padding-bottom: 2px;
            color: white;
            }
            """)
        self.ssnormal=str("""
            QPushButton {
            font-size: """ + str(sts) + """px; 
            text-align: left;    
            background-color: rgba(25, 25, 25, 0);
            border: 0px;
            padding-top: 0px;
            padding-left: 0px;
            padding-right: 0px;
            padding-bottom: 0px;
            margin-top: 0px;
            margin-left: 0px;
            margin-right: 0px;
            margin-bottom: 0px;
            color: white;
            }
            QSlider {
            font-size: """ + str(sts) + """px; 
            text-align: left;    
            background-color: rgba(25, 25, 25, 0);
            border: 0px;
            padding-top: 0px;
            padding-left: 0px;
            padding-right: 0px;
            padding-bottom: 0px;
            margin-top: 0px;
            margin-left: 0px;
            margin-right: 0px;
            margin-bottom: 0px;
            color: white;
            }
            QLabel {
            font-size: """ + str(sts) + """px; 
            text-align: left;    
            background-color: rgba(25, 25, 25, 115);
            border: 0px;
            padding-top: 0px;
            padding-left: 0px;
            padding-right: 0px;
            padding-bottom: 0px;
            margin-top: 0px;
            margin-left: 0px;
            margin-right: 0px;
            margin-bottom: 0px;
            color: white;
            }
            """)
        self.ssnormal1=str("""
            QPushButton {
            font-size: """ + str(sts) + """px; 
            text-align: center;    
            background-color: rgba(25, 25, 25, 0);
            border: 0px;
            padding-top: 0px;
            padding-left: 0px;
            padding-right: 0px;
            padding-bottom: 0px;
            margin-top: 0px;
            margin-left: 0px;
            margin-right: 0px;
            margin-bottom: 0px;
            color: white;
            }
            QSlider {
            font-size: """ + str(sts) + """px; 
            text-align: center;    
            background-color: rgba(25, 25, 25, 0);
            border: 0px;
            padding-top: 0px;
            padding-left: 0px;
            padding-right: 0px;
            padding-bottom: 0px;
            margin-top: 0px;
            margin-left: 0px;
            margin-right: 0px;
            margin-bottom: 0px;
            color: white;
            }
            QLabel {
            font-size: """ + str(sts) + """px; 
            text-align: center;    
            background-color: rgba(25, 25, 25, 115);
            border: 0px;
            padding-top: 0px;
            padding-left: 0px;
            padding-right: 0px;
            padding-bottom: 0px;
            margin-top: 0px;
            margin-left: 0px;
            margin-right: 0px;
            margin-bottom: 0px;
            color: white;
            }
            """)
        self.ssbtn2=str("""
            QPushButton {
            font-size: """ + str(sts) + """px; 
            text-align: left;      
            border-radius: 10px;
            border-top-left-radius: 10px;
            background-color: rgba(25, 25, 25, 115);
            border: 2px solid rgba(125, 125, 125, 115);
            padding-top: 2px;
            padding-left: 5px;
            padding-right: 5px;
            padding-bottom: 2px;
            color: white;
            }
            QWidget {
            font-size: """ + str(sts) + """px; 
            text-align: left;      
            border-radius: 10px;
            border-top-left-radius: 0px;
            background-color: rgba(25, 25, 25, 175);
            border: 2px solid rgba(125, 125, 125, 175);
            padding-top: 2px;
            padding-left: 5px;
            padding-right: 5px;
            padding-bottom: 2px;
            color: white;
            }
            """)
        
        self.ssclick=str("""
            QPushButton {
            font-size: """ + str(sts) + """px; 
            text-align: center;      
            border-radius: 10px;
            background-color: rgba(190, 125, 125, 185);
            border: 2px solid rgba(125, 125, 125, 185);
            padding-top: 2px;
            padding-left: 5px;
            padding-right: 5px;
            padding-bottom: 2px;
            color: white;
            }
            QPushButton:hover {
            font-size: """ + str(sts) + """px; 
            text-align: center;      
            border-radius: 10px;
            background-color: rgba(250, 125, 125, 185);
            border: 2px solid rgba(125, 125, 125, 185);
            padding-top: 2px;
            padding-left: 5px;
            padding-right: 5px;
            padding-bottom: 2px;
            color: white;
            }
            """)
        
        self.ssclick1=str("""
            QPushButton {
            font-size: """ + str(sts) + """px; 
            text-align: center;      
            border-radius: 10px;
            background-color: rgba(125, 170, 125, 185);
            border: 2px solid rgba(125, 125, 125, 185);
            padding-top: 2px;
            padding-left: 5px;
            padding-right: 5px;
            padding-bottom: 2px;
            color: white;
            }
            QPushButton:hover {
            font-size: """ + str(sts) + """px; 
            text-align: center;      
            border-radius: 10px;
            background-color: rgba(125, 250, 125, 185);
            border: 2px solid rgba(125, 125, 125, 185);
            padding-top: 2px;
            padding-left: 5px;
            padding-right: 5px;
            padding-bottom: 2px;
            color: white;
            }
            """)
        
        
        
        
        self.process=None
        layout = QHBoxLayout()
        main_widget=QWidget()
        layout_main = QVBoxLayout()
        layout_main.addWidget(main_widget)
        main_widget.setLayout(layout)
        main_widget.setStyleSheet(self.sswidget)
        main_widget.setFixedHeight(int(50*self.faktor))
        
        layout_set = QVBoxLayout()
        
        
        self.btn_settings = QPushButton()
        self.btn_settings.setIcon(QIcon('./menu.png'))
        self.btn_settings.setStyleSheet(self.ssnormal1)
        self.btn_settings.setFixedSize(int(18*self.faktor),int(18*self.faktor))
        self.btn_settings.clicked.connect(self.btn)
        self.btn_exit = QPushButton("X")
        self.btn_exit.setStyleSheet(self.ssnormal1)
        self.btn_exit.setFixedSize(int(18*self.faktor),int(18*self.faktor))
        self.btn_exit.clicked.connect(sys.exit)
        
        
        
        layout_set.addWidget(self.btn_exit)
        layout_set.addWidget(self.btn_settings)
        layout_set.addStretch(1)
        
        
        
        self.volume_slider = QSlider(Qt.Vertical, self)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(150)
        self.volume_slider.setValue(80)
        self.volume_slider.setStyleSheet(self.ssnormal)
        self.volume_slider.valueChanged.connect(self.change_volume)
        self.volume_slider.setFixedSize(int(12*self.faktor),int(36*self.faktor))
        
        
        self.btn_play_stop = QPushButton()
        self.btn_play_stop.setIcon(QIcon('./play.png'))
        self.btn_play_stop.setStyleSheet(self.ssnormal1)
        
        self.btn_play_stop.setFixedSize(int(24*self.faktor),int(36*self.faktor))
        self.btn_play_stop.setIconSize(QSize(int(24*self.faktor),int(24*self.faktor)))
        self.btn_play_stop.clicked.connect(self.play_stop)
        
        
        self.song_label = QPushButton()
        self.song_label.setStyleSheet(self.ssnormal)
        
        layout.addLayout(layout_set)
        layout.addWidget(self.volume_slider)
        layout.addWidget(self.btn_play_stop)
        layout.addWidget(self.song_label)
        layout.addStretch(1)
        self.setLayout(layout_main)
        #self.setStyleSheet(self.sswidget)
        

        # ---- Einlesen der Senderliste starten
        self.loadStreamList()

        # ---- Stream starten
        #self.play_radio(self.stream_url)
        


        # ---- Hauptfenster einstellung 
        self.setWindowTitle("X-Live Radioplayer")
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon.fromTheme('audio-radio'))
        breite = self.song_label.width()
        hoehe = self.song_label.height()
        self.move(0,0)


        # ---- Song anzeige auffrischen im interval
        self.refresh_song_info()
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_song_info)
        self.refresh_timer.start(5000)  # Refresh metadata every 5 seconds
        

    def get_metadata(self, stream_url):
        process = QProcess()
        process.readyReadStandardOutput.connect(lambda: self.process_metadata_output(process.readAllStandardOutput()))
        process.start('ffprobe', ['-v', 'quiet', '-print_format', 'json', '-show_format', stream_url])
        process.waitForFinished()
        self.check_ffplay
        
            
        
 
    def process_metadata_output(self, output):
        metadata_str = output.data().decode('utf-8').strip()
        if metadata_str:
            #print(metadata_str)
            metadata_lines = metadata_str.split('\n')
            for line in metadata_lines:
                line = line.strip().replace('"',"")
                if line.startswith('icy-name'):
                    radio_info = line.split(":")[1].strip()
                    self.radio = radio_info[:-1]
                    
                if line.startswith('StreamTitle'):
                    song_info = line.split(":")[1].strip()
                    if song_info != ",":
                        if song_info.endswith(','):
                            song_info = song_info[:-1]
                        self.old_song = self.song
                        self.song = song_info
               
            #self.song_label.setText(song_info) 
            if self.song != self.old_song:
                self.song_label.setText(" Radio: " + str(self.radio) + " \n Titel: " + str(self.song) + " ")   
            self.adjustSize()
  
            

    def refresh_song_info(self):
        self.get_metadata(self.stream_url)
    
    def play_radio(self, stream_url):
        os.system('killall ffplay 2>/dev/null')
        time.sleep(1)
        self.process = subprocess.Popen(['ffplay', '-nodisp', '-loglevel','quiet', '-volume', str(self.volume_slider.value()), stream_url])
        self.btn_play_stop.setIcon(QIcon('./stop.png'))
        time.sleep(2)
        self.stream_id = self.get_stream_id()
        
    def check_ffplay(self):        
        if not self.process:
            sys.exit()
        

    def change_volume(self):
        if self.process:
            cmd = ['pactl', 'set-sink-input-volume', str(self.stream_id), str(self.volume_slider.value())+"%"]
            subprocess.Popen(cmd)

    def get_stream_id(self):
        # Befehl ausführen, um die Stream-ID zu erhalten
        command = "pactl list sink-inputs short | awk '{print $1}' | tail -n 1"
        output = subprocess.check_output(command, shell=True, text=True)
        # Extrahieren der ersten Zeile und Konvertieren in eine Ganzzahl
        stream_id=0
        #print(output)
        if output:        
            stream_id = int(output.split('\t')[0])
        print(stream_id)
        
        return stream_id
        
    def play_stop(self):
        if not self.process:
            self.play_radio(self.stream_url)
            
        else:
            self.process = None
            os.system('killall ffplay 2>/dev/null')
            self.btn_play_stop.setIcon(QIcon('./play.png'))
        
# --- Hier fängt bereich streamwahl an
        
    def btn(self):
        if self.new_widget != None:
            self.new_widget = None
        else:
            self.stream_wahl()
        
        
    def stream_wahl(self):
        self.new_widget = None
        self.new_widget = QWidget()
        self.new_widget1 = QWidget()

        # ---- Kopfzeile ----
        self.new_layout = QHBoxLayout()
        self.new_label_title = QLabel("Streamauswahl")
        self.new_label_title.setStyleSheet(self.ssnormal)
        self.new_btn_close = QPushButton("X")
        self.new_btn_close.setStyleSheet(self.ssnormal)
        self.new_btn_close.clicked.connect(self.btn_close)
        self.new_layout.addWidget(self.new_label_title)
        self.new_layout.addStretch(1)
        self.new_layout.addWidget(self.new_btn_close)
        
        
        # ---- Bauchzeile 
        self.new_layoutH=QHBoxLayout()
        self.stream_list = QListWidget()
        self.stream_list.itemClicked.connect(self.onItemClicked)
        self.stream_list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff) 
        self.stream_list.setFixedSize(int(220*self.faktor),int(220*self.faktor))
        
        for stream in self.radio_name:
            self.stream_list.addItem(stream.strip())
        
        self.new_layoutH.addWidget(self.stream_list)
        #self.new_layoutH.addStretch(1)
        
        # --- Bauchzeile rechts
        self.new_layoutHV = QVBoxLayout()
        self.selected_stream_label = QLabel() 
        #self.selected_stream_label.setFixedWidth(int(300*self.faktor))
        self.new_layoutHV.addWidget(self.selected_stream_label)
        self.selected_stream_label.setStyleSheet(self.ssnormal)
        self.new_layoutHV.addStretch(2)
        self.selected_stream_start = QPushButton("zu Sender wechseln")
        self.selected_stream_start.setStyleSheet(self.ssclick1)
        self.selected_stream_start.clicked.connect(self.btn_change_stream)
        #self.new_layoutHV.addWidget(self.selected_stream_start)
        
        
        self.new_layoutH.addLayout(self.new_layoutHV)
        # ---- Fusszeile
        self.new_btn_end = QPushButton("Radio Ausschalten")
        self.new_btn_end.setStyleSheet(self.ssclick)
        self.new_btn_end.clicked.connect(self.btn_end)
        
        
        self.new_layoutV=QVBoxLayout()
        self.new_layoutV.addLayout(self.new_layout)
        self.new_layoutV.addLayout(self.new_layoutH)
        self.new_layoutV.addWidget(self.selected_stream_start)
        self.new_layoutV.addStretch(5)
        
        
        self.new_layout1=QVBoxLayout()
        self.new_layout1.addWidget(self.new_widget1)
        self.new_widget.setLayout(self.new_layout1)
        self.new_widget1.setLayout(self.new_layoutV)
        self.new_widget1.setStyleSheet(self.ssbtn2)
        self.new_widget.move(int(100*self.faktor),int(60*self.faktor))
        self.new_widget.setFixedWidth(int(600*self.faktor))
        self.new_widget.setWindowTitle("X-Live Radio Streamwahl")
        self.new_widget.setAttribute(Qt.WA_TranslucentBackground)
        self.new_widget.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.new_widget.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.new_widget.show()
        if self.stream_list.count() > 0:
            self.stream_list.setCurrentRow(0)
            first_item = self.stream_list.item(0)
            self.onItemClicked(first_item)
        
    def btn_close(self):
        self.new_widget = None
        
    def btn_end(self):
        self.new_widget = None
        sys.exit()
        
    def btn_change_stream(self):
        self.new_widget = None
        self.stream_url = self.radio_url[self.stream_number]
        self.play_radio(self.stream_url)
        self.refresh_song_info()
        
    def onItemClicked(self, item):
        self.selected_stream_label.setText("") 
        self.stream_number = self.stream_list.row(item)
        self.get_metadata_sw(self.radio_url[self.stream_number])
        self.selected_stream_label.setText( "(" + str(self.stream_number+1) + ") " + item.text() +
                                            "\n\nAktueller Titel: \n" + self.song_info +
                                            "\n\nGenre:\n"+self.icy_genre +
                                            "\n\nHomepage:\n"+self.icy_url 
                                            ) 
        self.song_info = ""
        self.icy_url = ""
        self.icy_genre = ""
        
    def loadStreamList(self):
        try:
            with open('radio.streamlist', 'r') as file:
                streams = file.readlines()
                for stream in streams:
                    self.radio = ""
                    stream = stream.replace("\n","")
                    self.radio_name.append(stream.split(",")[0])
                    self.radio_url.append(stream.split(",")[1])
            self.stream_url = self.radio_url[0]
        except FileNotFoundError:
            print("Datei 'radio.streamlist' nicht gefunden.")
            sys.exit()
        
    def get_metadata_sw(self, stream_url):
        process_sw = QProcess()
        process_sw.readyReadStandardOutput.connect(lambda: self.process_metadata_output_sw(process_sw.readAllStandardOutput()))
        process_sw.start('ffprobe', ['-v', 'quiet', '-print_format', 'json', '-show_format', stream_url])
        process_sw.waitForFinished()
        

    def process_metadata_output_sw(self, output):
        metadata_str = output.data().decode('utf-8').strip()       

        if metadata_str:
            metadata_lines = metadata_str.split('\n')
            for line in metadata_lines:
                line = line.strip().replace('"',"")
                    
                if line.startswith('StreamTitle'):
                    song_info = line.split(":")[1].strip()
                    if song_info.endswith(','):
                        song_info = song_info[:-1]
                    self.song_info = song_info
        
                if line.startswith('icy-url'):
                    song_info = str(line[line.find(":")+1:-1]).strip()
                    self.icy_url = song_info
                
                if line.startswith('icy-genre'):
                    song_info = str(line.split(":")[1].strip())[:-1]
                    self.icy_genre = song_info
        

def kill_ffplay():
    subprocess.run(['killall', 'ffplay'])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = RadioWidget()
    widget.show()    
    atexit.register(kill_ffplay)
    sys.exit(app.exec_())
