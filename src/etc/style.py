COLOR_BACKGROUND    = "rgba(0,0,0,200)"
COLOR_SYSTEM        = "#FF0000"
COLOR_HEADER        = "#00FF00"
COLOR_NORMAL        = "#000000"
COLOR_TEXT          = "#DDDDDD"
COLOR_VALUE         = "#3399FF"
COLOR_EXTRA         = "#FFFF00"
COLOR_INNER         = "#00DD00"
COLOR_OUTTER        = "#DD5500"
COLOR_BUTTON        = "#008800"

COLOR_WHITE         = "#FFFFFF"
COLOR_RED           = "#FF0000"
COLOR_GREEN         = "#00FF00"
COLOR_BLUE          = "#0000FF"
COLOR_BLACK         = "#000000"

COLOR_DARK_GREEN    = "#006600"
COLOR_DARK_RED      = "#990000"
COLOR_DARK_GREY     = "#555555"
COLOR_BRIGHT_BLUE   = "#0099FF"

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
                            border-bottom: 1px solid """ + COLOR_VALUE + """;
                            background: rgba(0,0,0,0);
                        }
                        QTabBar::tab
                        {
                            height: 15px;
                            min-width: 20px;
                            padding: 0px 3px 0px 3px;
                            margin: 0px 1px 0px 1px;
                            border-bottom: 1px solid """ + COLOR_VALUE + """;
                            border-top-left-radius: 2px;
                            border-top-right-radius: 2px;
                            color: """ + COLOR_TEXT + """;
                            background: rgba(51,153,255,100);
                        }
                        QTabBar::tab:selected
                        {
                            border-bottom: 1px solid """ + COLOR_INNER + """;
                            color: """ + COLOR_TEXT + """;
                            background: rgba(0,221,0,100);
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