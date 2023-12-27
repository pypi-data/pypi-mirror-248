# Licensed under the GPLv3 License: https://www.gnu.org/licenses/gpl-3.0.html
# For details: https://github.com/muziing/Py2exe-GUI/blob/main/README.md#license

from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices, QIcon, QPixmap
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QMenuBar, QStatusBar

from ..Constants import PLATFORM, RUNTIME_INFO, APP_URLs, AppConstant
from .center_widget import CenterWidget, WinMacCenterWidget
from .dialog_widgets import AboutDlg
from .pyinstaller_option_widget import PyinstallerOptionTable


def open_url(url: str) -> None:
    """
    辅助函数，在系统默认浏览器中打开URL \n
    :param url: 待打开的URL
    """

    QDesktopServices.openUrl(QUrl(url))


class MainWindow(QMainWindow):
    """
    主界面主窗口
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.center_widget: CenterWidget
        if RUNTIME_INFO.platform in (PLATFORM.windows, PLATFORM.macos):
            self.center_widget = WinMacCenterWidget(self)
        else:
            self.center_widget = CenterWidget(self)

        self.menu_bar = QMenuBar(self)
        self.status_bar = QStatusBar(self)
        self.pyinstaller_option_table = PyinstallerOptionTable()

        self.setCentralWidget(self.center_widget)
        self.setMenuBar(self.menu_bar)
        self.setStatusBar(self.status_bar)

        self._setup()

    def _setup(self) -> None:
        """
        设置主窗口 \n
        """

        self.setWindowTitle("Py2exe-GUI")
        self.setMinimumSize(350, 430)
        # self.resize(800, 600)
        self.setWindowIcon(QIcon(QPixmap(":/Icons/Py2exe-GUI_icon_72px")))

        self._setup_menu_bar()
        self._setup_status_bar()

    def _setup_menu_bar(self) -> None:
        """
        配置主窗口菜单栏 \n
        """

        file_menu = self.menu_bar.addMenu("文件(&F)")
        file_menu.addAction("打开打包任务")  # 暂时只为占位
        file_menu.addAction("保存当前打包任务")  # 暂时只为占位
        file_menu.addSeparator()
        file_menu.addAction("设置")  # 暂时只为占位
        file_menu.addSeparator()
        file_menu.addAction("退出(&X)", self.close)

        help_menu = self.menu_bar.addMenu("帮助(&H)")

        help_menu.addAction(
            "PyInstaller官方文档",
            lambda: open_url(APP_URLs["Pyinstaller_doc"]),
        )
        help_menu.addAction("PyInstaller选项详情", self.pyinstaller_option_table.show)
        help_menu.addSeparator()
        help_menu.addAction("报告Bug", lambda: open_url(APP_URLs["BugTracker"]))

        about_menu = self.menu_bar.addMenu("关于(&A)")
        about_menu.addAction("关于本程序", AboutDlg(self).exec)
        about_menu.addAction("关于 &Qt", QApplication.aboutQt)

    def _setup_status_bar(self) -> None:
        """
        配置主窗口状态栏 \n
        """

        # 在最右侧固定显示版本信息
        version_label = QLabel("V" + AppConstant.VERSION, self.status_bar)
        self.status_bar.insertPermanentWidget(0, version_label)
