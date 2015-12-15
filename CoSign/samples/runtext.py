#!/usr/bin/env python
# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics
import time

class RunText(SampleBase):
    def __init__(self,lineOne, lineTwo,*args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
	self.lineOne = lineOne
	self.lineTwo = lineTwo

    def Run(self):
        offscreenCanvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("./fonts/6x12.bdf")
        font2 = graphics.Font()
        font2.LoadFont("./fonts/5x8.bdf")
        textColor = graphics.Color(0,100,100)
        textColor2 = graphics.Color(100,0,100)
        pos = offscreenCanvas.width
        myText = self.lineOne
        myText2 = self.lineTwo + "mi"
        startPos = (32*2) - (len(myText2)*5)
        startPos1 = (32*2) - (len(myText)*6)
        startPos1 = 1

        while True:
            offscreenCanvas.Clear()
            len1 = graphics.DrawText(offscreenCanvas, font, startPos1, 7, textColor, myText)
	    len2 = graphics.DrawText(offscreenCanvas, font2, startPos, 16, textColor2, myText2)
            pos -= 1
            if (pos + len1 < 0):
                pos = offscreenCanvas.width

            time.sleep(0.05)
            offscreenCanvas = self.matrix.SwapOnVSync(offscreenCanvas)


# Main function
if __name__ == "__main__":
    parser = RunText("Bill's dick", "1000")
    if (not parser.process()):
        parser.print_help()
