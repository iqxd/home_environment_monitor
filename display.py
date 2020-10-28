import ssd1306
import machine
import time


class Display:
    def __init__(self, dc, res, cs, width, height, border=0):
        self.w = width
        self.h = height
        self.b = border
        spi = machine.SPI(1, baudrate=8000000, polarity=0, phase=0)
        self._screen = ssd1306.SSD1306_SPI(width, height, spi, dc, res, cs)

    def _clear(self):
        self._screen.fill(0)

    def _fill_all(self):
        self._screen.fill(1)

    def _fill_border(self):
        func_fill = self._screen.fill_rect
        func_fill(0, 0, self.w, self.b, 1)
        func_fill(0, self.h - self.b, self.w, self.b, 1)
        func_fill(0, 0, self.b, self.h, 1)
        func_fill(self.w - self.b, 0, self.b, self.h, 1)

    def _fill_linetext(self, litext, lino, nline):
        nchar = len(litext)
        assert (self.w - self.b * 2) / nchar > 8
        assert (self.h - self.b * 2) / nline > 8
        wpixels = nchar * 8
        x = self.w / 2 - wpixels / 2
        y = ((self.h - self.b * 2) / nline) * (lino - 1 / 2) + self.b - 4
        self._screen.text(litext, int(x), int(y))

    def show_text(self, text, border=True):
        # text : str or list[str]
        self._clear()
        if border:
            self._fill_border()
        if isinstance(text, str):
            text = text.split()
        nline = len(text)
        for lino, litext in enumerate(text, 1):
            self._fill_linetext(litext, lino, nline)

        self._screen.show()

    def show_progress(self, message, secs, border=True):
        self._clear()
        if border:
            self._fill_border()
        padding = 10
        expand_count_per_sec = 5
        duration_ms = 1000 // expand_count_per_sec
        count = secs * expand_count_per_sec  # expand 5 times per second
        bw = (self.w - self.b * 2 -
              padding * 2) // count  # now secs should <= 21 s
        assert bw > 0

        self._fill_linetext(message, 1, 2)

        x = int(self.b + padding)
        y = int((self.h - self.b * 2) / 2 * (2 - 1 / 2) + self.b - 4)
        for i in range(count):
            self._screen.fill_rect(x + i * bw, y, bw, 8, 1)
            self._screen.show()
            time.sleep_ms(duration_ms)
