import uuid
from multiprocessing.spawn import set_executable

from qfluentwidgets import SearchLineEdit, RoundMenu, Action, TitleLabel, SubtitleLabel, ImageLabel, \
    SingleDirectionScrollArea, FluentIcon, MessageBoxBase, LineEdit, RadioButton, BodyLabel, InfoBar, InfoBarPosition, \
    IconWidget
from PyQt5.QtWidgets import QSpacerItem, QSizePolicy, QWidget, QVBoxLayout, QPushButton, QGraphicsDropShadowEffect, \
    QFrame, QHBoxLayout, QButtonGroup
from PyQt5.QtGui import QPainter, QPainterPath, QLinearGradient, QBrush, QImage, QIcon, QColor, QDesktopServices
from PyQt5.QtCore import QRectF, Qt, QSize, QUrl, pyqtSignal
from PyQt5.QtGui import QPainter, QPainterPath, QLinearGradient, QBrush, QImage, QIcon, QDesktopServices
from PyQt5.QtWidgets import QSpacerItem, QSizePolicy, QWidget, QVBoxLayout, QPushButton, QHBoxLayout
from qfluentwidgets import SearchLineEdit, TitleLabel, SubtitleLabel, SingleDirectionScrollArea, FluentIcon

class BannerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('Banner-Widget')
        self.setFixedHeight(346)

        self.mainLayout = QVBoxLayout(self)
        self.title = TitleLabel('Online meeting room', self)
        self.starterLabel = SubtitleLabel('Start your first meeting', self)
        self.banner = QImage(':/images/header.png')

        self.createButton = CreateButton(self)

        self.mainLayout.setContentsMargins(20, 0, 20, 0)
        self.mainLayout.setSpacing(10)

        self.title.setAlignment(Qt.AlignCenter)
        self.mainLayout.addWidget(self.title, alignment=Qt.AlignLeft)

        self.mainLayout.addSpacerItem(QSpacerItem(20, 110, QSizePolicy.MinimumExpanding, QSizePolicy.Fixed))

        self.mainLayout.addWidget(self.starterLabel, alignment=Qt.AlignLeft)
        self.mainLayout.addWidget(self.createButton, alignment=Qt.AlignCenter)
        self.mainLayout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.MinimumExpanding, QSizePolicy.Fixed))

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(
            QPainter.Antialiasing | QPainter.SmoothPixmapTransform
        )
        painter.setPen(Qt.NoPen)

        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)
        w, h = self.width(), 241
        path.addRoundedRect(QRectF(0, 0, w, h), 10, 10)
        path.addRect(QRectF(0, h - 50, 50, 50))
        path.addRect(QRectF(w - 50, 0, 50, 50))
        path.addRect(QRectF(w - 50, h - 50, 50, 50))
        path = path.simplified()

        gradient = QLinearGradient(0, 0, 0, self.height())
        # draw background color

        gradient.setColorAt(0, QColor(207, 216, 228, 255))
        gradient.setColorAt(1, QColor(207, 216, 228, 0))
        # painter.fillPath(path, QBrush(gradient))

        qimage = self.banner.scaled(
            QSize(w, h), transformMode=Qt.SmoothTransformation)

        painter.fillPath(path, QBrush(qimage))


class CreateButton(QPushButton):
    CREATE_ICON_PATH = ':/images/create.png'

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('Create-Button')
        self.setFixedSize(74, 74)
        self.setStyleSheet("""
            QPushButton#Create-Button {
                background-color: #ff9c1a;
                color: white;
                border-radius: 25px;
                }
            QPushButton#Create-Button:hover {
                background-color: #f1a644
                }
            QPushButton#Create-Button:pressed {
                background-color: #c7c4bf
                }
        """)
        self.setIcon(QIcon(self.CREATE_ICON_PATH))
        self.setIconSize(QSize(55, 55))
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 100))
        shadow.setOffset(0, 0)
        self.setGraphicsEffect(shadow)


