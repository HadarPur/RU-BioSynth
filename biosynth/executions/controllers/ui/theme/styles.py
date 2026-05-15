"""QSS stylesheet factories.

All Qt style strings used by the GUI live here. Each helper returns the QSS
string from values defined in `tokens.py`, so changing a token there
propagates everywhere automatically.
"""

from biosynth.executions.controllers.ui.theme.tokens import COLORS, FONTS, SIZES


def global_app_qss() -> str:
    """Application-wide QSS applied via QApplication.setStyleSheet()."""
    return f"""
        pre {{
            font-size: {FONTS.body_px}px;
            line-height: 20px;
            max-width: 90%;
            margin-right: auto;
            overflow-wrap: break-word;
        }}

        p {{
            font-size: {FONTS.body_px}px;
            line-height: {FONTS.body_line_height_px}px;
            padding: {FONTS.body_padding_px}px;
        }}

        QCheckBox {{
            font-size: {FONTS.body_px}px;
            line-height: {FONTS.body_line_height_px}px;
            padding: {FONTS.body_padding_px}px;
        }}

        QLabel {{
            font-size: {FONTS.body_px}px;
            line-height: {FONTS.body_line_height_px}px;
            padding: {FONTS.body_padding_px}px;
            color: #333;
        }}

        QLineEdit, QComboBox {{
            background-color: white;
            border: 1px solid {COLORS.surface_border};
            border-radius: 6px;
            padding: 4px 8px;
            font-size: {FONTS.body_px}px;
            selection-background-color: {COLORS.table_selection_bg};
            selection-color: {COLORS.table_selection_text};
        }}

        QLineEdit:focus, QComboBox:focus {{
            border-color: {COLORS.primary};
        }}

        QTextEdit, QTextBrowser {{
            font-size: {FONTS.body_px}px;
            line-height: {FONTS.body_line_height_px}px;
            padding: {FONTS.body_padding_px}px;
            background-color: white;
            border: 1px solid {COLORS.surface_border};
            border-radius: 8px;
            selection-background-color: {COLORS.table_selection_bg};
            selection-color: {COLORS.table_selection_text};
        }}

        QScrollArea {{
            border: none;
            background: {COLORS.scroll_area_bg};
        }}

        QScrollBar:vertical {{
            border: none;
            background: {COLORS.scrollbar_track};
            width: 4px;
            margin: 4px 0;
            border-radius: 2px;
        }}

        QScrollBar::handle:vertical {{
            background: {COLORS.scrollbar_handle};
            min-height: {SIZES.scrollbar_handle_min}px;
            border-radius: 2px;
        }}

        QScrollBar::handle:vertical:hover {{
            background: {COLORS.scrollbar_handle_hover};
        }}

        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}

        QScrollBar:horizontal {{
            border: none;
            background: {COLORS.scrollbar_track};
            height: 4px;
            margin: 0 4px;
            border-radius: 2px;
        }}

        QScrollBar::handle:horizontal {{
            background: {COLORS.scrollbar_handle};
            min-width: {SIZES.scrollbar_handle_min}px;
            border-radius: 2px;
        }}

        QScrollBar::handle:horizontal:hover {{
            background: {COLORS.scrollbar_handle_hover};
        }}

        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            width: 0px;
        }}
    """


def transparent_text_edit_qss(with_border: bool = True, border_color: str = None,
                              padding_px: int = None, margin_right_px: int = 25) -> str:
    """QTextEdit/QTextBrowser with transparent background and an optional border."""
    border_color = border_color or COLORS.border_light
    border = f"1px solid {border_color}" if with_border else "transparent"
    padding_rule = f"padding: {padding_px}px;" if padding_px is not None else ""
    margin_rule = f"margin-right: {margin_right_px}px;" if margin_right_px else ""
    return f"""
        QTextEdit, QTextBrowser {{
            background-color: transparent;
            border: {border};
            {padding_rule}
            {margin_rule}
        }}
    """


def text_edit_transparent_only_qss() -> str:
    """QTextEdit with just a transparent background — no border, no padding."""
    return """
        QTextEdit {
            background-color: transparent;
        }
    """


def card_text_edit_qss(margin_right_px: int = 0) -> str:
    """QTextEdit/QTextBrowser/QPlainTextEdit styled to match the table card
    look — white background, light border, 10px radius. Used for "panel"
    style text boxes so they match the adjacent tables.
    """
    margin_rule = f"margin-right: {margin_right_px}px;" if margin_right_px else ""
    return f"""
        QTextEdit, QTextBrowser, QPlainTextEdit {{
            background-color: {COLORS.table_bg};
            border: 1px solid {COLORS.table_border};
            border-radius: 10px;
            padding: 6px 10px;
            {margin_rule}
        }}
    """


