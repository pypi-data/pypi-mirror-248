# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'searchdialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SearchDialog(object):
    def setupUi(self, SearchDialog):
        SearchDialog.setObjectName("SearchDialog")
        SearchDialog.resize(801, 598)
        SearchDialog.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.verticalLayout = QtWidgets.QVBoxLayout(SearchDialog)
        self.verticalLayout.setContentsMargins(-1, -1, -1, 3)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.searchLayout = QtWidgets.QHBoxLayout()
        self.searchLayout.setSpacing(5)
        self.searchLayout.setObjectName("searchLayout")
        self.searchLabel = QtWidgets.QLabel(SearchDialog)
        self.searchLabel.setObjectName("searchLabel")
        self.searchLayout.addWidget(self.searchLabel)
        self.lineEdit = QtWidgets.QLineEdit(SearchDialog)
        self.lineEdit.setObjectName("lineEdit")
        self.searchLayout.addWidget(self.lineEdit)
        self.syntaxLabel = QtWidgets.QLabel(SearchDialog)
        self.syntaxLabel.setObjectName("syntaxLabel")
        self.searchLayout.addWidget(self.syntaxLabel)
        self.syntaxComboBox = QtWidgets.QComboBox(SearchDialog)
        self.syntaxComboBox.setObjectName("syntaxComboBox")
        self.syntaxComboBox.addItem("")
        self.syntaxComboBox.addItem("")
        self.syntaxComboBox.addItem("")
        self.syntaxComboBox.addItem("")
        self.syntaxComboBox.addItem("")
        self.syntaxComboBox.addItem("")
        self.syntaxComboBox.addItem("")
        self.syntaxComboBox.setItemText(6, "")
        self.searchLayout.addWidget(self.syntaxComboBox)
        self.caseCheckbox = QtWidgets.QCheckBox(SearchDialog)
        self.caseCheckbox.setObjectName("caseCheckbox")
        self.searchLayout.addWidget(self.caseCheckbox)
        self.searchLayout.setStretch(0, 1)
        self.searchLayout.setStretch(1, 10)
        self.searchLayout.setStretch(2, 1)
        self.searchLayout.setStretch(3, 2)
        self.searchLayout.setStretch(4, 1)
        self.verticalLayout.addLayout(self.searchLayout)
        self.viewLayout = QtWidgets.QHBoxLayout()
        self.viewLayout.setSpacing(3)
        self.viewLayout.setObjectName("viewLayout")
        self.availableFrame = QtWidgets.QFrame(SearchDialog)
        self.availableFrame.setObjectName("availableFrame")
        self.availableLayout = QtWidgets.QVBoxLayout(self.availableFrame)
        self.availableLayout.setObjectName("availableLayout")
        self.availableLabel = QtWidgets.QLabel(self.availableFrame)
        self.availableLabel.setTextFormat(QtCore.Qt.RichText)
        self.availableLabel.setObjectName("availableLabel")
        self.availableLayout.addWidget(self.availableLabel)
        self.availableView = QtWidgets.QTableView(self.availableFrame)
        self.availableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.availableView.setTabKeyNavigation(False)
        self.availableView.setAlternatingRowColors(True)
        self.availableView.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.availableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.availableView.setObjectName("availableView")
        self.availableLayout.addWidget(self.availableView)
        self.viewLayout.addWidget(self.availableFrame)
        self.leftRightFrame = QtWidgets.QFrame(SearchDialog)
        self.leftRightFrame.setObjectName("leftRightFrame")
        self.leftRightLayout = QtWidgets.QVBoxLayout(self.leftRightFrame)
        self.leftRightLayout.setObjectName("leftRightLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.leftRightLayout.addItem(spacerItem)
        self.rightButton = QtWidgets.QPushButton(self.leftRightFrame)
        self.rightButton.setEnabled(False)
        self.rightButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/arrow-right.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rightButton.setIcon(icon)
        self.rightButton.setObjectName("rightButton")
        self.leftRightLayout.addWidget(self.rightButton)
        self.leftButton = QtWidgets.QPushButton(self.leftRightFrame)
        self.leftButton.setEnabled(False)
        self.leftButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/arrow-left.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.leftButton.setIcon(icon1)
        self.leftButton.setObjectName("leftButton")
        self.leftRightLayout.addWidget(self.leftButton)
        self.resetButton = QtWidgets.QPushButton(self.leftRightFrame)
        self.resetButton.setEnabled(False)
        self.resetButton.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/redo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.resetButton.setIcon(icon2)
        self.resetButton.setObjectName("resetButton")
        self.leftRightLayout.addWidget(self.resetButton)
        self.unselectAllButton = QtWidgets.QPushButton(self.leftRightFrame)
        self.unselectAllButton.setEnabled(False)
        self.unselectAllButton.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/x-logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.unselectAllButton.setIcon(icon3)
        self.unselectAllButton.setObjectName("unselectAllButton")
        self.leftRightLayout.addWidget(self.unselectAllButton)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.leftRightLayout.addItem(spacerItem1)
        self.viewLayout.addWidget(self.leftRightFrame)
        self.selectedFrame = QtWidgets.QFrame(SearchDialog)
        self.selectedFrame.setObjectName("selectedFrame")
        self.selectedLayout = QtWidgets.QVBoxLayout(self.selectedFrame)
        self.selectedLayout.setObjectName("selectedLayout")
        self.selectedLabel = QtWidgets.QLabel(self.selectedFrame)
        self.selectedLabel.setTextFormat(QtCore.Qt.RichText)
        self.selectedLabel.setObjectName("selectedLabel")
        self.selectedLayout.addWidget(self.selectedLabel)
        self.selectedListWidget = QtWidgets.QListWidget(self.selectedFrame)
        self.selectedListWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.selectedListWidget.setTabKeyNavigation(False)
        self.selectedListWidget.setAlternatingRowColors(True)
        self.selectedListWidget.setSelectionMode(QtWidgets.QAbstractItemView.ContiguousSelection)
        self.selectedListWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.selectedListWidget.setResizeMode(QtWidgets.QListView.Adjust)
        self.selectedListWidget.setLayoutMode(QtWidgets.QListView.Batched)
        self.selectedListWidget.setModelColumn(0)
        self.selectedListWidget.setUniformItemSizes(True)
        self.selectedListWidget.setObjectName("selectedListWidget")
        self.selectedLayout.addWidget(self.selectedListWidget)
        self.viewLayout.addWidget(self.selectedFrame)
        self.verticalLayout.addLayout(self.viewLayout)
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.buttonLayout.setSpacing(5)
        self.buttonLayout.setObjectName("buttonLayout")
        self.matchLabel = QtWidgets.QLabel(SearchDialog)
        self.matchLabel.setObjectName("matchLabel")
        self.buttonLayout.addWidget(self.matchLabel)
        self.rowCount = QtWidgets.QLineEdit(SearchDialog)
        self.rowCount.setReadOnly(True)
        self.rowCount.setObjectName("rowCount")
        self.buttonLayout.addWidget(self.rowCount)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.buttonLayout.addItem(spacerItem2)
        self.controlsLabel = QtWidgets.QLabel(SearchDialog)
        self.controlsLabel.setObjectName("controlsLabel")
        self.buttonLayout.addWidget(self.controlsLabel)
        self.findPrevButton = QtWidgets.QPushButton(SearchDialog)
        self.findPrevButton.setEnabled(False)
        self.findPrevButton.setIcon(icon1)
        self.findPrevButton.setObjectName("findPrevButton")
        self.buttonLayout.addWidget(self.findPrevButton)
        self.findNextButton = QtWidgets.QPushButton(SearchDialog)
        self.findNextButton.setEnabled(False)
        self.findNextButton.setIcon(icon)
        self.findNextButton.setObjectName("findNextButton")
        self.buttonLayout.addWidget(self.findNextButton)
        self.plotButton = QtWidgets.QPushButton(SearchDialog)
        self.plotButton.setEnabled(False)
        self.plotButton.setObjectName("plotButton")
        self.buttonLayout.addWidget(self.plotButton)
        self.showButton = QtWidgets.QPushButton(SearchDialog)
        self.showButton.setEnabled(False)
        self.showButton.setObjectName("showButton")
        self.buttonLayout.addWidget(self.showButton)
        self.hideButton = QtWidgets.QPushButton(SearchDialog)
        self.hideButton.setEnabled(False)
        self.hideButton.setObjectName("hideButton")
        self.buttonLayout.addWidget(self.hideButton)
        self.selectButton = QtWidgets.QPushButton(SearchDialog)
        self.selectButton.setEnabled(False)
        self.selectButton.setObjectName("selectButton")
        self.buttonLayout.addWidget(self.selectButton)
        self.cancelButton = QtWidgets.QPushButton(SearchDialog)
        self.cancelButton.setObjectName("cancelButton")
        self.buttonLayout.addWidget(self.cancelButton)
        self.buttonLayout.setStretch(0, 1)
        self.buttonLayout.setStretch(1, 3)
        self.buttonLayout.setStretch(2, 4)
        self.buttonLayout.setStretch(3, 1)
        self.buttonLayout.setStretch(4, 1)
        self.buttonLayout.setStretch(5, 1)
        self.buttonLayout.setStretch(6, 1)
        self.buttonLayout.setStretch(7, 1)
        self.buttonLayout.setStretch(8, 1)
        self.buttonLayout.setStretch(9, 1)
        self.buttonLayout.setStretch(10, 1)
        self.verticalLayout.addLayout(self.buttonLayout)
        self.verticalLayout.setStretch(1, 100)

        self.retranslateUi(SearchDialog)
        self.syntaxComboBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(SearchDialog)

    def retranslateUi(self, SearchDialog):
        _translate = QtCore.QCoreApplication.translate
        SearchDialog.setWindowTitle(_translate("SearchDialog", "Search All Available Columns"))
        self.searchLabel.setText(_translate("SearchDialog", "Search"))
        self.lineEdit.setPlaceholderText(_translate("SearchDialog", "Start typing to search"))
        self.syntaxLabel.setText(_translate("SearchDialog", "Syntax"))
        self.syntaxComboBox.setItemText(0, _translate("SearchDialog", "Regular Expression"))
        self.syntaxComboBox.setItemText(1, _translate("SearchDialog", "RegExp2 (Greedy)"))
        self.syntaxComboBox.setItemText(2, _translate("SearchDialog", "Wildcard"))
        self.syntaxComboBox.setItemText(3, _translate("SearchDialog", "Wildcard (Unix)"))
        self.syntaxComboBox.setItemText(4, _translate("SearchDialog", "Fixed String"))
        self.syntaxComboBox.setItemText(5, _translate("SearchDialog", "XML Schema"))
        self.caseCheckbox.setText(_translate("SearchDialog", "Case Sensitive"))
        self.availableLabel.setText(_translate("SearchDialog", "<html><head/><body><p><span style=\" font-weight:600; text-decoration: underline;\">Available Columns:</span></p></body></html>"))
        self.rightButton.setToolTip(_translate("SearchDialog", "Select columns"))
        self.leftButton.setToolTip(_translate("SearchDialog", "Unselect columns"))
        self.resetButton.setToolTip(_translate("SearchDialog", "Reset to previous selection"))
        self.unselectAllButton.setToolTip(_translate("SearchDialog", "Unselect all"))
        self.selectedLabel.setText(_translate("SearchDialog", "<html><head/><body><p><span style=\" font-weight:600; text-decoration: underline;\">Selected Columns:</span></p></body></html>"))
        self.matchLabel.setText(_translate("SearchDialog", "# of Matches"))
        self.controlsLabel.setText(_translate("SearchDialog", "<html><head/><body><p><span style=\" font-weight:600; text-decoration: underline;\">Column Actions:</span></p></body></html>"))
        self.findPrevButton.setToolTip(_translate("SearchDialog", "Scroll to previous match"))
        self.findPrevButton.setText(_translate("SearchDialog", "Prev"))
        self.findNextButton.setToolTip(_translate("SearchDialog", "Scroll to next match"))
        self.findNextButton.setText(_translate("SearchDialog", "Next"))
        self.plotButton.setText(_translate("SearchDialog", "Plot"))
        self.showButton.setText(_translate("SearchDialog", "Show"))
        self.hideButton.setText(_translate("SearchDialog", "Hide"))
        self.selectButton.setText(_translate("SearchDialog", "Select"))
        self.cancelButton.setText(_translate("SearchDialog", "Cancel"))
import resources_rc
