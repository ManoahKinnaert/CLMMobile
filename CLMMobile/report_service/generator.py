from fpdf import FPDF
from io import BytesIO
from CLMMobile.translation_service import TranslationService
from CLMMobile.schedule_service.schedule_service import TalkType

class Generator:
    FONT_FAMILY = "Helvetica"
    NORMAL_SIZE = 12
    SECTION_SIZE = 16
    TITLE_SIZE = 20

    TALK_FILL_COLOR = (230, 230, 230)
    DEFAULT_TEXT_COLOR = (0, 0, 0)

    COLOR_TABLE = {
        "INTRO": None,
        "TREASURES_FROM_GODS_WORD": (52, 116, 128),
        "APPLY_YOURSELF_TO_THE_FIELD_MINISTRY": (208, 132, 4),
        "LIVING_AS_CHRISTIANS": (183, 41, 20)
    }

    def __init__(self, trans: TranslationService, meeting_data: dict | None=None):
        self._data: dict | None = meeting_data
        self._trans = trans
        self.trans_sections = trans.get_meeting_section_codes()
        self.trans_talks = trans.get_meeting_codes()

        self.pdf: FPDF = FPDF(orientation="P", unit="mm", format="A4")

    @property
    def report_data(self): return self._data.copy()

    @report_data.setter 
    def report_data(self, new_data: dict | None):
        self._data = new_data if new_data is None else new_data.copy()
    
    def generate(self):
        self.pdf.add_page()
        self.pdf.set_font(self.FONT_FAMILY, size=self.TITLE_SIZE, style="B")

        # generate the meeting header
        self.pdf.cell(0, 10, text=f"{self.trans_talks["MEETING"]} {self._data["date"]}", new_x="LMARGIN", new_y="NEXT", align="L")
        self.pdf.ln(3)
        # generate stuff for meeting section
        keys = list(self.COLOR_TABLE.keys())
        for part in self._data["meeting-sections"]:
            self._gen_meeting_section(key=keys[part[0]["meeting_section"]], data=part)

    def _gen_meeting_section(self, key: str, data: dict):
        self.pdf.ln(3)
        # generate the title
        if self.COLOR_TABLE[key] is not None:
            self.pdf.set_fill_color(self.COLOR_TABLE[key])
            self.pdf.set_text_color(255, 255, 255)
            self.pdf.cell(0, 7, text=self.trans_sections[key], new_x="LMARGIN", new_y="NEXT", align="L", fill=True) 
            self.pdf.ln(3)
        # generate the items
        self._render_talk_items(talks=data)

    def _render_talk_items(self, talks: list):
        for talk in talks:
            self._render_talk(name=f"{self.trans_talks[TalkType(talk["talk_type"]).name]} {talk["sequence_number"] if talk["sequence_number"] > 0 else ""}", time_used=talk["measured_time"], time_limit=talk["time_limit"])

    def _render_talk(self, name: str, time_used: int, time_limit: int):
        self.pdf.set_fill_color(self.TALK_FILL_COLOR)
        self.pdf.set_text_color(self.DEFAULT_TEXT_COLOR)
        self.pdf.set_font(self.FONT_FAMILY, size=self.NORMAL_SIZE)
        self.pdf.cell(0, 6, text=f"{name} ({time_limit}:00)", align="L", fill=True)
        self.pdf.cell(0, 6, text=f"{time_used // 60}:{time_used % 60}", align="R", new_x="LMARGIN", new_y="NEXT", fill=True)
        self.pdf.ln(1)
        
    def save(self, location: str, name: str):
        self.pdf.output(f"{location}/{name}")

    def reset(self):
        self.pdf = FPDF(orientation="P", unit="mm", format="A4")
        self.report_data = None
        self.trans_sections = self._trans.get_meeting_section_codes()
        self.trans_talks = self._trans.get_meeting_codes()

    def get_pdf_bytes(self):
        pdf_bytes = BytesIO(self.pdf.output())
        pdf_bytes.seek(0)
        return pdf_bytes