from .text import text_normal

menu_style = """
    QComboBox {"
        padding: 5px;
        font-size: 14px;
        border: 1px solid #ccc;
        border-radius: 6px;
        background-color: #ffffff;
    "}

    QComboBox::drop-down {
        border: none;
    }

    /* Elimina esta sección si quieres la flecha del sistema:
    QComboBox::down-arrow {
        image: url(assets/arrow_down.png);
        width: 12px;
        height: 12px;
    }
    */

    QComboBox QAbstractItemView {
        background-color: #ffffff;
        border: 1px solid #ccc;
        border-radius: 6px;
        outline: 0;
    }

    QComboBox QAbstractItemView::item {
        padding: 6px 10px;
    }

    QComboBox QAbstractItemView::item:hover {
        background-color: #eaeaea;
        color: #666666;  /* texto gris al hacer hover */
    }

    QComboBox QAbstractItemView::item:selected {
        background-color: #d0d0d0;
        color: #666666;
    }
"""
