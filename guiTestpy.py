# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QVBoxLayout, QScrollArea, QPushButton, QLineEdit, QApplication, QWidget, QMainWindow, QLabel, QRadioButton
from PyQt5.QtGui import QIcon, QPixmap
from class_tree import Tree
import os
from win32api import GetSystemMetrics
from PIL import Image



class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Decision Tree'
        self.width = GetSystemMetrics(0)*7/8
        self.height = GetSystemMetrics(1)*7/8
        self.left = (GetSystemMetrics(0)-self.width)/2
        self.top = (GetSystemMetrics(1)-self.height)/2

        self.tree = Tree()
        self.initUI()


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.width, self.height)


        def import_graph_pic(pic):
            pic.setGeometry(350, 120, 1000, 500)
            pic.setPixmap(QPixmap(os.getcwd() + os.path.sep + 'graf_in_progress.png'))

        def add_node_command():
            parent = input_parent.text()
            label = input_label.text()
            weight = input_weight.text()
            probability = input_probability.text()

            if parent == "":
                parent = None
            else:
                parent = int(parent)

            if label == "":
                label = None
            else:
                label = str(label)

            if weight == "":
                weight = 0
            else:
                weight = float(weight)

            if probability == "":
                probability = None
            else:
                probability = float(probability)


            self.tree.create_node(parent, external_label=label, weight=weight, probability=probability)
            import_graph_pic(pic)


        def remove_node_command():

            index = node_to_remove.text()

            if index == "":
                index = None
            else:
                index = int(index)

            self.tree.remove_node(index)
            import_graph_pic(pic)

        def calculate_command():
            if max_radio_button.isChecked(): self.tree_type = 'max'
            if min_radio_button.isChecked(): self.tree_type = 'min'

            self.tree.calculate_all(type=self.tree_type)
            im = Image.open(os.getcwd() + os.path.sep + 'graf1.png')
            im.show()


        def import_command():
            self.tree

        def save_command():
            return 0

        margin = 25
        base = 35
        increment = 35
        x_input = 100
        fixed_width = 200

        parent_label = QLabel('Parent: ', self)
        parent_label.move(margin, base)
        input_parent = QLineEdit(self)
        input_parent.move(x_input, base)
        input_parent.setFixedWidth(fixed_width)

        label_label = QLabel('Label: ', self)
        label_label.move(margin, base+increment)
        input_label = QLineEdit(self)
        input_label.move(x_input, base+increment)
        input_label.setFixedWidth(fixed_width)

        weight_label = QLabel('Weight: ', self)
        weight_label.move(margin, base+increment*2)
        input_weight = QLineEdit(self)
        input_weight.move(x_input, base+increment*2)
        input_weight.setFixedWidth(fixed_width)

        probability_label = QLabel('Probability: ', self)
        probability_label.move(margin, base+increment*3)
        input_probability = QLineEdit(self)
        input_probability.move(x_input, base+increment*3)
        input_probability.setFixedWidth(fixed_width)

        add_node = QPushButton(self)
        add_node.setText("Add node")
        add_node.clicked.connect(add_node_command)
        add_node.move(x_input+50, base+increment*4)

        remove_node_label = QLabel('Remove: ', self)
        remove_node_label.move(margin, base+increment*5)
        node_to_remove = QLineEdit(self)
        node_to_remove.move(x_input, base+increment*5)
        node_to_remove.setFixedWidth(fixed_width)

        remove_node = QPushButton(self)
        remove_node.setText("Remove node")
        remove_node.clicked.connect(remove_node_command)
        remove_node.move(x_input+50, base+increment*6)

        max_radio_button = QRadioButton(self)
        max_radio_button.setText("Max value")
        max_radio_button.move(x_input+50+15, base+increment*8)

        min_radio_button = QRadioButton(self)
        min_radio_button.setText("Min value")
        min_radio_button.move(x_input+50+15, base+increment*9)



        calculate = QPushButton(self)
        calculate.setText("Calculate")
        calculate.clicked.connect(calculate_command)
        calculate.move(x_input+50, base+increment*10)

        path_label = QLabel('Path: ', self)
        path_label.move(margin, base+increment*12)
        input_path = QLineEdit(self)
        input_path.move(x_input, base+increment*12)
        input_path.setFixedWidth(fixed_width)

        save_to_path = QPushButton(self)
        save_to_path.setText("Save")
        save_to_path.move(x_input+100, base+increment*13)

        import_from_path = QPushButton(self)
        import_from_path.setText("Import")
        import_from_path.move(x_input, base+increment*13)

        pic = QLabel(self)
        pic.setGeometry(350, 100, 757, 287)
        pic.setPixmap(QPixmap(os.getcwd() + os.path.sep + 'graf_in_progress.png'))

        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scrollContent = QWidget(scroll)

        scrollLayout = QVBoxLayout(scrollContent)
        scrollContent.setLayout(scrollLayout)
        scrollLayout.addWidget(pic)
        scroll.setWidget(scrollContent)
        scroll.setGeometry(350, 35, 1250, 800)


        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