from qfluentwidgets import ImageLabel, AvatarWidget, MessageBox
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import QLabel, QPushButton, QFrame, QGraphicsDropShadowEffect


class ConferenceCard(QFrame):
    LIVING_ICON_PATH = ':/images/living.gif'

    conf_joined = pyqtSignal(int, str) # (id, title)

    def __init__(self, title, creator, id, parent=None):
        '''
        title: str
        avatar: list[IconWidget]
        id: int
        icon: str
        '''
        super().__init__(parent)

        self.id = id

        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(20, 20, 20, 20)
        self.mainLayout.setSpacing(10)

        # self.iconWidget = ImageLabel(DEFAULT_ICON_PATH, self)
        self.titleLabel = QLabel(title, self)
        self.contentLabel = QLabel(f'id:{id}', self)
        self.joinButton = QPushButton(icon=FluentIcon.ADD_TO.icon(color=QColor('#9c89d3')), parent=self)
        self.extraButton = None

        self.setObjectName('conference-card')
        self.setFixedHeight(160)
        self.setFixedWidth(350)

        # set title
        titleFont = QFont()
        titleFont.setBold(True)
        titleFont.setPointSize(16)
        titleFont.setFamilies(['Trebuchet MS', 'Microsoft YaHei'])
        self.titleLabel.setFont(titleFont)
        self.titleLabel.setStyleSheet('color: white;')
        self.titleLabel.setAlignment(Qt.AlignLeft)
        self.titleLabel.setWordWrap(True)

        # set content
        contentFont = QFont()
        contentFont.setPointSize(10)
        contentFont.setFamily('Arial')  # for id text
        self.contentLabel.setFont(contentFont)
        self.contentLabel.setStyleSheet('color: #e6e6e6;')
        self.contentLabel.setAlignment(Qt.AlignLeft)
        self.contentLabel.setWordWrap(True)

        # bottom layout
        self.bottomLayout = QHBoxLayout()

        # avatar area (overlapp style)
        avatars_layout = QHBoxLayout()
        avatars_layout.setContentsMargins(0, 0, 0, 0)
        avatars_layout.maximumSize = QSize(100, 40)
        creatorFont = QFont()
        creatorFont.setPointSize(13)
        creatorFont.setFamily('Arial')
        creatorFont.setBold(True)
        self.creatorLabel = QLabel('Creator', self)
        self.creatorLabel.setStyleSheet('color: white;')
        self.creatorLabel.setAlignment(Qt.AlignCenter)
        self.creatorLabel.setFont(creatorFont)

        self.creatorName = QLabel(creator, self)
        self.creatorName.setStyleSheet('color: white;')
        self.creatorName.setAlignment(Qt.AlignCenter)
        self.creatorName.setFont(creatorFont)
        avatars_layout.setSpacing(10)

        self.livingLabel = ImageLabel(self.LIVING_ICON_PATH, self)

        avatars_layout.addWidget(self.creatorLabel, 0, Qt.AlignCenter)
        avatars_layout.addWidget(self.creatorName, 0, Qt.AlignCenter)
        avatars_layout.addWidget(self.livingLabel, 0, Qt.AlignCenter)

        self.bottomLayout.addLayout(avatars_layout)
        self.bottomLayout.addStretch()

        # button area
        self.buttonLayout = QHBoxLayout()
        self.joinButton.setFixedHeight(35)
        self.joinButton.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #9c89d3;
                border-radius: 10px;
                font-size: 14px;
                font-weight: bold;
                font-family: 'Microsoft YaHei';
                padding-left: 20px;
                padding-right: 20px
            }
            QPushButton:hover {
                background-color: #ecebff;

            }
            QPushButton:pressed {
                background-color: #dcd0ff;
            }
            QIcon {
                padding-right: 10px;
            }
            QIcon:hover {
                color: #9cffd3;
            }
        """)

        self.buttonLayout.addWidget(self.joinButton, 0, Qt.AlignRight)
        self.bottomLayout.addLayout(self.buttonLayout)

        # add widgets to main layout
        self.mainLayout.addWidget(self.titleLabel)
        self.mainLayout.addWidget(self.contentLabel)
        self.mainLayout.addStretch()
        self.mainLayout.addLayout(self.bottomLayout)

        # set style (gradient blue and blue purple background)
        self.setStyleSheet("""
            #conference-card {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #4e9df3, stop:1 #7cd9fb);
                border-radius: 10px;
            }
            #conference-card:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #6eb8f3, stop:1 #9ce6fb);
            }
        """)
        dropShadowEffect = QGraphicsDropShadowEffect()
        dropShadowEffect.setBlurRadius(20)
        dropShadowEffect.setColor(QColor(0, 0, 0, 100))
        dropShadowEffect.setOffset(0, 0)
        self.setGraphicsEffect(dropShadowEffect)

        self.joinButton.setText('Join')

    def top_view(self):
        parent = self.parent()
        while parent:
            parent = parent.parent()
            if parent.objectName() == 'Home-Interface':
                break
        return parent

    def showMessageBox(self):
        w = MessageBox(
            'Join meeting',
            'Do you want to join this meeting?',
            self.top_view()
        )
        w.yesButton.setText('Join')
        w.cancelButton.setText('Cancel')

        if w.exec():
            self.conf_joined.emit(self.id, self.titleLabel.text())

class OwnedConferenceCard(ConferenceCard):
    def __init__(self, title, avatar, id, parent=None):
        super().__init__(title, avatar, id, parent)

        # change background color to orange gradient
        self.setStyleSheet("""
            #conference-card {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #ff9c1a, stop:1 #ff6f1a);
                border-radius: 10px;
            }
            #conference-card:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #ffba6a, stop:1 #ff8f6a);
            }
        """)

        self.extraButton = QPushButton

class ScrollArea(SingleDirectionScrollArea):

    entered = pyqtSignal()

    def __init__(self, parent=None, orient=Qt.Horizontal):
        super().__init__(parent, orient)
        self.setObjectName('conference-scroll-area')

    def enterEvent(self, event):
        self.entered.emit()
        super().enterEvent(event)

class HomeInterface(QFrame):
    ONLINE_ICON_PATH = ':/images/online.png'

    scroll_area_entered = pyqtSignal()
    search_edit_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('Home-Interface')
        self.body = QVBoxLayout(self)
        self.body.setContentsMargins(0, 0, 0, 0)
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(20, 0, 20, 0)
        self.mainLayout.setSpacing(10)

        self.srollWidth = 820

        # create a banner widget
        self.banner = BannerWidget(self)
        self.body.addWidget(self.banner)

        # create a subtitle label "ongoing meetings/正在进行的会议 " in the center
        self.midBox = QHBoxLayout()
        self.onlineIcon = ImageLabel(self.ONLINE_ICON_PATH, self)
        self.onlineIcon.setFixedSize(30, 30)
        self.secondLabel = SubtitleLabel('On-going meetings', self)
        self.secondLabel.setAlignment(Qt.AlignCenter)
        self.midBox.setContentsMargins(10, 0, 10, 0)
        self.midBox.addWidget(self.onlineIcon, alignment=Qt.AlignCenter, stretch=0)
        self.midBox.addWidget(self.secondLabel, alignment=Qt.AlignCenter, stretch=1)

        self.searchedit = SearchLineEdit(self)
        self.searchedit.setPlaceholderText('Search meetings...')
        self.searchedit.setFixedWidth(200)
        self.searchedit.hide()
        self.midBox.addWidget(self.searchedit, alignment=Qt.AlignCenter, stretch=2)
        self.midBox.addSpacerItem(QSpacerItem(650, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)) # hide the search bar

        self.mainLayout.addLayout(self.midBox)
        self.body.addLayout(self.mainLayout)
        # self.mainLayout.addStretch()

        # create a scroll area for conference cards
        view = QWidget(self)
        view.setObjectName('conference-view')
        view.setStyleSheet("""
            #conference-view {
                background: #f9f9f9;
            }
        """)
        self.meetingCardView = view
        self.meetingCardView.setFixedSize(self.srollWidth, 200)
        layout = QHBoxLayout(view)
        self.scrollLayout = layout
        self.scrollArea = ScrollArea()
        self.scrollArea.setFixedHeight(200)
        self.scrollArea.setObjectName('conference-scroll-area')
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(20)

        # connect signals
        self.scrollArea.entered.connect(self.scroll_area_entered)

        self.scrollArea.setWidget(view)
        self.scrollArea.setFrameShape(QFrame.NoFrame)
        self.mainLayout.addWidget(self.scrollArea)

    def addConferenceCard(self, title, id, creator):
        card = ConferenceCard(title, creator, id, self)
        card.joinButton.clicked.connect(card.showMessageBox)
        card_w = card.width()
        print(self.scrollLayout.count())
        if self.srollWidth < (card_w + 10) * (self.scrollLayout.count() + 1):
            self.srollWidth += card_w + 10 # 10 is the spacing
        self.scrollLayout.addWidget(card, 0, Qt.AlignLeft)
        self.meetingCardView.setFixedWidth(self.srollWidth)
        self.meetingCardView.adjustSize()
        return card

    def removeConferenceCard(self, card: ConferenceCard):
        card.deleteLater()
        if self.srollWidth > 800 + card.width() + 10:
            self.srollWidth -= card.width() + 10
        self.meetingCardView.setFixedWidth(self.srollWidth)
        self.meetingCardView.adjustSize()

    def info(self, info_level, title, msg, pos=InfoBarPosition.TOP, orient=Qt.Orientation.Horizontal):
        """
        generate toast-like infobar
        """
        if info_level == 'success':
            InfoBar.success(
                title=title,
                content=msg,
                orient=orient,
                isClosable=True,
                duration=3000,
                position=pos,
                parent=self
            )
        elif info_level == 'warning':
            InfoBar.warning(
                title=title,
                content=msg,
                orient=orient,
                isClosable=True,
                duration=3000,
                position=pos,
                parent=self
            )
        elif info_level == 'error':
            InfoBar.error(
                title=title,
                content=msg,
                orient=orient,
                isClosable=True,
                duration=3000,
                position=pos,
                parent=self
            )
        elif info_level == 'info':
            InfoBar.info(
                title=title,
                content=msg,
                orient=orient,
                isClosable=True,
                duration=3000,
                position=pos,
                parent=self
            )
        else:
            raise ValueError('Invalid info_level')

    def closeEvent(self, a0):
        pass

class MeetingConfigMessageBox(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel('Meeting configuration', self)

        self.hintLabel = BodyLabel('Please input the meeting name', self)

        self.lineEdit = LineEdit(self)
        self.lineEdit.setPlaceholderText('Meeting name')
        self.warningBadge = IconWidget(FluentIcon.INFO.colored(QColor('#ff9c1a'), QColor('#ff9c1a')), self)
        self.warningBadge.setFixedSize(16, 16)
        self.warningLabel = BodyLabel('Meeting name cannot be empty', self)
        self.warningLayout = QHBoxLayout()
        self.warningLayout.addWidget(self.warningBadge)
        self.warningLayout.addWidget(self.warningLabel)
        self.warningLayout.setSpacing(5)
        self.warningLayout.setContentsMargins(0, 0, 0, 0)
        self.warningLayout.addStretch()

        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.hintLabel)
        self.viewLayout.addWidget(self.lineEdit)
        self.viewLayout.addLayout(self.warningLayout)

        self.warningBadge.hide()
        self.warningLabel.hide()

        self.widget.setMinimumWidth(350)

    def meetingName(self):
        return self.lineEdit.text()


    def validate(self) -> bool:
        valid = self.lineEdit.text() != ''

        if not valid:
            self.warningLabel.show()
            self.warningBadge.show()
        else:
            self.warningLabel.hide()
            self.warningBadge.hide()

        return valid