from fpdf import FPDF

class Generator:
    FONT_FAMILY = "Helvetica"
    NORMAL_SIZE = 12
    SECTION_SIZE = 16
    TITLE_SIZE = 20

    TALK_FILL_COLOR = (230, 230, 230)
    DEFAULT_TEXT_COLOR = (0, 0, 0)

    def __init__(self, meeting_data: dict):
        """
        Meeting data must have the following format:
            - pre-talks: [
                        {name: str, time_limit: int -> minutes, time_used: int -> seconds}
                ]
            - meeting-parts: [{
                "name": str, -> used for the title text content
                "color": str, -> is used for the title color
                "talks": [
                    {"name": str, time_limit: int -> in minutes, time_used: int -> in seconds},
                    ...
                ]
            }]
        """
        self._data: dict = meeting_data

        self.pdf: FPDF = FPDF(orientation="P", unit="mm", format="A4")

    def generate(self):
        self.pdf.add_page()
        self.pdf.set_font(self.FONT_FAMILY, size=self.TITLE_SIZE, style="B")

        # generate the meeting header
        self.pdf.cell(0, 10, text=f"Meeting {self._data["date"]}", new_x="LMARGIN", new_y="NEXT", align="L")
        self.pdf.ln(3)
        # generate pre-talks
        self._render_talk_items(talks=self._data["pre-talks"])
        # generate stuff for meeting parts
        for part in self._data["meeting-parts"]:
            self._gen_meeting_part(part)

    def _gen_meeting_part(self, part: dict):
        self.pdf.ln(3)
        # generate the title
        self.pdf.set_fill_color(part["color"])
        self.pdf.set_text_color(255, 255, 255)
        self.pdf.cell(0, 7, text=part["name"], new_x="LMARGIN", new_y="NEXT", align="L", fill=True) 
        self.pdf.ln(3)
        # generate the items
        self._render_talk_items(talks=part["talks"])

    def _render_talk_items(self, talks: dict):
        for talk in talks:
            self._render_talk(name=talk["name"], time_used=talk["time_used"], time_limit=talk["time_limit"])

    def _render_talk(self, name: str, time_used: int, time_limit: int):
        self.pdf.set_fill_color(self.TALK_FILL_COLOR)
        self.pdf.set_text_color(self.DEFAULT_TEXT_COLOR)
        self.pdf.set_font(self.FONT_FAMILY, size=self.NORMAL_SIZE)
        self.pdf.cell(0, 6, text=f"{name} ({time_limit}:00)", align="L", fill=True)
        self.pdf.cell(0, 6, text=f"{time_used // 60}:{time_used % 60}", align="R", new_x="LMARGIN", new_y="NEXT", fill=True)
        self.pdf.ln(1)
        
    def save(self, location: str, name: str):
        self.pdf.output(f"{location}/{name}")


if __name__ == "__main__":
    import os
    dummy_data = {
        "date": "24/10/2026",
        "pre-talks": [
            {"name": "Intro", "time_limit": 1, "time_used": 40}
        ],
        "meeting-parts": [
            {"name": "Treasures", "color": (80, 180, 200), "talks": [
                {"name": "Talk", "time_limit": 10, "time_used": 23},
                {"name": "Treasures", "time_limit": 10, "time_used": 100},
                {"name": "Bible Reading", "time_limit": 4, "time_used": 140}
            ]},

            {"name": "Apply yourself to the field ministry", "color": (200, 110, 20), "talks": [
                {"name": "Talk - 1", "time_limit": 2, "time_used": 100}
            ]}
        ]
    }

    gen = Generator(dummy_data)
    gen.generate()
    gen.save(location=os.getenv("LOCATION"), name="test.pdf")
 