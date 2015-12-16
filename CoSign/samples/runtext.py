#!/usr/bin/env python
# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics
import time, threading

class RunText(SampleBase):
    def __init__(self, place, distance, stop, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
        self.place = place
        self.distance = distance + " mi"
        self.stop = stop

    def Run(self):
        offscreenCanvas = self.matrix.CreateFrameCanvas()

        placeFont = graphics.Font()
        placeFont.LoadFont("./fonts/6x12.bdf")
        distFont = graphics.Font()
        distFont.LoadFont("./fonts/5x8.bdf")

        placeColor = graphics.Color(0,100,100)
        distColor = graphics.Color(100,0,100)

        # Right justify the distance text
        distStartPos = (32*2) - (len(self.distance)*5)

        if (len(self.place) > 10):
            # Place name can't fit on the screen, so scroll it
            pos = offscreenCanvas.width
            # Keep running until we get a stop signal
            while (not self.stop.is_set()):
                offscreenCanvas.Clear()
                len1 = graphics.DrawText(offscreenCanvas, placeFont, pos, 7, placeColor, self.place)
                len2 = graphics.DrawText(offscreenCanvas, distFont, distStartPos, 16, distColor, self.distance)

                # Scroll backwards, loop back when it reaches the end
                pos -= 1
                if (pos + len1 < 0):
                    pos = offscreenCanvas.width

                time.sleep(0.05)
                offscreenCanvas = self.matrix.SwapOnVSync(offscreenCanvas)
        else:
            placeStartPos = 1
            offscreenCanvas.Clear()
            len1 = graphics.DrawText(offscreenCanvas, placeFont, placeStartPos, 7, placeColor, self.place)
            len2 = graphics.DrawText(offscreenCanvas, distFont, distStartPos, 16, distColor, self.distance)
            offscreenCanvas = self.matrix.SwapOnVSync(offscreenCanvas)


# Main function
if __name__ == "__main__":
    parser = RunText("Bill's dick", "1000")
    if (not parser.process()):
        parser.print_help()
