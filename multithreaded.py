# import the necessary packages
import datetime
import time
import sys
import os
import os.path
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import argparse
import imutils
import cv2
import threading
from threading import Thread
import multiprocessing
import fonksiyonlar as fonks

key=0

class SignalHandler:
    """
    The object that will handle signals and stop the worker threads.
    """

    #: The stop event that's shared by this handler and threads.
    stopper = None

    #: The pool of worker threads
    workers = None

    def __init__(self, stopper, workers):
        self.stopper = stopper
        self.workers = workers

    def __call__(self, signum, frame):
        """
        This will be called by the python signal module

        https://docs.python.org/3/library/signal.html#signal.signal
        """
        self.stopper.set()

        for worker in self.workers:
            worker.join()

        sys.exit(0)

class FPS:
    def __init__(self):
        # store the start time, end time, and total number of frames
        # that were examined between the start and end intervals
        self._start = None
        self._end = None
        self._numFrames = 0

    def start(self):
        # start the timer
        self._start = datetime.datetime.now()
        return self

    def stop(self):
        # stop the timer
        self._end = datetime.datetime.now()

    def update(self):
        # increment the total number of frames examined during the
        # start and end intervals
        self._numFrames += 1

    def elapsed(self):
        # return the total number of seconds between the start and
        # end interval
        return (self._end - self._start).total_seconds()

    def fps(self):
        # compute the (approximate) frames per second
        return self._numFrames / self.elapsed()
#(threading.Thread)
class WebcamVideoStream:
    def __init__(self, src=0,lock= 0):
        #super().__init__()
        # initialize the video camera stream and read the first frame
        # from the stream
        threading.Thread.__init__(self)
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        self.lock=lock
        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False
    def start(self):
        # start the thread to read frames from the video stream

        try:
            for x in range(args["multithread"]):
                self.thread = Thread(target=self.update, args=())
                self.thread.daemon = True #garbage collection starts
                self.thread.start()
        except (KeyboardInterrupt, SystemExit):
            self.stop()
            sys.exit("Program Interrupted")
            #Thread.daemon = False
        except AssertionError: self.stop()

        '''
        try:
            jobs = []
            for i in range(args["multiprocess"]):
                self.p = multiprocessing.Process(target=self.update)
                jobs.append(self.p)
                self.p.start()
                #self.p.daemon=True
        except (KeyboardInterrupt, SystemExit):
            for i in range(args["multiprocess"]):
                self.p.terminate()
                self.stop()
        except AssertionError:
            self.stop()
        '''

        return self
    def update(self):
        # keep looping infinitely until the thread is stopped
        try:
            while True:
                # if the thread indicator variable is set, stop the thread
                try:
                    if self.stopped:
                        return
                    # otherwise, read the next frame from the stream
                    (self.grabbed, self.frame) = self.stream.read()
                    if self.grabbed==False:
                        print("camera connection maybe lost or video has ended.")
                        break
                    self.frame = fonks.annotate_image(self.frame)
                    if fonks.ret==False: #self.frame==False:
                        continue
                except TypeError:
                    if key is 0:
                        continue
                    else:
                        break
                except Exception as e:
                    print(e); continue
                # print("There is no lane") #çizgi algılanamazsa çökmesin.
        except TypeError:
            pass
        except Exception as e:
            print(e)
        # print("There is no lane") #çizgi algılanamazsa çökmesin.
        except (KeyboardInterrupt, SystemExit):
            self.stop()
            if self.stopped:
                return
            sys.exit("Program Interrupted")
            # Thread.daemon = False
        except AssertionError:
            self.stop()
            print("AssertionError Error.")
            if self.stopped:
                return
        except Exception as e:
            print("Unknown Error")
            self.stop()
            if self.stopped:
                return

    def read(self):
        # return the frame most recently read
        return (self.grabbed,self.frame)
    def stop(self):
        # indicate that the thread should be stopped
        #self._stopper = threading.Event()
        #threading._shutdown()
        self.stopped = True
        #sys.exit(0)


# import the necessary packages

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
#default=400 yerine None yazılıp while içine if args["num_frames"]==None while 1: ... diye sonsuza kadar gidebilir.
ap.add_argument("-i", "--infinite", type=bool, default=True,
                help="Do you want limited number of frame or not? default=True")
