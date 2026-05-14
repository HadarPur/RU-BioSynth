"""Design tokens for the BioSynth GUI.

Single source of truth for colors, fonts, sizes, margins, and labels used
across the PyQt5 wizard. Edit values here to retheme the app — no need to
hunt through individual window files.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Colors:
    # Report-derived palette (primary blue / surfaces / accents)
    primary: str = "#245076"
    primary_hover: str = "#2c618f"
    primary_pressed: str = "#1a3b58"
    surface_alt: str = "#fafafa"
    surface_border: str = "#ddd"

    # Toggle switch
    toggle_on: str = "#245076"
    toggle_off: str = "#ccc"
    toggle_knob: str = "#fff"

    # Circular info button
    circular_button_bg: str = "#888"
    circular_button_hover: str = "#aaa"
    circular_button_pressed: str = "#555"
    circular_button_text: str = "white"

    # Floating scroll indicator
    floating_indicator_bg: str = "gray"
    floating_indicator_border: str = "lightgray"
    floating_indicator_text: str = "white"

    # Generic borders and placeholders
    border_light: str = "#ddd"
    border_medium: str = "#245076"
    placeholder_text: str = "#888"

    # Status label
    status_text: str = "#000000"

    # Table palette (matches the report's pattern-table look)
    table_bg: str = "#ffffff"
    table_alt_row: str = "#fafafa"
    table_border: str = "#ccc"
    table_text: str = "#333333"
    table_item_border: str = "#ddd"
    table_selection_bg: str = "#cfe3ff"
    table_selection_item_bg: str = "#dbe9ff"
    table_selection_text: str = "#000000"
    table_header_bg: str = "#ffffff"
    table_header_text: str = "#000000"
    table_header_bottom_border: str = "#245076"

    # Scrollbar (report uses a pill-shaped #245076 handle on a light track)
    scrollbar_handle: str = "#245076"
    scrollbar_handle_hover: str = "#1a3b58"
    scrollbar_track: str = "#e8e8e8"

    # Scroll area background (global app stylesheet)
    scroll_area_bg: str = "white"


@dataclass(frozen=True)
class Fonts:
    """Single-source-of-truth font sizing.

    Every non-header text element in the UI — labels, buttons, text edits,
    table rows, status pill, placeholder text, info button, monospace code
    blocks — derives its size from :attr:`body_px`. Change ``body_px``
    here and the whole UI rescales uniformly.

    Headers (``<h1>`` / ``<h2>`` / ``<h3>`` inside ``QLabel``) keep their
    own Qt-rendered sizes and are not affected.
    """

    code_family: str = "Menlo"

    body_px: int = 15
    body_line_height_px: int = 5
    body_padding_px: int = 2

    # The following are read-only aliases of ``body_px`` so existing call
    # sites that reference table/status/placeholder/info/code sizes all
    # render at the same size. Aliasing (rather than duplicating values)
    # keeps "all UI text the same size" a true invariant of the theme.
    @property
    def table_px(self) -> int:
        return self.body_px

    @property
    def status_px(self) -> int:
        return self.body_px

    @property
    def placeholder_px(self) -> int:
        return self.body_px

    @property
    def info_button_px(self) -> int:
        return self.body_px

    @property
    def code_px(self) -> int:
        return self.body_px


@dataclass(frozen=True)
class Sizes:
    # Main window
    window_width: int = 1000
    window_height: int = 950
    window_x: int = 100
    window_y: int = 100

    # Logo
    logo_w: int = 110
    logo_h: int = 110

    # Toggles / spinboxes / buttons
    toggle_w: int = 50
    toggle_h: int = 25
    spinbox_w: int = 80
    spinbox_h: int = 30
    button_w: int = 60
    button_h: int = 30
    button_medium_w: int = 100
    button_medium_h: int = 30
    button_large_w: int = 120
    button_xlarge_w: int = 200

    # Info / circular buttons
    circular_btn: int = 20
    circular_btn_radius: int = 10
    floating_indicator: int = 20
    floating_indicator_radius: int = 10
    floating_indicator_margin_bottom: int = 80

    # Scroll / text areas
    scroll_area_height: int = 550
    sequence_height: int = 200
    sequence_diff_height: int = 150
    scroll_area_max_inline: int = 150
    scroll_padding: int = 10

    # Status label
    status_label_width: int = 890
    status_label_padding: int = 15
    status_label_bottom_margin: int = 15
    status_label_left_margin: int = 20

    # Info dialog
    info_dialog_w: int = 1000
    info_dialog_h_short: int = 400
    info_dialog_h_tall: int = 500

    # Busy dialog
    busy_dialog_w: int = 360
    busy_dialog_h: int = 120

    # Report preview window (pywebview)
    preview_w: int = 1200
    preview_h: int = 800

    # Table header / rows
    table_header_min_h: int = 38
    table_row_default_h: int = 34

    # Scrollbar
    scrollbar_thin: int = 2
    scrollbar_thick: int = 6
    scrollbar_handle_min: int = 20

    # Animation durations (ms)
    toggle_anim_ms: int = 200
    fade_anim_ms: int = 300
    scroll_anim_ms: int = 500
    status_visible_ms: int = 5000


@dataclass(frozen=True)
class Margins:
    """(left, top, right, bottom) tuples."""

    page_padded: tuple = (20, 20, 20, 20)
    page_top_bottom: tuple = (20, 5, 20, 20)
    page_middle: tuple = (20, 10, 20, 10)
    page_top_compact: tuple = (20, 20, 20, 5)
    frame_padding: tuple = (5, 5, 5, 5)
    spinbox_row: tuple = (0, 5, 0, 10)


@dataclass(frozen=True)
class Labels:
    back: str = "Back"
    next: str = "Next"
    reset: str = "Reset"
    done: str = "Done"
    download: str = "Download"
    save_as: str = "Save as"
    copy: str = "Copy"
    show_preview: str = "Show Preview"
    info_glyph: str = "ⓘ"
    indicator_glyph: str = "▼"

    load_target_sequence: str = "Load Target Sequence"
    load_patterns: str = "Load Patterns"
    load_codon_usage: str = "Load Codon Usage"

    placeholder_target_sequence: str = (
        "Upload Target Sequence/Drag&Drop Target Sequence file (.txt)"
    )
    placeholder_patterns: str = "Upload Patterns file/Drag&Drop Patterns file (.txt)"
    placeholder_codon_usage: str = (
        "Upload Codon Usage file/Drag&Drop Codon Usage file (.txt)"
    )
    codon_columns: tuple = ("Codon", "Frequency")

    spin_alpha: str = "Transition substitution cost"
    spin_beta: str = "Transversion substitution cost"
    spin_w: str = "Non-synonymous substitution cost"
    toggle_optimized_codon: str = "Enable codon optimization"

    report_available: str = "Elimination report is now available"
    tab_coding_region: str = "Coding Region Criteria"
    tab_substitution_costs: str = "Substitution Costs"
    tab_cost_contribution: str = "Cost Contribution"
    tab_cost_substitution: str = "Cost Substitution"

    busy_message: str = "Computation in progress.\nThis may take a few moments for long sequences."
    elimination_failed: str = "Elimination failed"


@dataclass(frozen=True)
class Titles:
    app: str = "🧬 BioSynth App"
    info_dialog: str = "Information"
    results_info_dialog: str = "Cost Information"
    preview_window: str = "Preview Report"
    busy_dialog: str = "Please wait"


# Module-level singletons — import these instead of instantiating.
COLORS = Colors()
FONTS = Fonts()
SIZES = Sizes()
MARGINS = Margins()
LABELS = Labels()
TITLES = Titles()
