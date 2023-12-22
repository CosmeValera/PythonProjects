BUTTON_STYLES = """
    QPushButton {
        color: #F9F9F9;
        background-color: #DF0024;
        border-color: #DF0024;
    }

    QPushButton:hover {
        color: #FFFFFF;
        background-color: #FF0024;
        border-color: #FF0024;
    }
"""

COMBO_BOX_STYLES = """
    QComboBox {
        color: #99999999; /* Opacity are first 2 numbers */
        background-color: #191919;
        border-bottom: 1px solid #FFFFFF;
    }

    QComboBox::down-arrow {
        image: url("arrow.svg");
    }

    QComboBox QAbstractItemView {
        color: #F9F9F9;
        background-color: #252525;
        selection-background-color: #191919;
        border-color: #999999;
        padding: 4px;
        margin: 4px;
    }
"""

FILTER_STYLES = """
    QLineEdit {
        color: #FFFFFF;
        background-color: #191919;
        border-bottom: 1px solid #FFFFFF;
    }
    
    QToolTip {
        color: #999999;
        background-color: #191919;
        border: 1px solid #191919;
    }
"""

SIDEBAR_STYLES = """
    background-color: #191919;
"""

SIDEBAR_BUTTON_STYLES = """
    QPushButton {
        color: #F6F6F6;
        background-color: #191919;
        border: none;
    }
    QPushButton:hover {
        color: #FFFFFF;
        background-color: #252525;
        border: none;
    }
"""

SEPARATOR_STYLES = """
    background-color: #343434;
"""
