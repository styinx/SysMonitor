from etc.settings import *

TRANSPARENT			= "rgba(0, 0, 0, 0)"

COLOR_BACKGROUND    = SETTINGS.get("Colors", "background")
COLOR_SYSTEM        = SETTINGS.get("Colors", "system")
COLOR_HEADER        = SETTINGS.get("Colors", "header")
COLOR_TEXT          = SETTINGS.get("Colors", "text")
COLOR_VALUE         = SETTINGS.get("Colors", "value")
COLOR_BUTTON        = SETTINGS.get("Colors", "button")
COLOR_EXTRA         = SETTINGS.get("Colors", "extra")
COLOR_INNER         = SETTINGS.get("Colors", "inner")
COLOR_OUTTER        = SETTINGS.get("Colors", "outter")
COLOR_TAB           = SETTINGS.get("Colors", "tab")
COLOR_TAB_ACTIVE    = SETTINGS.get("Colors", "tab_active")

STYLE_BACKGROUND  = """background: """ + COLOR_BACKGROUND + """;"""

STYLE_PROGRESSBAR = """ QProgressBar:horizontal
                        {
                            height: 10px;
							width: 100px;
                            border: 2px solid """ + COLOR_OUTTER + """;
                            border-radius: 2px;
                            background: rgba(0,0,0,0);
                        }
                        QProgressBar::chunk:horizontal
                        {
                            background: """ + COLOR_INNER + """;
                        } """

STYLE_FRAME       = """ QFrame
                        {
                            color: """ + COLOR_TEXT + """;
                            background: rgba(0,0,0,0);
                        }
                        QLabel
                        {
                            max-width: 180px;
                        } """

STYLE_WIDGET      = """ QWidget
                        {
                            color: """ + COLOR_TEXT + """;
                            background: rgba(0,0,0,0);
                        } """

STYLE_TABWIDGET   = """ QTabWidget
                        {
                            max-height: 165px;
                            padding: 0px;
                            margin: 0px;
                            border: none;
                            background: rgba(0,0,0,0);
                        }
                        QTabWidget::pane
                        {
                            max-height: 150px;
                            border: none;
                            background: rgba(0,0,0,0);
                        }
                        QTabBar
                        {
                            border-bottom: 1px solid """ + TRANSPARENT + """;
                            background: """ + TRANSPARENT + """;
                        }
                        QTabBar::tab
                        {
                            height: 15px;
                            min-width: 20px;
                            padding: 0px 3px 0px 3px;
                            margin: 0px 1px 0px 1px;
                            border-bottom: 1px solid """ + COLOR_TAB_ACTIVE + """;
                            border-top-left-radius: 2px;
                            border-top-right-radius: 2px;
                            color: """ + COLOR_TEXT + """;
                            background: """ + COLOR_TAB + """;
                        }
                        QTabBar::tab:selected
                        {
                            border-bottom: 1px solid """ + COLOR_TAB + """;
                            color: """ + COLOR_TEXT + """;
                            background: """ + COLOR_TAB_ACTIVE + """;
                        }

                        QTabBar QToolButton::left-arrow, QToolButton::right-arrow
                        {
                            color: red;
                        } """

STYLE_BUTTON      = """ QPushButton, QPushButton:disabled, QPushButton:hover
                        {
							width: 150px;
                            font-weight: bold;
                            border: 2px solid """ + COLOR_BUTTON + """;
                            border-radius: 2px;
                            padding: 2px 2px 2px 2px;
                            color: """ + COLOR_TEXT + """;
                            background: rgba(0,0,0,0);
                        }
                        QPushButton:on
                        {
                            border: 2px solid """ + COLOR_HEADER + """;
                            color: """ + COLOR_SYSTEM + """;
                        } """

STYLE_ALL = STYLE_BUTTON + STYLE_PROGRESSBAR + STYLE_TABWIDGET + STYLE_FRAME + STYLE_WIDGET