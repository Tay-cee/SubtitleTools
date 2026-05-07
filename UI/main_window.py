from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QFileDialog,
    QSlider, QLabel, QFrame
)
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import Qt, QUrl


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Editor Style Video Player")
        self.resize(1400, 800)

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        root_layout = QVBoxLayout()
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        central_widget.setLayout(root_layout)


        #
        # MAIN CONTENT
        #
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        #
        # LEFT PANEL
        #
        left_panel = QFrame()
        left_panel.setFixedWidth(220)

        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(10, 10, 10, 10)

        left_panel.setLayout(left_layout)

        left_layout.addWidget(QLabel("Left Panel"))
        left_layout.addWidget(QLabel("Mabye do list of subtitles with timestamps here?"))
        left_layout.addStretch()

        #
        # VIDEO AREA
        #
        center_widget = QWidget()

        center_layout = QVBoxLayout()
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(0)

        center_widget.setLayout(center_layout)

        self.video_widget = QVideoWidget()

        center_layout.addWidget(self.video_widget)

        #
        # PLAYER CONTROLS
        #
        controls_widget = QFrame()
        controls_widget.setFixedHeight(80)

        controls_layout = QHBoxLayout()
        controls_layout.setContentsMargins(10, 10, 10, 10)
        controls_layout.setSpacing(10)

        controls_widget.setLayout(controls_layout)

        self.back_button = QPushButton("⏮")
        self.back_button.clicked.connect(self.skip_back)

        self.play_button = QPushButton("▶")
        self.play_button.clicked.connect(self.toggle_play)

        self.forward_button = QPushButton("⏭")
        self.forward_button.clicked.connect(self.skip_forward)

        self.open_button = QPushButton("Open")
        self.open_button.clicked.connect(self.open_video)

        self.position_slider = QSlider(Qt.Horizontal)
        self.position_slider.sliderMoved.connect(self.set_position)

        self.time_label = QLabel("00:00 / 00:00")

        controls_layout.addWidget(self.back_button)
        controls_layout.addWidget(self.play_button)
        controls_layout.addWidget(self.forward_button)
        controls_layout.addWidget(self.open_button)
        controls_layout.addWidget(self.position_slider)
        controls_layout.addWidget(self.time_label)

        center_layout.addWidget(controls_widget)

        #
        # RIGHT PANEL
        #
        right_panel = QFrame()
        right_panel.setFixedWidth(180)

        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(10, 10, 10, 10)

        right_panel.setLayout(right_layout)

        right_layout.addWidget(QLabel("Right Panel"))
        right_layout.addWidget(QLabel("Defo put like a selector menu for adding, editing css etc"))
        right_layout.addStretch()


        content_layout.addWidget(left_panel)
        content_layout.addWidget(center_widget)
        content_layout.addWidget(right_panel)

        root_layout.addLayout(content_layout)

        #
        # MEDIA PLAYER
        #
        self.player = QMediaPlayer()

        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)

        self.player.setVideoOutput(self.video_widget)

        #
        # SIGNALS
        #
        self.player.positionChanged.connect(self.position_changed)
        self.player.durationChanged.connect(self.duration_changed)

    def open_video(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open Video",
            "",
            "Video Files (*.mp4 *.avi *.mkv *.mov)"
        )

        if file_name:
            self.player.setSource(QUrl.fromLocalFile(file_name))
            self.player.play()

            self.play_button.setText("⏸")

    def toggle_play(self):
        if self.player.playbackState() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.play_button.setText("▶")
        else:
            self.player.play()
            self.play_button.setText("⏸")

    def skip_forward(self):
        self.player.setPosition(
            self.player.position() + 5000
        )

    def skip_back(self):
        self.player.setPosition(
            max(0, self.player.position() - 5000)
        )

    def position_changed(self, position):
        self.position_slider.setValue(position)
        self.timeline_slider.setValue(position)

        self.update_time_label(
            position,
            self.player.duration()
        )

    def duration_changed(self, duration):
        self.position_slider.setRange(0, duration)
        self.timeline_slider.setRange(0, duration)

    def set_position(self, position):
        self.player.setPosition(position)

    def update_time_label(self, position, duration):
        current_sec = position // 1000
        total_sec = duration // 1000

        current_min = current_sec // 60
        current_remain = current_sec % 60

        total_min = total_sec // 60
        total_remain = total_sec % 60

        self.time_label.setText(
            f"{current_min:02}:{current_remain:02} / "
            f"{total_min:02}:{total_remain:02}"
        )

    #
    # KEYBINDS
    #
    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_Space:
            self.toggle_play()

        elif key == Qt.Key_Right:
            self.skip_forward()

        elif key == Qt.Key_Left:
            self.skip_back()

        elif key == Qt.Key_Up:
            volume = self.audio_output.volume()
            self.audio_output.setVolume(
                min(1.0, volume + 0.1)
            )

        elif key == Qt.Key_Down:
            volume = self.audio_output.volume()
            self.audio_output.setVolume(
                max(0.0, volume - 0.1)
            )