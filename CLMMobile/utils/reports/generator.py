from fpdf import FPDF 
from CLMMobile.utils.translation import Translation

class Generator:
    def __init__(self, trans: Translation, meeting_data: dict=None):
        self._trans: Translation = trans
        self._data: dict = meeting_data

    @property
    def report_data(self): self._data.copy()

    @report_data.setter 
    def report_data(self, new_data: dict):
        self._data = new_data if new_data is None else new_data.copy()