ap.add_argument("-n", "--num-frames", type=int, default=-1,
                help="# of frames to loop over for FPS test. default=-1")
ap.add_argument("-d", "--display", type=bool, default=True,
                help="Whether or not frames should be displayed. default True")
ap.add_argument("-v","--cameravideo",type=int, default=0,
                help="Do you want to play video or open your camera? default=0")
ap.add_argument("-t","--multithread",type=int,default=0,
                help="how may process do you need?")
args = vars(ap.parse_args())
lock = threading.RLock() # multiple time wait for synchronization

def notthread():
    # grab a pointer to the video stream and initialize the FPS counter
    print("[INFO] sampling frames from webcam...")
    if args["cameravideo"]==0:
        src=0
    else:
        src = input("input video")
        assert os.path.exists(src), "I did not find the file at, " + str(src)
    stream = cv2.VideoCapture(src)
    fps = FPS().start()
    # not multithreded
    # loop over some frames
    num_frame = fps._numFrames < args["num_frames"]
    if args["infinite"]==True:
        if args["num_frames"]>0:
            sys.exit("""You said infinite and limited frame. it is not sensible """)
        num_frame = True

    while num_frame:
        # grab the frame from the stream and resize it to have a maximum
        # width of 400 pixels
        try:
            (grabbed, frame) = stream.read()
            if grabbed==False:
                print("camera connection maybe lost or video has ended.")
                break
            frame = imutils.resize(frame, width=400)
            frame = fonks.annotate_image(frame)
        except (TypeError,AttributeError): pass # print("There is no lane") #çizgi algılanamazsa çökmesin.
        except Exception as e: print(e)
        # check to see if the frame should be displayed to our screen
        if args["display"] > 0:
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == 27 or key == ord('q'):
                break
        # update the FPS counter
        fps.update()

    # stop the timer and display FPS information
    fps.stop()
    print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

    # do a bit of cleanup
    stream.release()
    cv2.destroyAllWindows()

def thrededed():
    # created a *threaded* video stream, allow the camera sensor to warmup,
    # and start the FPS counter
    print("[INFO] sampling THREADED frames from webcam...")

    if args["cameravideo"] == 0:
        src=0
    else:
        src=input("input video")
        assert os.path.exists(src), "I did not find the file at, " + str(src)
    vs = WebcamVideoStream(src=src).start()
    fps = FPS().start()
    # multithreded
    # loop over some frames...this time using the threaded stream
    num_frame = fps._numFrames < args["num_frames"]
    if args["infinite"] == True:
        if args["num_frames"] > 0:
            sys.exit("""You said infinite and limited frame. it is not sensible """)
        num_frame = True

    while num_frame:
        # grab the frame from the threaded video stream and resize it
        # to have a maximum width of 400 pixels
        # with lock:
        try:
            # with lock:
            with lock:
                grapped,frame = vs.read()
                if grapped==False:
                    print("camera connection maybe lost or video has ended.")
                    break
                frame = imutils.resize(frame, width=400)
                # check to see if the frame should be displayed to our screen

                if args["display"] > 0:
                    cv2.imshow("Frame", frame)
                    key = cv2.waitKey(1) & 0xFF
                    if key == 27 or key == ord('q'):
                        vs.stop()
                        if vs.stopped:
                            return
                        break
        except (KeyboardInterrupt, SystemExit):

            vs.stop()

            if vs.stopped:
                return

            sys.exit("Program Interrupted")

            # Thread.daemon = False
        except AssertionError:

            vs.stop()

            print("AssertionError Error.")

            if vs.stopped:
                return
        except TypeError:
            print("There is no lane");
            time.sleep(.5)
            continue  # pass #çizgi algılanamazsa çökmesin.
        except Exception as e:

            print(e)

            vs.stop()

            if vs.stopped:
                return






        # update the FPS counter
        fps.update()

    # stop the timer and display FPS information
    fps.stop()
    print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

    # do a bit of cleanup
    cv2.destroyAllWindows()
    vs.stop()


if __name__=="__main__":
    if args["multithread"]>0:
        thrededed()
    elif args["multithread"] is 0:
        notthread()
    else:
        sys.exit("wrong selection or typing")