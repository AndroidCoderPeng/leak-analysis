# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.12.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDoubleSpinBox, QFormLayout,
    QFrame, QGridLayout, QHBoxLayout, QLabel,
    QLayout, QLineEdit, QMainWindow, QPushButton,
    QSizePolicy, QSpacerItem, QSpinBox, QStatusBar,
    QTabWidget, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1200, 820)
        MainWindow.setMinimumSize(QSize(1024, 700))
        self.centralWidget = QWidget(MainWindow)
        self.centralWidget.setObjectName(u"centralWidget")
        self.rootLayout = QVBoxLayout(self.centralWidget)
        self.rootLayout.setSpacing(0)
        self.rootLayout.setObjectName(u"rootLayout")
        self.rootLayout.setContentsMargins(0, 0, 0, 0)
        self.contentLayout = QHBoxLayout()
        self.contentLayout.setSpacing(14)
        self.contentLayout.setObjectName(u"contentLayout")
        self.contentLayout.setContentsMargins(14, 14, 14, 14)
        self.leftColumnLayout = QVBoxLayout()
        self.leftColumnLayout.setSpacing(14)
        self.leftColumnLayout.setObjectName(u"leftColumnLayout")
        self.leftColumnLayout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.dataCard = QFrame(self.centralWidget)
        self.dataCard.setObjectName(u"dataCard")
        self.dataCard.setMaximumSize(QSize(275, 16777215))
        self.dataCard.setFrameShape(QFrame.Shape.StyledPanel)
        self.dataCard.setFrameShadow(QFrame.Shadow.Raised)
        self.dataCardLayout = QVBoxLayout(self.dataCard)
        self.dataCardLayout.setObjectName(u"dataCardLayout")
        self.dataTitle = QLabel(self.dataCard)
        self.dataTitle.setObjectName(u"dataTitle")
        font = QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.dataTitle.setFont(font)

        self.dataCardLayout.addWidget(self.dataTitle)

        self.dataSubtitle = QLabel(self.dataCard)
        self.dataSubtitle.setObjectName(u"dataSubtitle")
        self.dataSubtitle.setWordWrap(True)

        self.dataCardLayout.addWidget(self.dataSubtitle)

        self.fileBox = QFrame(self.dataCard)
        self.fileBox.setObjectName(u"fileBox")
        self.fileBox.setMinimumSize(QSize(0, 92))
        self.fileBox.setFrameShape(QFrame.Shape.StyledPanel)
        self.fileBox.setFrameShadow(QFrame.Shadow.Sunken)
        self.fileBoxLayout = QVBoxLayout(self.fileBox)
        self.fileBoxLayout.setObjectName(u"fileBoxLayout")
        self.fileNameLabel = QLabel(self.fileBox)
        self.fileNameLabel.setObjectName(u"fileNameLabel")
        self.fileNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.fileNameLabel.setWordWrap(True)

        self.fileBoxLayout.addWidget(self.fileNameLabel)

        self.fileHintLabel = QLabel(self.fileBox)
        self.fileHintLabel.setObjectName(u"fileHintLabel")
        self.fileHintLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.fileHintLabel.setWordWrap(True)

        self.fileBoxLayout.addWidget(self.fileHintLabel)


        self.dataCardLayout.addWidget(self.fileBox)

        self.statsGrid = QGridLayout()
        self.statsGrid.setSpacing(6)
        self.statsGrid.setObjectName(u"statsGrid")
        self.statAmpA = QFrame(self.dataCard)
        self.statAmpA.setObjectName(u"statAmpA")
        self.statAmpA.setFrameShape(QFrame.Shape.StyledPanel)
        self.statAmpALayout = QVBoxLayout(self.statAmpA)
        self.statAmpALayout.setSpacing(2)
        self.statAmpALayout.setObjectName(u"statAmpALayout")
        self.stAamp = QLabel(self.statAmpA)
        self.stAamp.setObjectName(u"stAamp")
        self.stAamp.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stAamp.setWordWrap(True)

        self.statAmpALayout.addWidget(self.stAamp)

        self.stAampCaption = QLabel(self.statAmpA)
        self.stAampCaption.setObjectName(u"stAampCaption")
        self.stAampCaption.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stAampCaption.setWordWrap(True)

        self.statAmpALayout.addWidget(self.stAampCaption)


        self.statsGrid.addWidget(self.statAmpA, 1, 0, 1, 1)

        self.statAmpB = QFrame(self.dataCard)
        self.statAmpB.setObjectName(u"statAmpB")
        self.statAmpB.setFrameShape(QFrame.Shape.StyledPanel)
        self.statAmpBLayout = QVBoxLayout(self.statAmpB)
        self.statAmpBLayout.setSpacing(2)
        self.statAmpBLayout.setObjectName(u"statAmpBLayout")
        self.stBamp = QLabel(self.statAmpB)
        self.stBamp.setObjectName(u"stBamp")
        self.stBamp.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stBamp.setWordWrap(True)

        self.statAmpBLayout.addWidget(self.stBamp)

        self.stBampCaption = QLabel(self.statAmpB)
        self.stBampCaption.setObjectName(u"stBampCaption")
        self.stBampCaption.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stBampCaption.setWordWrap(True)

        self.statAmpBLayout.addWidget(self.stBampCaption)


        self.statsGrid.addWidget(self.statAmpB, 1, 1, 1, 1)

        self.statLength = QFrame(self.dataCard)
        self.statLength.setObjectName(u"statLength")
        self.statLength.setFrameShape(QFrame.Shape.StyledPanel)
        self.statLengthLayout = QVBoxLayout(self.statLength)
        self.statLengthLayout.setSpacing(2)
        self.statLengthLayout.setObjectName(u"statLengthLayout")
        self.stLen = QLabel(self.statLength)
        self.stLen.setObjectName(u"stLen")
        self.stLen.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.statLengthLayout.addWidget(self.stLen)

        self.stLenCaption = QLabel(self.statLength)
        self.stLenCaption.setObjectName(u"stLenCaption")
        self.stLenCaption.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stLenCaption.setWordWrap(True)

        self.statLengthLayout.addWidget(self.stLenCaption)


        self.statsGrid.addWidget(self.statLength, 0, 0, 1, 2)


        self.dataCardLayout.addLayout(self.statsGrid)

        self.cardActionsGrid = QGridLayout()
        self.cardActionsGrid.setSpacing(6)
        self.cardActionsGrid.setObjectName(u"cardActionsGrid")
        self.btnImportData = QPushButton(self.dataCard)
        self.btnImportData.setObjectName(u"btnImportData")

        self.cardActionsGrid.addWidget(self.btnImportData, 0, 0, 1, 1)

        self.btnImportCfg = QPushButton(self.dataCard)
        self.btnImportCfg.setObjectName(u"btnImportCfg")

        self.cardActionsGrid.addWidget(self.btnImportCfg, 0, 1, 1, 1)

        self.btnRun = QPushButton(self.dataCard)
        self.btnRun.setObjectName(u"btnRun")

        self.cardActionsGrid.addWidget(self.btnRun, 1, 0, 1, 2)


        self.dataCardLayout.addLayout(self.cardActionsGrid)


        self.leftColumnLayout.addWidget(self.dataCard)

        self.parameterCard = QFrame(self.centralWidget)
        self.parameterCard.setObjectName(u"parameterCard")
        self.parameterCard.setMaximumSize(QSize(275, 16777215))
        self.parameterCard.setFrameShape(QFrame.Shape.StyledPanel)
        self.parameterCard.setFrameShadow(QFrame.Shadow.Raised)
        self.parameterCardLayout = QVBoxLayout(self.parameterCard)
        self.parameterCardLayout.setObjectName(u"parameterCardLayout")
        self.parameterTitle = QLabel(self.parameterCard)
        self.parameterTitle.setObjectName(u"parameterTitle")
        self.parameterTitle.setFont(font)

        self.parameterCardLayout.addWidget(self.parameterTitle)

        self.parameterForm = QFormLayout()
        self.parameterForm.setObjectName(u"parameterForm")
        self.parameterForm.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        self.parameterForm.setLabelAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.parameterForm.setHorizontalSpacing(8)
        self.parameterForm.setVerticalSpacing(8)
        self.sampleRateLabel = QLabel(self.parameterCard)
        self.sampleRateLabel.setObjectName(u"sampleRateLabel")

        self.parameterForm.setWidget(0, QFormLayout.ItemRole.LabelRole, self.sampleRateLabel)

        self.cfgSampleRate = QLineEdit(self.parameterCard)
        self.cfgSampleRate.setObjectName(u"cfgSampleRate")
        self.cfgSampleRate.setEnabled(False)

        self.parameterForm.setWidget(0, QFormLayout.ItemRole.FieldRole, self.cfgSampleRate)

        self.distanceLabel = QLabel(self.parameterCard)
        self.distanceLabel.setObjectName(u"distanceLabel")

        self.parameterForm.setWidget(1, QFormLayout.ItemRole.LabelRole, self.distanceLabel)

        self.cfgDis = QDoubleSpinBox(self.parameterCard)
        self.cfgDis.setObjectName(u"cfgDis")
        self.cfgDis.setDecimals(1)
        self.cfgDis.setMaximum(100000.000000000000000)

        self.parameterForm.setWidget(1, QFormLayout.ItemRole.FieldRole, self.cfgDis)

        self.materialLabel = QLabel(self.parameterCard)
        self.materialLabel.setObjectName(u"materialLabel")

        self.parameterForm.setWidget(3, QFormLayout.ItemRole.LabelRole, self.materialLabel)

        self.cfgMaterial = QComboBox(self.parameterCard)
        self.cfgMaterial.setObjectName(u"cfgMaterial")

        self.parameterForm.setWidget(3, QFormLayout.ItemRole.FieldRole, self.cfgMaterial)

        self.diameterLabel = QLabel(self.parameterCard)
        self.diameterLabel.setObjectName(u"diameterLabel")

        self.parameterForm.setWidget(2, QFormLayout.ItemRole.LabelRole, self.diameterLabel)

        self.cfgDiam = QSpinBox(self.parameterCard)
        self.cfgDiam.setObjectName(u"cfgDiam")
        self.cfgDiam.setMaximum(100000)

        self.parameterForm.setWidget(2, QFormLayout.ItemRole.FieldRole, self.cfgDiam)

        self.velocityLabel = QLabel(self.parameterCard)
        self.velocityLabel.setObjectName(u"velocityLabel")

        self.parameterForm.setWidget(4, QFormLayout.ItemRole.LabelRole, self.velocityLabel)

        self.cfgVelo = QDoubleSpinBox(self.parameterCard)
        self.cfgVelo.setObjectName(u"cfgVelo")
        self.cfgVelo.setDecimals(1)
        self.cfgVelo.setMaximum(100000.000000000000000)

        self.parameterForm.setWidget(4, QFormLayout.ItemRole.FieldRole, self.cfgVelo)

        self.freqMaxLabel = QLabel(self.parameterCard)
        self.freqMaxLabel.setObjectName(u"freqMaxLabel")

        self.parameterForm.setWidget(5, QFormLayout.ItemRole.LabelRole, self.freqMaxLabel)

        self.cfgFreqMax = QDoubleSpinBox(self.parameterCard)
        self.cfgFreqMax.setObjectName(u"cfgFreqMax")
        self.cfgFreqMax.setDecimals(1)
        self.cfgFreqMax.setMaximum(1000000.000000000000000)

        self.parameterForm.setWidget(5, QFormLayout.ItemRole.FieldRole, self.cfgFreqMax)

        self.freqMinLabel = QLabel(self.parameterCard)
        self.freqMinLabel.setObjectName(u"freqMinLabel")

        self.parameterForm.setWidget(6, QFormLayout.ItemRole.LabelRole, self.freqMinLabel)

        self.cfgFreqMin = QDoubleSpinBox(self.parameterCard)
        self.cfgFreqMin.setObjectName(u"cfgFreqMin")
        self.cfgFreqMin.setDecimals(1)
        self.cfgFreqMin.setMaximum(1000000.000000000000000)

        self.parameterForm.setWidget(6, QFormLayout.ItemRole.FieldRole, self.cfgFreqMin)


        self.parameterCardLayout.addLayout(self.parameterForm)

        self.parameterSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.parameterCardLayout.addItem(self.parameterSpacer)

        self.parameterHint = QLabel(self.parameterCard)
        self.parameterHint.setObjectName(u"parameterHint")
        self.parameterHint.setWordWrap(True)

        self.parameterCardLayout.addWidget(self.parameterHint)


        self.leftColumnLayout.addWidget(self.parameterCard)

        self.leftColumnLayout.setStretch(1, 1)

        self.contentLayout.addLayout(self.leftColumnLayout)

        self.rightColumn = QWidget(self.centralWidget)
        self.rightColumn.setObjectName(u"rightColumn")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rightColumn.sizePolicy().hasHeightForWidth())
        self.rightColumn.setSizePolicy(sizePolicy)
        self.rightColumnLayout = QVBoxLayout(self.rightColumn)
        self.rightColumnLayout.setSpacing(14)
        self.rightColumnLayout.setObjectName(u"rightColumnLayout")
        self.rightColumnLayout.setContentsMargins(0, 0, 0, 0)
        self.metricsLayout = QGridLayout()
        self.metricsLayout.setSpacing(10)
        self.metricsLayout.setObjectName(u"metricsLayout")
        self.metricDisB = QFrame(self.rightColumn)
        self.metricDisB.setObjectName(u"metricDisB")
        self.metricDisB.setFrameShape(QFrame.Shape.StyledPanel)
        self.metricDisBLayout = QVBoxLayout(self.metricDisB)
        self.metricDisBLayout.setObjectName(u"metricDisBLayout")
        self.metricDisBLabel = QLabel(self.metricDisB)
        self.metricDisBLabel.setObjectName(u"metricDisBLabel")

        self.metricDisBLayout.addWidget(self.metricDisBLabel)

        self.mDisB = QLabel(self.metricDisB)
        self.mDisB.setObjectName(u"mDisB")
        font1 = QFont()
        font1.setPointSize(14)
        font1.setBold(True)
        self.mDisB.setFont(font1)

        self.metricDisBLayout.addWidget(self.mDisB)


        self.metricsLayout.addWidget(self.metricDisB, 0, 1, 1, 1)

        self.metricSnr = QFrame(self.rightColumn)
        self.metricSnr.setObjectName(u"metricSnr")
        self.metricSnr.setFrameShape(QFrame.Shape.StyledPanel)
        self.metricSnrLayout = QVBoxLayout(self.metricSnr)
        self.metricSnrLayout.setObjectName(u"metricSnrLayout")
        self.metricSnrLabel = QLabel(self.metricSnr)
        self.metricSnrLabel.setObjectName(u"metricSnrLabel")

        self.metricSnrLayout.addWidget(self.metricSnrLabel)

        self.mSnr = QLabel(self.metricSnr)
        self.mSnr.setObjectName(u"mSnr")
        self.mSnr.setFont(font1)

        self.metricSnrLayout.addWidget(self.mSnr)


        self.metricsLayout.addWidget(self.metricSnr, 0, 2, 1, 1)

        self.metricDisA = QFrame(self.rightColumn)
        self.metricDisA.setObjectName(u"metricDisA")
        self.metricDisA.setFrameShape(QFrame.Shape.StyledPanel)
        self.metricDisALayout = QVBoxLayout(self.metricDisA)
        self.metricDisALayout.setObjectName(u"metricDisALayout")
        self.metricDisALabel = QLabel(self.metricDisA)
        self.metricDisALabel.setObjectName(u"metricDisALabel")

        self.metricDisALayout.addWidget(self.metricDisALabel)

        self.mDisA = QLabel(self.metricDisA)
        self.mDisA.setObjectName(u"mDisA")
        self.mDisA.setFont(font1)

        self.metricDisALayout.addWidget(self.mDisA)


        self.metricsLayout.addWidget(self.metricDisA, 0, 0, 1, 1)


        self.rightColumnLayout.addLayout(self.metricsLayout)

        self.correlationCard = QFrame(self.rightColumn)
        self.correlationCard.setObjectName(u"correlationCard")
        self.correlationCard.setMinimumSize(QSize(0, 280))
        self.correlationCard.setFrameShape(QFrame.Shape.StyledPanel)
        self.correlationCard.setFrameShadow(QFrame.Shadow.Raised)
        self.correlationCardLayout = QVBoxLayout(self.correlationCard)
        self.correlationCardLayout.setObjectName(u"correlationCardLayout")
        self.correlationTitle = QLabel(self.correlationCard)
        self.correlationTitle.setObjectName(u"correlationTitle")
        self.correlationTitle.setFont(font)

        self.correlationCardLayout.addWidget(self.correlationTitle)

        self.correlationSubtitle = QLabel(self.correlationCard)
        self.correlationSubtitle.setObjectName(u"correlationSubtitle")

        self.correlationCardLayout.addWidget(self.correlationSubtitle)

        self.corrPlot = QFrame(self.correlationCard)
        self.corrPlot.setObjectName(u"corrPlot")
        self.corrPlot.setMinimumSize(QSize(0, 210))
        self.corrPlot.setFrameShape(QFrame.Shape.StyledPanel)
        self.corrPlot.setFrameShadow(QFrame.Shadow.Sunken)
        self.corrPlotLayout = QVBoxLayout(self.corrPlot)
        self.corrPlotLayout.setObjectName(u"corrPlotLayout")
        self.corrEmpty = QLabel(self.corrPlot)
        self.corrEmpty.setObjectName(u"corrEmpty")
        self.corrEmpty.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.corrPlotLayout.addWidget(self.corrEmpty)


        self.correlationCardLayout.addWidget(self.corrPlot)

        self.correlationLegend = QHBoxLayout()
        self.correlationLegend.setObjectName(u"correlationLegend")
        self.corrLegendCoefficient = QLabel(self.correlationCard)
        self.corrLegendCoefficient.setObjectName(u"corrLegendCoefficient")

        self.correlationLegend.addWidget(self.corrLegendCoefficient)

        self.corrLegendPeak = QLabel(self.correlationCard)
        self.corrLegendPeak.setObjectName(u"corrLegendPeak")

        self.correlationLegend.addWidget(self.corrLegendPeak)

        self.correlationLegendSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.correlationLegend.addItem(self.correlationLegendSpacer)


        self.correlationCardLayout.addLayout(self.correlationLegend)


        self.rightColumnLayout.addWidget(self.correlationCard)

        self.signalCard = QFrame(self.rightColumn)
        self.signalCard.setObjectName(u"signalCard")
        self.signalCard.setMinimumSize(QSize(0, 250))
        self.signalCard.setFrameShape(QFrame.Shape.StyledPanel)
        self.signalCard.setFrameShadow(QFrame.Shadow.Raised)
        self.signalCardLayout = QVBoxLayout(self.signalCard)
        self.signalCardLayout.setObjectName(u"signalCardLayout")
        self.signalTitleLayout = QHBoxLayout()
        self.signalTitleLayout.setObjectName(u"signalTitleLayout")
        self.signalTitle = QLabel(self.signalCard)
        self.signalTitle.setObjectName(u"signalTitle")
        self.signalTitle.setFont(font)

        self.signalTitleLayout.addWidget(self.signalTitle)

        self.sigDur = QLabel(self.signalCard)
        self.sigDur.setObjectName(u"sigDur")

        self.signalTitleLayout.addWidget(self.sigDur)

        self.signalTitleSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.signalTitleLayout.addItem(self.signalTitleSpacer)


        self.signalCardLayout.addLayout(self.signalTitleLayout)

        self.signalTabs = QTabWidget(self.signalCard)
        self.signalTabs.setObjectName(u"signalTabs")
        self.waveTab = QWidget()
        self.waveTab.setObjectName(u"waveTab")
        self.waveTabLayout = QVBoxLayout(self.waveTab)
        self.waveTabLayout.setObjectName(u"waveTabLayout")
        self.waveBoxA = QFrame(self.waveTab)
        self.waveBoxA.setObjectName(u"waveBoxA")
        self.waveBoxA.setMinimumSize(QSize(0, 110))
        self.waveBoxA.setFrameShape(QFrame.Shape.NoFrame)
        self.waveBoxALayout = QVBoxLayout(self.waveBoxA)
        self.waveBoxALayout.setObjectName(u"waveBoxALayout")
        self.waveBoxALayout.setContentsMargins(0, 0, 0, 0)

        self.waveTabLayout.addWidget(self.waveBoxA)

        self.waveBoxB = QFrame(self.waveTab)
        self.waveBoxB.setObjectName(u"waveBoxB")
        self.waveBoxB.setMinimumSize(QSize(0, 110))
        self.waveBoxB.setFrameShape(QFrame.Shape.NoFrame)
        self.waveBoxBLayout = QVBoxLayout(self.waveBoxB)
        self.waveBoxBLayout.setObjectName(u"waveBoxBLayout")
        self.waveBoxBLayout.setContentsMargins(0, 0, 0, 0)

        self.waveTabLayout.addWidget(self.waveBoxB)

        self.signalTabs.addTab(self.waveTab, "")
        self.spectrumTab = QWidget()
        self.spectrumTab.setObjectName(u"spectrumTab")
        self.spectrumTabLayout = QVBoxLayout(self.spectrumTab)
        self.spectrumTabLayout.setObjectName(u"spectrumTabLayout")
        self.specBox = QFrame(self.spectrumTab)
        self.specBox.setObjectName(u"specBox")
        self.specBox.setFrameShape(QFrame.Shape.NoFrame)
        self.specBoxLayout = QVBoxLayout(self.specBox)
        self.specBoxLayout.setObjectName(u"specBoxLayout")
        self.specBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.spectrumTabLayout.addWidget(self.specBox)

        self.signalTabs.addTab(self.spectrumTab, "")

        self.signalCardLayout.addWidget(self.signalTabs)

        self.signalLegend = QHBoxLayout()
        self.signalLegend.setObjectName(u"signalLegend")
        self.signalLegendA = QLabel(self.signalCard)
        self.signalLegendA.setObjectName(u"signalLegendA")

        self.signalLegend.addWidget(self.signalLegendA)

        self.signalLegendB = QLabel(self.signalCard)
        self.signalLegendB.setObjectName(u"signalLegendB")

        self.signalLegend.addWidget(self.signalLegendB)

        self.signalLegendRange = QLabel(self.signalCard)
        self.signalLegendRange.setObjectName(u"signalLegendRange")

        self.signalLegend.addWidget(self.signalLegendRange)

        self.signalLegendSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.signalLegend.addItem(self.signalLegendSpacer)


        self.signalCardLayout.addLayout(self.signalLegend)


        self.rightColumnLayout.addWidget(self.signalCard)

        self.rightColumnLayout.setStretch(1, 1)
        self.rightColumnLayout.setStretch(2, 1)

        self.contentLayout.addWidget(self.rightColumn)


        self.rootLayout.addLayout(self.contentLayout)

        MainWindow.setCentralWidget(self.centralWidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.cfgMaterial.setCurrentIndex(-1)
        self.signalTabs.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"LeakAnalysis \u00b7 \u6f0f\u6c34\u76f8\u5173\u5b9a\u4f4d\u7cfb\u7edf", None))
        self.dataTitle.setText(QCoreApplication.translate("MainWindow", u"\u6570\u636e", None))
        self.dataSubtitle.setText(QCoreApplication.translate("MainWindow", u"\u5355\u5217 txt \u00b7 \u524d\u534a A / \u540e\u534a B", None))
        self.fileNameLabel.setText(QCoreApplication.translate("MainWindow", u"\u672a\u5bfc\u5165\u6570\u636e\u6587\u4ef6", None))
        self.fileHintLabel.setText(QCoreApplication.translate("MainWindow", u"\u652f\u6301 .txt / .dat\uff0c\u5355\u5217\u6570\u503c\uff0c\u524d 1/2 \u4e3a\u4f20\u611f\u5668 A\uff0c\u540e 1/2 \u4e3a\u4f20\u611f\u5668 B", None))
        self.stAamp.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.stAampCaption.setText(QCoreApplication.translate("MainWindow", u"A \u901a\u9053\u5e45\u503c\u8303\u56f4", None))
        self.stBamp.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.stBampCaption.setText(QCoreApplication.translate("MainWindow", u"B \u901a\u9053\u5e45\u503c\u8303\u56f4", None))
        self.stLen.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.stLenCaption.setText(QCoreApplication.translate("MainWindow", u"\u91c7\u6837\u70b9\u6570 / \u901a\u9053", None))
        self.btnImportData.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u5165\u6570\u636e", None))
        self.btnImportCfg.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u5165\u914d\u7f6e", None))
        self.btnRun.setText(QCoreApplication.translate("MainWindow", u"\u6267\u884c\u5b9a\u4f4d", None))
        self.parameterTitle.setText(QCoreApplication.translate("MainWindow", u"\u5b9a\u4f4d\u53c2\u6570", None))
        self.sampleRateLabel.setText(QCoreApplication.translate("MainWindow", u"\u91c7\u6837\u7387 (Hz)", None))
        self.cfgSampleRate.setText(QCoreApplication.translate("MainWindow", u"7500", None))
        self.distanceLabel.setText(QCoreApplication.translate("MainWindow", u"\u4f20\u611f\u5668\u8ddd\u79bb (m)", None))
        self.materialLabel.setText(QCoreApplication.translate("MainWindow", u"\u7ba1\u6750", None))
        self.diameterLabel.setText(QCoreApplication.translate("MainWindow", u"\u7ba1\u5f84 (mm)", None))
        self.velocityLabel.setText(QCoreApplication.translate("MainWindow", u"\u58f0\u901f (m/s)", None))
        self.freqMaxLabel.setText(QCoreApplication.translate("MainWindow", u"\u6700\u5927\u9891\u7387 (Hz)", None))
        self.freqMinLabel.setText(QCoreApplication.translate("MainWindow", u"\u6700\u5c0f\u9891\u7387 (Hz)", None))
        self.parameterHint.setText(QCoreApplication.translate("MainWindow", u"\u91c7\u6837\u7387\u56fa\u5b9a 7500 Hz\uff1b\u58f0\u901f\u7531\u7ba1\u6750 + \u7ba1\u5f84\u533a\u95f4\u67e5\u8868\u81ea\u52a8\u586b\u5145\uff0c\u53ef\u624b\u52a8\u8986\u76d6\u3002", None))
        self.metricDisBLabel.setText(QCoreApplication.translate("MainWindow", u"\u8ddd\u4f20\u611f\u5668 B (m)", None))
        self.mDisB.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.metricSnrLabel.setText(QCoreApplication.translate("MainWindow", u"\u4fe1\u566a\u6bd4 SNR", None))
        self.mSnr.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.metricDisALabel.setText(QCoreApplication.translate("MainWindow", u"\u8ddd\u4f20\u611f\u5668 A (m)", None))
        self.mDisA.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.correlationTitle.setText(QCoreApplication.translate("MainWindow", u"\u5b9a\u4f4d\u66f2\u7ebf", None))
        self.correlationSubtitle.setText(QCoreApplication.translate("MainWindow", u"\u76f8\u5173\u7cfb\u6570 \u2014 \u8ddd A \u8ddd\u79bb\uff08\u672a\u6ee4\u6ce2 \u00b7 \u542b\u96f6\u586b\u5145\u53e3\u5f84\uff09", None))
        self.corrEmpty.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u5165\u6570\u636e\u5e76\u6267\u884c\u5b9a\u4f4d\u540e\u663e\u793a", None))
        self.corrLegendCoefficient.setText(QCoreApplication.translate("MainWindow", u"\u2501 |\u76f8\u5173\u7cfb\u6570|", None))
        self.corrLegendPeak.setText(QCoreApplication.translate("MainWindow", u"\u2501 \u5cf0\u503c\u4f4d\u7f6e \u2192 disA", None))
        self.signalTitle.setText(QCoreApplication.translate("MainWindow", u"\u4fe1\u53f7\u9884\u89c8", None))
        self.sigDur.setText("")
        self.signalTabs.setTabText(self.signalTabs.indexOf(self.waveTab), QCoreApplication.translate("MainWindow", u"\u65f6\u57df\u6ce2\u5f62", None))
        self.signalTabs.setTabText(self.signalTabs.indexOf(self.spectrumTab), QCoreApplication.translate("MainWindow", u"\u9891\u8c31", None))
        self.signalLegendA.setText(QCoreApplication.translate("MainWindow", u"\u2501 \u901a\u9053 A", None))
        self.signalLegendB.setText(QCoreApplication.translate("MainWindow", u"\u2501 \u901a\u9053 B", None))
        self.signalLegendRange.setText(QCoreApplication.translate("MainWindow", u"\u9891\u8c31\u663e\u793a 0 ~ 3000 Hz", None))
    # retranslateUi

