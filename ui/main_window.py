# ui/main_window.py
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QListWidget, QListWidgetItem, QPushButton, QWidget, QFileDialog, QAction, QMessageBox, QShortcut, QHBoxLayout, QMenuBar
from PyQt5.QtCore import QTimer, Qt, QMetaObject, QUrl, pyqtSignal
from PyQt5.QtGui import QIcon, QPalette, QColor, QKeySequence
from PyQt5.QtMultimedia import QSoundEffect
import os
import threading
import keyboard
from utils.config import load_config
from utils.timer import Timer
from utils.notes import note_time, read_notes, update_note_description
from ui.settings_dialog import SettingsDialog

class MainWindow(QMainWindow):
    toggleTimerSignal = pyqtSignal()
    createNoteSignal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.timer = Timer()
        self.currentSessionStart = None
        self.config = load_config()
        self.initUI()
        self.setupHotkeys()
        self.setupSignals()

    def setupSignals(self):
        self.toggleTimerSignal.connect(self.toggleTimer)
        self.createNoteSignal.connect(self.createNoteAndUpdateList)

    def initUI(self):
        # Set window size and minimum size
        self.setWindowTitle('ClipNotes')
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(600, 400)
        
        # Set window icon
        self.setWindowIcon(QIcon('ui/clipnotes.ico'))        

        # Set dark theme colors
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)
        self.setPalette(dark_palette)

        # Create central widget and layout
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        mainLayout = QVBoxLayout()
        centralWidget.setLayout(mainLayout)

        # Initialize UI elements
        self.projectTitleInput = QLineEdit()
        self.timerDisplay = QLabel('Timer: 00:00:00')
        self.notesList = QListWidget()
        self.updateNoteButton = QPushButton('Update Selected Note')
        self.deleteNoteButton = QPushButton('Delete Selected Note')
        self.descriptionInput = QTextEdit()
        self.settingsButton = QPushButton('Settings')
        self.initSounds()

        # Set dark theme colors for the window
        self.applyDarkTheme()
        
        # Adjusting the timer display's font size
        self.timerDisplay.setStyleSheet('''
            QLabel {
                color: #FFFFFF; /* White text for contrast */
                font-size: 30px; /* Increased font size for better visibility */
                font-weight: bold; /* Optional: makes the font bolder */
            }
        ''')
        
        # Game title input bar adjustments
        self.projectTitleInput.setStyleSheet('''
            QLineEdit {
                background-color: #333333; /* Dark background for visibility */
                color: #FFFFFF; /* White text for contrast */
                border: 1px solid #555555; /* Subtle border */
                border-radius: 4px; /* Rounded corners for modern look */
                padding: 5px; /* Padding for text inside */
                font-size: 14px; /* Adequate font size */
            }
        ''')
        self.projectTitleInput.setPlaceholderText('Enter Game Title Here')  # Placeholder text
        
        # Description input box adjustments
        self.descriptionInput.setStyleSheet('''
            QTextEdit {
                background-color: #333333; /* Dark background for visibility */
                color: #FFFFFF; /* White text for contrast */
                border: 1px solid #555555; /* Subtle border */
                border-radius: 4px; /* Rounded corners for modern look */
                padding: 5px; /* Padding for text inside */
                font-size: 14px; /* Adequate font size */
            }
        ''')
        self.descriptionInput.setPlaceholderText('Enter description for the selected timestamp here...')  # Placeholder text

        # Menu bar styling adjusted for readability
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('File')
        menuBar.setStyleSheet('''
            QMenuBar {
                background-color: #2E2E2E; /* Dark grey background */
                color: #FFFFFF; /* White text */
            }
            QMenuBar::item:selected {
                background-color: #555555; /* Slightly lighter grey for selection */
            }
        ''')
        
        # Existing import action
        importAction = QAction('Import', self)
        importAction.triggered.connect(self.importFile)
        fileMenu.addAction(importAction)
        
        # Add the Help action
        helpAction = QAction('Help', self)
        helpAction.triggered.connect(self.showHelpDialog)
        fileMenu.addAction(helpAction)

        # Layout setup
        self.setupLayouts(mainLayout)

        self.show()

    def initSounds(self):
        self.startStopSound = QSoundEffect()
        self.startStopSound.setSource(QUrl.fromLocalFile("sounds/stop.wav"))  # Adjust path as needed
        self.startStopSound.setVolume(0.15)
        
        self.noteSound = QSoundEffect()
        self.noteSound.setSource(QUrl.fromLocalFile("sounds/new.wav"))  # Adjust path as needed
        self.noteSound.setVolume(0.15)

    def setupLayouts(self, mainLayout):
        # Create top layout for project title and timer display
        topLayout = QHBoxLayout()
        topLayout.addWidget(self.projectTitleInput)
        topLayout.addWidget(self.timerDisplay)

        # Middle layout for notes list and description input
        middleLayout = QVBoxLayout()
        middleLayout.addWidget(self.notesList)

        # Layout for update and delete buttons
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.updateNoteButton)
        buttonLayout.addWidget(self.deleteNoteButton)
        middleLayout.addLayout(buttonLayout)
        middleLayout.addWidget(self.descriptionInput)

        # Layout for hotkey tooltip and settings button
        infoLayout = QHBoxLayout()
        self.hotkeysInfo = QLabel(f"Start/Stop Hotkey: {self.config['start_stop_hotkey']} | Note Hotkey: {self.config['note_hotkey']}")
        infoLayout.addWidget(self.hotkeysInfo)
        infoLayout.addStretch()
        infoLayout.addWidget(self.settingsButton)

        # Add sub-layouts to main layout
        mainLayout.addLayout(topLayout)
        mainLayout.addLayout(middleLayout)
        mainLayout.addLayout(infoLayout)

        # Connect button click events
        self.updateNoteButton.clicked.connect(self.updateSelectedNote)
        self.deleteNoteButton.clicked.connect(self.deleteSelectedNote)
        self.settingsButton.clicked.connect(self.openSettingsDialog)

        # Timer update
        self.timerUpdate = QTimer(self)
        self.timerUpdate.timeout.connect(self.updateTimer)
        self.timerUpdate.start(1000)
        
    def applyDarkTheme(self):
        # Apply dark theme palette to the application
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(45, 45, 45)) # Darker button background
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)
        self.setPalette(dark_palette)

        # Apply styles to buttons for improved readability and hover effect
        buttonStyle = '''
            QPushButton {
                background-color: #3C3C3C; /* Dark grey background */
                color: #D3D3D3; /* Light grey text */
                border: 1px solid #555; /* Slightly darker border for depth */
                border-radius: 4px; /* Rounded corners */
                padding: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #505050; /* Slightly lighter on hover */
            }
            QPushButton:pressed {
                background-color: #424242; /* Darker when pressed */
            }
        '''
        self.updateNoteButton.setStyleSheet(buttonStyle)
        self.deleteNoteButton.setStyleSheet(buttonStyle)
        self.settingsButton.setStyleSheet(buttonStyle)

    def importFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, 'Import File', '', 'Text Files (*.txt)')
        if fileName:
            try:
                self.notesList.clear()
                with open(fileName, 'r') as file:
                    content = file.readlines()
                    for line in content:
                        parts = line.strip().split(' - ', maxsplit=2)
                        if len(parts) >= 2:
                            uid = parts[0].split(': ')[1]
                            time_mark = parts[1].split(': ')[1]
                            description = parts[2] if len(parts) == 3 else "(No description)"
                            display_text = f"{time_mark} - {description}"
                            item = QListWidgetItem(display_text)
                            item.setData(Qt.UserRole, fileName)
                            item.setData(Qt.UserRole + 1, uid)
                            self.notesList.addItem(item)
            except IOError:
                print(f"Error: Could not read file '{fileName}'")

    def setupHotkeys(self):
        threading.Thread(target=lambda: keyboard.add_hotkey(self.config['start_stop_hotkey'], self.toggleTimerSignal.emit), daemon=True).start()
        threading.Thread(target=lambda: keyboard.add_hotkey(self.config['note_hotkey'], self.createNoteSignal.emit), daemon=True).start()
        
    def updateHotkeyText(self):
        self.hotkeysInfo.setText(f"Start/Stop Hotkey: {self.config['start_stop_hotkey']} | Note Hotkey: {self.config['note_hotkey']}")        

    def toggleTimer(self):
        if not self.timer.start_time:
            self.timer.start_stop()
            self.currentSessionStart = self.timer.start_time.strftime('%Y-%m-%d_%H-%M-%S')
            self.notesList.clear()
            if self.config['sound_effects']:
                self.startStopSound.play()
        else:
            self.timer.start_stop()
            self.timerDisplay.setText('Timer: 00:00:00')
            self.currentSessionStart = None
            if self.config['sound_effects']:
                self.startStopSound.play()

    def createNoteAndUpdateList(self):
        QTimer.singleShot(0, self.createNoteAndUpdateListHelper)

    def createNoteAndUpdateListHelper(self):
        description = self.descriptionInput.toPlainText()
        title = self.projectTitleInput.text()

        if not title:
            title = 'Untitled'

        note_time(self.timer.start_time, self.config['notes_dir'], title, description)
        if self.config['sound_effects']:
            self.noteSound.play()
        self.updateNotesList()
        if self.config['clear_description']:
            self.descriptionInput.clear()
            
    def updateNotesList(self):
        self.notesList.clear()
        notes = read_notes(self.config['notes_dir'])
        for filepath, note in notes:
            if self.currentSessionStart and self.currentSessionStart in filepath:
                parts = note.split(' - ', maxsplit=2)
                if len(parts) >= 2:
                    uid = parts[0].split(": ")[1]
                    time_mark = parts[1].split(": ")[1]
                    description = parts[2] if len(parts) == 3 else "(No description)"
                    display_text = f"{time_mark} - {description}"
                    item = QListWidgetItem(display_text)
                    item.setData(Qt.UserRole, filepath)
                    item.setData(Qt.UserRole + 1, uid)
                    self.notesList.addItem(item)

    def updateSelectedNote(self):
        selectedItems = self.notesList.selectedItems()
        if selectedItems:
            new_description = self.descriptionInput.toPlainText()
            for item in selectedItems:
                filepath = item.data(Qt.UserRole)
                uid = item.data(Qt.UserRole + 1)
                if filepath and uid:
                    update_note_description(filepath, uid, new_description)
                    time_mark = item.text().split(' - ')[0]
                    display_text = f"{time_mark} - {new_description}"
                    item.setText(display_text)
                    if self.config['clear_description']:
                        self.descriptionInput.clear()
                else:
                    print("Could not retrieve the necessary data for the selected note.")
        else:
            print("No note selected.")

    def deleteSelectedNote(self):
        selectedItems = self.notesList.selectedItems()
        if selectedItems:
            confirm = QMessageBox.question(self, 'Confirm Delete', 'Are you sure you want to delete the selected note(s)?',
                                           QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                for item in selectedItems:
                    filepath = item.data(Qt.UserRole)
                    if filepath:
                        try:
                            os.remove(filepath)
                            self.notesList.takeItem(self.notesList.row(item))
                        except OSError as e:
                            print(f"Error deleting file '{filepath}': {e}")
                    else:
                        print("Could not retrieve the file path for the selected note.")
        else:
            print("No note selected.")

    def updateTimer(self):
        if self.timer.start_time:
            elapsed_time = self.timer.get_elapsed_time()
            self.timerDisplay.setText(f"Timer: {str(elapsed_time).split('.')[0]}")

    def openSettingsDialog(self):
        dialog = SettingsDialog(self)
        if dialog.exec_():
            self.config = load_config()
            self.setupHotkeys()
            self.updateHotkeyText()

    def showHelpDialog(self):
        helpText = """
        <h2>Welcome to ClipNotes - Your Ultimate Companion for Game Recording Sessions!</h2>
        <p>ClipNotes is designed to make your gameplay recording sessions more productive and engaging. Whether you're a content creator, a streamer, or a gameplay analyst, ClipNotes provides you with the tools to easily capture and annotate important moments without ever having to leave your game.</p>
        <h3>Getting Started:</h3>
        <p><b>Configuration:</b><br>
        - Before diving into your game, open ClipNotes and configure your settings. Go to the <b>Settings</b> dialog where you can:<br>
        &nbsp;&nbsp;• Set your hotkeys for starting/stopping the recording timer and capturing notes.<br>
        &nbsp;&nbsp;• Choose the directory where your note files will be saved.<br>
        &nbsp;&nbsp;• Decide if you want the note input field to clear after capturing a note.</p>
        <p><b>Recording Session:</b><br>
        - Enter the title of your game in the <b>Enter Game Title Here</b> field at the top.<br>
        - Use your configured hotkey to start the timer simultaneously with your gameplay recording.<br>
        - Whenever something note-worthy happens, hit the note hotkey, type in your note, and it's automatically saved with a timestamp. The note will appear in the main window, where you can review, edit, or delete it as needed.</p>
        <p><b>Reviewing Notes:</b><br>
        - All notes are saved in a file named after your game title and session start time. This file can be found in the directory you specified in the settings.<br>
        - To review notes from a past session, use the <b>Import</b> feature in the <b>File</b> menu to load the note file into ClipNotes.</p>
        <h3>Features at a Glance:</h3>
        <p>- <b>Synchronized Note-Taking:</b> Capture your thoughts in real-time with gameplay.<br>
        - <b>Customizable Hotkeys:</b> Set hotkeys that don't interfere with your game controls.<br>
        - <b>Automatic Note Saving:</b> Every note is timestamped and saved automatically.<br>
        - <b>Note Management:</b> Review, edit, and delete notes directly within the application.<br>
        - <b>Import Functionality:</b> Easily load past notes for review or further analysis.</p>
        <h3>Support and Feedback:</h3>
        <p>Your feedback is invaluable to us! If you encounter any issues or have suggestions for how we can improve ClipNotes, please don't hesitate to reach out to us via our support channel.</p>
        <p>Thank you for choosing ClipNotes. Happy recording!</p>
        """
        QMessageBox.information(self, "Help - How to Use ClipNotes", helpText)