import datetime
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
from queue import Queue
import multiprocessing
import fonksiyonlar as fonks


class MyThread (threading.Thread):
    maxRetries = 20

    def __init__(self, thread_id, name, thread_lock):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.thread_lock = thread_lock

    def run(self):
        print ("Starting " + self.name)
        window_name = self.name
        cv2.namedWindow(window_name)
        video = cv2.VideoCapture(0)
        while True:
            # self.thread_lock.acquire()  # These didn't seem necessary
            got_a_frame, image = video.read()
            image = fonks.annotate_image(image)
            # self.thread_lock.release()
            if not got_a_frame:  # error on video source or last frame finished
                break
            cv2.imshow(window_name, image)
            key = cv2.waitKey(50) & 0xFF
            if key == 27 or ord("q"):
                break
        cv2.destroyWindow(window_name)
        print (self.name + " Exiting")


def main():
    thread_lock = threading.Lock()
    thread1 = MyThread(1, "Thread 1", thread_lock)
    thread2 = MyThread(2, "Thread 2", thread_lock)
    thread1.start()
    thread2.start()
    print ("Exiting Main Thread")

if __name__ == '__main__':
    main()



















