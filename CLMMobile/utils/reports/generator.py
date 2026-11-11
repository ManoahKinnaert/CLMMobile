from fpdf import FPDF 
from CLMMobile.utils.translation import Translation
from io import BytesIO

class Generator:

    FONT_FAMILY = "Helvetica"
    NORMAL_SIZE = 12
    SECTION_TITLE = 16
    TITLE = 20

    COLOR_TABLE = {
        "treasures from gods word": (52, 116, 128),
        "apply to ministry": (208, 132, 4),
        "living as christians": (183, 41, 20),
        "weekend": (20, 100, 200)
    }

    def __init__(self, trans: Translation, meeting_data: dict=None):
        self._trans: Translation = trans
        self._data: dict = meeting_data

        self._pdf: FPDF = FPDF(orientation="p", unit="mm", format="A4")

        self._meeting_codes: dict = self._trans.get_string_section("talks")

    @property
    def report_data(self): self._data.copy()

    @report_data.setter 
    def report_data(self, new_data: dict):
        self._data = new_data if new_data is None else new_data.copy()

    def generate(self):
        self._pdf.add_page()
        
        self.pdf.set_font(self.FONT_FAMILY, size=self.TITLE, style="B")
        self._pdf.cell(0, 10, text=f"{self._meeting_codes["MEETING"]} {self._data["date"]}", new_x="LMARGIN", new_y="NEXT", align="L")
        self._pdf.ln(3)
        # generate meeting sections

    def _gen_meeting_section(self, key: str, data: dict):
        pass 

    def _render_talk_items(self, talks: list):
        pass 

    def _render_talk(self, name: str, time: int, limit: int):
        pass 

    def save(self, location: str, name: str):
        pass 

    def reset(self):
        self._pdf = FPDF(orientation="p", unit="mm", format="A4")
        self._meeting_codes = self._trans.get_string_section("talks")

    def get_pdf_bytes(self):
        pdf_bytes = BytesIO(self._pdf.output())
        pdf_bytes.seek(0)
        return pdf_bytes