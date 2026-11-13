import os
from fpdf import FPDF
from fpdf.enums import XPos, YPos, Align
from CLMMobile.utils.translation import Translation
from io import BytesIO


class Generator:

    FONT_FAMILY = "Helvetica"
    NORMAL_SIZE = 12
    SECTION_TITLE = 16
    TITLE = 20

    TALK_FILL_COLOR = (230, 230, 230)
    DEFAULT_TEXT_COLOR = (0, 0, 0)

    COLOR_TABLE = {
        "introduction": (100, 100, 100),
        "treasures from gods word": (52, 116, 128),
        "apply to ministry": (208, 132, 4),
        "living as christians": (183, 41, 20),
        "weekend": (20, 100, 200)
    }

    SECTION_RANGES = {
        "introduction": range(0, 1),
        "treasures from gods word": range(1, 4),
        "apply to ministry": range(4, 10),
        "living as christians": range(10, 13),
        "weekend": range(13, 15)
    }

    TALK_NAME_KEYS = {
        "introduction": ["INTRODUCTION"],
        "treasures from gods word": ["TREASURES TALK", "SPIRITUAL GEMS", "BIBLE READING"],
        "apply to ministry": ["STARTING A CONVERSATION", "FOLLOWING UP", "WHAT WOULD YOU SAY?", "MAKING DISCIPLES", "EXPLAINING YOUR BELIEFS", "TALK"],
        "living as christians": ["LIVING TALK", "CONGREGATION BIBLE STUDY", "CONCLUDING COMMENTS"],
        "weekend": ["PUBLIC TALK", "WATCHTOWER STUDY"]
    }

    def __init__(self, trans: Translation, meeting_data: dict = None):
        self._trans: Translation = trans
        self._data: dict = meeting_data or {}

        self._pdf: FPDF = FPDF(orientation="p", unit="mm", format="A4")

        self._meeting_codes: dict = self._trans.get_string_section("talks") or {}

    @property
    def report_data(self):
        return self._data.copy()

    @report_data.setter
    def report_data(self, new_data: dict):
        self._data = new_data if new_data is None else new_data.copy()

    def _section_for_talk_type(self, talk_type: int):
        for section, rng in self.SECTION_RANGES.items():
            if talk_type in rng:
                return section
        return None

    def _talk_name(self, talk_type: int, section: str) -> str:
        rng = self.SECTION_RANGES[section]
        index = talk_type - rng.start
        keys = self.TALK_NAME_KEYS.get(section, [])
        if index < 0 or index >= len(keys):
            return str(talk_type)
        return self._meeting_codes.get(keys[index], keys[index])

    def generate(self):
        self._pdf.add_page()

        self._pdf.set_font(self.FONT_FAMILY, size=self.TITLE, style="B")
        self._pdf.cell(
            0, 10,
            text=f"{self._meeting_codes.get('MEETING', 'Meeting')} {self._data.get('date', '')}",
            align=Align.L,
            new_x=XPos.LMARGIN,
            new_y=YPos.NEXT,
        )
        self._pdf.ln(3)

        current_section = None
        for talk in self._data.get("talks", []):
            talk_type = talk.get("talk_type")
            if talk_type is None:
                continue
            section = self._section_for_talk_type(talk_type)
            if section is None:
                continue
            if section != current_section:
                current_section = section
                self._render_section_title(
                    title=self._meeting_codes.get(section, section),
                    color=self.COLOR_TABLE[section]
                )
            self._render_talk(
                name=self._talk_name(talk_type, section),
                time=talk.get("measured_time", 0),
                limit=talk.get("time_limit", 0)
            )

    def _render_section_title(self, title: str, color: tuple):
        self._pdf.set_fill_color(*color)
        self._pdf.set_text_color(255, 255, 255)
        self._pdf.set_font(self.FONT_FAMILY, size=self.SECTION_TITLE, style="B")
        self._pdf.cell(
            0, 8,
            text=title,
            align=Align.L,
            fill=True,
            new_x=XPos.LMARGIN,
            new_y=YPos.NEXT,
        )
        self._pdf.ln(2)

    def _render_talk(self, name: str, time: int, limit: int):
        self._pdf.set_fill_color(*self.TALK_FILL_COLOR)
        self._pdf.set_text_color(*self.DEFAULT_TEXT_COLOR)
        self._pdf.set_font(self.FONT_FAMILY, size=self.NORMAL_SIZE)
        minutes, seconds = divmod(time, 60)
        self._pdf.cell(
            100, 6,
            text=f"{name} ({limit}:00)",
            align=Align.L,
            fill=True,
            new_x=XPos.RIGHT,
            new_y=YPos.TOP,
        )
        self._pdf.cell(
            0, 6,
            text=f"{minutes:02d}:{seconds:02d}",
            align=Align.R,
            fill=True,
            new_x=XPos.LMARGIN,
            new_y=YPos.NEXT,
        )
        self._pdf.ln(1)

    def save(self, location: str, name: str):
        self._pdf.output(os.path.join(location, name))

    def reset(self):
        self._pdf = FPDF(orientation="p", unit="mm", format="A4")
        self._meeting_codes = self._trans.get_string_section("talks") or {}

    def get_pdf_bytes(self):
        pdf_bytes = BytesIO(self._pdf.output())
        pdf_bytes.seek(0)
        return pdf_bytes
