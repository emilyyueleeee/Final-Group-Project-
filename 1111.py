import sys
import os
import random
from PyQt5 import QtWidgets, QtGui, QtCore
from pathlib import Path
import logging
base_folder = Path(__file__).parent

class DeskPet(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.childPets = []
        self.isDragging = False
        self.isMoving = False
        self.change = False

    def initUI(self):
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setGeometry(500, 500, 130, 130)
        self.currentAction = self.startIdle
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.updateAnimation)
        self.changeDirectionTimer = QtCore.QTimer(self)  # Add Timer
        self.changeDirectionTimer.timeout.connect(self.changeDirection)  # The changeDirection method is called when the timer is triggered.
        self.startIdle()
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showMenu)
        self.setMouseTracking(True)
        self.dragging = False

    def loadImages(self, path):
        return [QtGui.QPixmap(os.path.join(path, f)) for f in os.listdir(path) if f.endswith('.png')]

    def startIdle(self):
        self.setFixedSize(130, 130)
        self.currentAction = self.startIdle
        self.images = self.loadImages(base_folder / "crayon/Deskpet/resource/xianzhi")
        self.currentImage = 0
        self.timer.start(100)
        self.moveSpeed = 0
        self.movingDirection = 0
        if self.changeDirectionTimer.isActive():
            self.changeDirectionTimer.stop()  # Stop direction change timer

    def startWalk(self):
        self.setFixedSize(130, 130)
        if not self.isDragging:
            self.currentAction = self.startWalk
            direction = random.choice(["zuo", "you"])
            self.images = self.loadImages(base_folder / f"crayon/Deskpet/resource/sanbu/{direction}")
            self.currentImage = 0
            self.movingDirection = -1 if direction == "zuo" else 1
            self.moveSpeed = 10
            self.timer.start(100)
            self.changeDirectionTimer.start(3000)  # Start Timer

    def movePet(self):
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        new_x = self.x() + self.movingDirection * self.moveSpeed
        if new_x < 10:
            new_x = 10
            if self.currentAction == self.startWalk:
                self.movingDirection *= -1
                # Stop loading the original image
                self.timer.stop()
                self.images = []  # Empty the current picture list
                if self.movingDirection == -1:  # Left
                    self.images = self.loadImages(base_folder / "crayon/Deskpet/resource/sanbu/zuo")
                else:  # Right
                    self.images = self.loadImages(base_folder / "crayon/Deskpet/resource/sanbu/you")

                self.currentImage = 0
                self.timer.start(100)
        elif new_x > screen.width() - self.width() - 10:
            new_x = screen.width() - self.width() - 10
            if self.currentAction == self.startWalk:
                self.movingDirection *= -1
                # Stop loading the original image
                self.timer.stop()
                self.images = []  # Empty the current picture list
                # Load the corresponding image according to the direction of movement
                if self.movingDirection == -1:  # Left
                    self.images = self.loadImages(base_folder / "crayon/Deskpet/resource/sanbu/zuo")
                else:  # Right
                    self.images = self.loadImages(base_folder / "crayon/Deskpet/resource/sanbu/you")

                self.currentImage = 0
                self.timer.start(100)
        self.deskpet_rect = self.geometry()
        for child in self.childPets:
            if isinstance(child, XiaobaiWindow):
                self.xiaobai_rect = child.geometry()
                if self.deskpet_rect.intersects(self.xiaobai_rect):
                    child.close()
                    self.startMeet()
        self.move(new_x, self.y())

    def startMeet(self):
        self.setFixedSize(150, 150)
        self.currentAction = self.startMeet
        
        self.currentImage = 0
        self.moveSpeed = 0
        self.movingDirection = 0
        self.timer.start(30)

    def startLift(self):
        self.setFixedSize(160, 160)
        self.currentAction = self.startLift
       
        self.currentImage = 0
        self.moveSpeed = 0
        self.movingDirection = 0
        self.timer.start(100)

    def startFall(self):
        self.setFixedSize(150, 150)
        self.currentAction = self.startFall
        self.images = self.loadImages(base_folder / "crayon/Deskpet/resource/xialuo")
        self.currentImage = 0
        self.movingDirection = 0
        self.moveSpeed = 5
        self.stopOtherActions()
        self.timer.start(30)

    def stopOtherActions(self):
        self.timer.stop()
        if self.currentAction == self.startWalk:
            self.changeDirectionTimer.stop()  # Stop direction determination timer
            self.startIdle()
        elif self.currentAction == self.startLift:
            self.startIdle()
        elif self.currentAction == self.startFall:
            pass
        else:
            self.startIdle()

    def updateAnimation(self):
        self.setPixmap(self.images[self.currentImage])
        self.currentImage = (self.currentImage + 1) % len(self.images)
        if hasattr(self, 'movingDirection'):
            if self.currentAction == self.startFall:
                self.fallPet()
            else:
                self.movePet()

    def fallPet(self):
        self.setFixedSize(130, 130)
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        new_y = self.y() + self.moveSpeed
        if new_y > screen.height() - self.height() - 10:
            new_y = screen.height() - self.height() - 10
            self.timer.stop()
            self.startIdle()
        self.move(self.x(), new_y)

    def showMenu(self, position):
        print("showing menu")
        menu = QtWidgets.QMenu()
        menu.addAction("Walk", self.startWalk)
        menu.addAction("Fall", self.startFall)
        menu.addAction("Exercise", self.exercise)
        menu.addAction("Eating", self.eating)
        menu.addAction("Sit", self.sleep)
        menu.addAction("Wakeup", self.WakeUp)
        menu.addAction("Pet Xiaobai", self.summonXiaobai)
        menu.addSeparator() 
        menu.addAction("Close", self.close)
        menu.exec_(self.mapToGlobal(position))


    def pipi(self):
        self.setFixedSize(300, 130)
        self.currentAction = self.pipi
        self.images = self.loadImages(base_folder / "crayon/Deskpet/resource/pipi")
        self.currentImage = 0
        self.timer.start(25)
        self.moveSpeed = 0
        self.movingDirection = 0

    def exercise(self):
        self.setFixedSize(150,180 )
        self.currentAction = self.exercise
        self.images = self.loadImages(base_folder / "crayon/Deskpet/resource/yundong")
        self.currentImage = 0
        self.timer.start(125)
        self.moveSpeed = 0
        self.movingDirection = 0

    def eating(self):
        self.setFixedSize(160, 90)
        self.currentAction = self.eating
        self.images = self.loadImages(base_folder / "crayon/Deskpet/resource/eat")
        self.currentImage = 0
        self.timer.start(25)
        self.moveSpeed = 0
        self.movingDirection = 0
        QtCore.QTimer.singleShot(len(self.images) * 30, self.startIdle)

    def sleep(self):
        self.setFixedSize(160, 160)
        self.currentAction = self.sleep
        self.images = self.loadImages(base_folder / "crayon/Deskpet/resource/text")
        self.currentImage = 0
        self.timer.start(155)
        self.moveSpeed = 0
        self.movingDirection = 0
        QtCore.QTimer.singleShot(len(self.images) * 30, self.startIdle)
        

    def showWakeUpMenu(self):
        self.setFixedSize(130, 130)
        self.sleeping = True
        menu = QtWidgets.QMenu()
        menu.addAction("Wakeup", self.wakeUp)
        menu.exec_(self.mapToGlobal(self.pos()))

    def WakeUp(self):
        self.setFixedSize(180, 180)
        self.sleeping = False
        self.currentAction = self.WakeUp
        self.images = self.loadImages(base_folder / "crayon/Deskpet/resource/waken")
        self.currentImage = 0
        self.timer.start(30)
        # Delay, wait for all images to finish loading
        QtCore.QTimer.singleShot(len(self.images) * 30, self.finishWakeUp)


    def finishWakeUp(self):
        self.movingDirection = 0
        self.wakeUpImagesLoaded = True
        self.setFixedSize(180, 180)
        self.timer.stop()
        self.currentAction = self.startIdle
        self.images = self.loadImages(base_folder / "crayon/Deskpet/resource/xianzhi")
        self.currentImage = 0
        self.timer.start(100)


    def starttalk(self):
        starttalk = ChatApp()
        starttalk.show()
        self.childPets.append(starttalk)

    def summonXiaobai(self):
        self.setFixedSize(160, 90)
        self.currentAction = self.summonXiaobai
        self.images = self.loadImages(base_folder / "crayon/Deskpet/resource/xiaobai")
        self.currentImage = 0
        self.timer.start(25)
        self.moveSpeed = 0
        self.movingDirection = 0

    def closeEvent(self, event):
        for child in self.childPets:
            child.close()  #  Close all subwindows
        super().closeEvent(event)

    def minimizeWindow(self):
        self.showMinimized()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.dragging = True
            self.isDragging = True
            self.drag_position = event.globalPos() - self.pos()
            print("drag position", self.drag_position)
            self.prevAction = self.currentAction
            self.startLift()

            event.accept()

    def mouseMoveEvent(self, event):

        if QtCore.Qt.LeftButton and self.isDragging:
            print("moving to", event.globalPos())
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        print("mouse relased")
        if event.button() == QtCore.Qt.LeftButton:
            self.dragging = False
            self.isDragging = False

            # Restart the changeDirectionTimer as needed.
            if self.currentAction == self.startWalk:
                self.changeDirectionTimer.start()

            self.prevAction()  # or self.startIdle(), Restore the state according to the previous action
            event.accept()

    def changeDirection(self):
        if self.currentAction == self.startFall or self.currentAction == self.eating or self.currentAction == self.sleep or self.currentAction == self.pipi or self.currentAction == self.exercise or self.currentAction == self.WakeUp or self.currentAction == self.startIdle or self.startMeet:
            return  # If a drop action is being performed without changing direction

        if random.random() < 0.5:  # Randomly select whether to change direction
            self.movingDirection *= -1
            self.change = True
            if self.change == True:
                # Stop loading the original image
                self.timer.stop()
                self.images = []  # Empty the current picture list
                self.startWalk()
                self.change = False

class XiaobaiWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setGeometry(500, 500, 125, 100)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.updateAnimation)
        self.images = self.loadImages(base_folder / "crayon/Deskpet/resource/xiaobai")
        self.currentImage = 0
        self.timer.start(20)
        self.dragPosition = QtCore.QPoint()
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(0, 0, 140, 100)

    # def mousePressEvent(self, event):
    #     if event.button() == QtCore.Qt.LeftButton:
    #         self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
    #         event.accept()

    # def mouseMoveEvent(self, event):
    #     if event.buttons() == QtCore.Qt.LeftButton:
    #         self.move(event.globalPos() - self.dragPosition)
    #         event.accept()

    def showMenu(self, position):
        print("showing menu")
        menu = QtWidgets.QMenu()
        menu.addAction("Minimize", self.minimizeWindow)
        menu.addAction("Back", self.close)
        menu.exec_(self.mapToGlobal(position))

    def loadImages(self, path):
        return [QtGui.QPixmap(os.path.join(path, f)) for f in os.listdir(path) if f.endswith('.png')]

    def updateAnimation(self):
        self.label.setPixmap(self.images[self.currentImage])
        self.currentImage = (self.currentImage + 1) % len(self.images)

    def minimizeWindow(self):
        self.showMinimized()

    def closeEvent(self, event):
        self.timer.stop()
        super().closeEvent(event)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.ContextMenu:
            logging.debug('damn, a bug')
            self.showMenu(event.pos())
            return True
        return super().eventFilter(obj, event)

    def showEvent(self, event):
        self.installEventFilter(self)


logging.getLogger().setLevel(logging.DEBUG)
app = QtWidgets.QApplication(sys.argv)
pet = DeskPet()
pet.show()
sys.exit(app.exec_())