def circular_button_qss() -> str:
    """Round QPushButton styled as the muted info-glyph button."""
    return f"""
        QPushButton {{
            border: 2px solid transparent;
            border-radius: {SIZES.circular_btn_radius};
            background-color: {COLORS.circular_button_bg};
            color: {COLORS.circular_button_text};
            font-size: {FONTS.info_button_px}px;
            outline: none;
        }}
        QPushButton:hover {{
            background-color: {COLORS.circular_button_hover};
        }}
        QPushButton:pressed {{
            background-color: {COLORS.circular_button_pressed};
        }}
    """


def floating_indicator_qss() -> str:
    """Pill-shaped QPushButton used as the floating scroll-to-bottom chip."""
    return f"""
        QPushButton {{
            background-color: {COLORS.floating_indicator_bg};
            border: 1px solid {COLORS.floating_indicator_border};
            color: {COLORS.floating_indicator_text};
            border-radius: {SIZES.floating_indicator_radius}px;
            font-weight: bold;
        }}
    """


def info_dialog_text_qss() -> str:
    """QTextEdit inside the info dialog — card-style HTML help text."""
    return f"""
        QTextEdit {{
            background-color: {COLORS.table_bg};
            border: 1px solid {COLORS.table_border};
            border-radius: 10px;
            font-size: {FONTS.body_px}px;
            line-height: {FONTS.body_line_height_px}px;
            padding: 8px 12px;
        }}
    """


def info_dialog_tabs_qss() -> str:
    """QTabWidget/QTabBar styled as borderless tabs with a primary underline."""
    return f"""
        QTabWidget::pane {{
            border: none;
            background: transparent;
            top: -1px;
        }}

        QTabBar::tab {{
            background: transparent;
            color: {COLORS.table_text};
            padding: 4px 10px;
            min-height: 18px;
            min-width: 200px;
            border: none;
            border-bottom: 2px solid transparent;
            font-size: {FONTS.body_px}px;
        }}

        QTabBar::tab:selected {{
            color: {COLORS.table_header_text};
            border-bottom: 2px solid {COLORS.primary};
            font-weight: 600;
        }}

        QTabBar::tab:hover:!selected {{
            color: {COLORS.primary_hover};
        }}
    """


def status_label_qss() -> str:
    """Floating QLabel used to show transient status/toast messages."""
    return f"""
        QLabel {{
            color: {COLORS.status_text};
            background-color: transparent;
            border: transparent;
            border-radius: 5px;
            padding: 10px {SIZES.status_label_padding}px;
            font-size: {FONTS.status_px}px;
        }}
    """


def placeholder_label_qss() -> str:
    """Inline QLabel style for empty-state placeholder text inside tables."""
    return f"color: {COLORS.placeholder_text}; font-size: {FONTS.placeholder_px}px;"


def scroll_area_borderless_qss() -> str:
    """QScrollArea with no frame border, for embedding inside cards."""
    return "QScrollArea { border: none; }"


def table_qss() -> str:
    """QTableWidget styled to match the HTML report's pattern-table look."""
    return f"""
        QTableWidget {{
            background-color: {COLORS.table_bg};
            alternate-background-color: {COLORS.table_alt_row};
            border: 1px solid {COLORS.table_border};
            border-radius: 10px;
            padding: 4px;
            color: {COLORS.table_text};
            font-size: {FONTS.table_px}px;
            selection-background-color: {COLORS.table_selection_bg};
            selection-color: {COLORS.table_selection_text};
        }}

        QTableWidget::item {{
            padding-left: 10px;
            padding-right: 10px;
            border-bottom: 1px solid {COLORS.table_item_border};
        }}

        QTableWidget::item:selected {{
            background-color: {COLORS.table_selection_item_bg};
            color: {COLORS.table_selection_text};
        }}

        QHeaderView {{
            border: none;
        }}

        QHeaderView::section {{
            background-color: {COLORS.table_header_bg};
            color: {COLORS.table_header_text};
            border: none;
            border-bottom: 2px solid {COLORS.table_header_bottom_border};
            padding: 10px;
            font-weight: 600;
            font-size: {FONTS.table_px}px;
        }}

        QScrollBar:vertical {{
            border: none;
            background: {COLORS.scrollbar_track};
            width: 4px;
            margin: 4px 0;
            border-radius: 2px;
        }}

        QScrollBar::handle:vertical {{
            background: {COLORS.scrollbar_handle};
            min-height: {SIZES.scrollbar_handle_min}px;
            border-radius: 2px;
        }}

        QScrollBar::handle:vertical:hover {{
            background: {COLORS.scrollbar_handle_hover};
        }}

        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {{
            height: 0px;
        }}

        QScrollBar:horizontal {{
            background: transparent;
            height: 10px;
            margin: 0 4px;
        }}

        QScrollBar::handle:horizontal {{
            background: {COLORS.scrollbar_handle};
            min-width: {SIZES.scrollbar_handle_min}px;
            border-radius: 2px;
        }}

        QScrollBar::handle:horizontal:hover {{
            background: {COLORS.scrollbar_handle_hover};
        }}

        QScrollBar::add-line:horizontal,
        QScrollBar::sub-line:horizontal {{
            width: 0px;
        }}
    """
