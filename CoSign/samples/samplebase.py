import argparse, time, sys, os

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))
from rgbmatrix import RGBMatrix

class SampleBase(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        super(SampleBase, self).__init__(*args, **kwargs)

        self.args = {}

    def usleep(self, value):
        time.sleep(value / 1000000.0)

    def Run(self):
        print("Running")

    def process(self):

        self.matrix = RGBMatrix(16, 2, 1)
        self.matrix.pwmBits = 11
        self.matrix.brightness = 100

        self.matrix.luminanceCorrect = False

        try:
            # Start loop
            print("Press CTRL-C to stop sample")
            self.Run()
        except KeyboardInterrupt:
            print "Exiting\n"
            sys.exit(0)

        return True
