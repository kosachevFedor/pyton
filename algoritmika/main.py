#создай тут фоторедактор Easy Editor!
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog, QInputDialog, QListWidget, QApplication, QWidget, QTextEdit, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
import os
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageFilter, ImageEnhance

app = QApplication([])
main_win = QWidget()

main_win.setWindowTitle('Easy Editor')

main_win.resize(700,500)

picimage = QLabel('картинка')

file_ = QPushButton('Папка')
blwt = QPushButton('Ч/Б')
left = QPushButton('Влево')
right = QPushButton('Вправо')
mirror = QPushButton('Зеркало')
sharp = QPushButton('Резкость')
blur = QPushButton('Размытость')

list_pic = QListWidget()

main_line = QHBoxLayout()
line1 = QVBoxLayout()
line2 = QVBoxLayout()
line1_1 = QHBoxLayout()

line2.addWidget(file_)
line2.addWidget(list_pic)

line1_1.addWidget(left)
line1_1.addWidget(right)
line1_1.addWidget(mirror)
line1_1.addWidget(sharp)
line1_1.addWidget(blur)
line1_1.addWidget(blwt)

line1.addWidget(picimage)
line1.addLayout(line1_1)

main_line.addLayout(line2)
main_line.addLayout(line1)

main_win.setLayout(main_line)
workdir = ' '
    
def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()
      

results = []

def filter(filenames, extensions):
    for fil in filenames:
        for extension in extensions:
            if fil.endswith(extension):
                results.append(fil)
    return results

def ShowFiles():
    chooseWorkdir()
    extensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp']
    filenames = filter(os.listdir(workdir), extensions)
    list_pic.clear()
    for result in results:
        list_pic.addItem(result)

file_.clicked.connect(ShowFiles)

class ImageProcessor:
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = "Modified"

    def loadImage(self, dir, filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)

    def saveImage(self):
        path = os.path.join(self.dir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)

    def showImage(self, path):
        picimage.hide()
        pixmapimage = QPixmap(path)
        w, h = picimage.width(), picimage.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        picimage.setPixmap(pixmapimage)
        picimage.show()

    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def right_pic(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)
    def left_pic(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)


    def mirror_pic(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def sharp_pic(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def blur_pic(self):
        self.image = self.image.filter(ImageFilter.BLUR)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)


def showChosenImage():
    if list_pic.currentRow() >= 0:
        filename = list_pic.currentItem().text()
        workimage.loadImage(workdir, filename)
        image_path = os.path.join(workimage.dir, workimage.filename)
        workimage.showImage(image_path)

workimage = ImageProcessor()

list_pic.currentRowChanged.connect(showChosenImage)

blwt.clicked.connect(workimage.do_bw)
right.clicked.connect(workimage.right_pic)
sharp.clicked.connect(workimage.sharp_pic)
left.clicked.connect(workimage.left_pic)
mirror.clicked.connect(workimage.mirror_pic)
blur.clicked.connect(workimage.blur_pic)

main_win.show()
app.exec_()