scroll_style = """
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                width: 10px;
                background: #f0f0f0;
                border: none;
            }
            QScrollBar::handle:vertical {
                background: #c0c0c0;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: #a0a0a0;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """