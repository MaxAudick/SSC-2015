__author__ = 'max'

import numpy as np
import cv2
import threading
from collections import deque
import time


def resize(im_arr, factor=1):
    num_rows = int(len(im_arr) / factor)
    num_cols = int(len(im_arr[0]) / factor)
    arr_out = np.zeros((num_rows, num_cols), dtype=np.uint8)
    for r in range(num_rows):
        for c in range(num_cols):
            arr_out[r][c] = im_arr[int(r * factor)][int(c * factor)]
    return arr_out


def make_noise(im_arr, max_amp):
    num_rows = len(im_arr)
    num_cols = len(im_arr[0])
    arr_out = np.zeros((num_rows, num_cols), dtype=np.uint8)
    for r in range(num_rows):
        for c in range(num_cols):
            new_pixel = int(im_arr[r][c] + (np.random.randn() * max_amp) - 1)
            if new_pixel < 0:
                new_pixel = 0
            if new_pixel > 255:
                new_pixel = 255
            arr_out[r][c] = int(new_pixel)
    return arr_out


def moving_average_filter(im_arr, width):
    print 'initialized: block summation processing'
    num_rows = len(im_arr)
    num_cols = len(im_arr[0])
    arr_out = np.zeros((num_rows, num_cols), dtype=np.uint8)
    for r in range(num_rows):
        for c in range(num_cols):
            total = 0
            div = 0
            for r2 in range(width):
                for c2 in range(width):
                    r2 = r + (width / 2) - r2
                    c2 = c + (width / 2) - c2
                    if 0 <= r2 < len(im_arr) and 0 <= c2 < len(im_arr[0]):
                        total += im_arr[r2][c2]
                        div += 1
            arr_out[r][c] = int(total / div)
    im_arr = arr_out
    print 'completed'


def moving_average_filter2(im_arr, width):
    print 'initialized: deque processing 2.0'
    num_rows = len(im_arr)
    num_cols = len(im_arr[0])
    arr_out = np.zeros((num_rows, num_cols), dtype=np.uint8)
    for r in range(num_rows):
        total = 0
        div = 0
        for r2 in range(width):
            r2 = r + (width / 2) - r2
            if 0 <= r2 < len(im_arr):
                for c2 in range(width / 2):
                    total += im_arr[r2][c2]
                    div += 1

        for c in range(num_cols):
            offset = 0
            for win_r in range(width):
                r2 = r + (width / 2) - win_r
                c2 = c + (width / 2)
                if 0 <= r2 < len(im_arr):
                    if 0 <= c2 < len(im_arr[0]):
                        try:
                            total += im_arr[r2][c2]
                            div += 1
                        except:
                            continue
                    if c2 >= width:
                        try:
                            total -= im_arr[r2][c2 - width]
                            div -= 1
                        except:
                            continue
            arr_out[r][c] = int(total / div)
    print 'completed'
    return arr_out


def moving_average_filter3(im_arr, mask):
    print 'initialized: deque processing'
    width = len(mask)
    mask_sum = 0
    for row in mask:
        for val in row:
            mask_sum += val
    half_width = width / 2
    sqr_width = width ** 2
    num_rows = len(im_arr)
    num_cols = len(im_arr[0])
    arr_out = np.zeros((num_rows, num_cols), dtype=np.uint8)
    im_arr = np.pad(im_arr, ((half_width, half_width), (half_width, half_width)), 'constant')
    for r in range(num_rows):
        window = []
        for r2 in range(width):
            r2 += r
            window.append(deque([im_arr[r2][c2] for c2 in range(width)]))

        for c in range(num_cols):

            win_out = window * mask
            total = 0
            for row in win_out:
                total += sum(row)
            arr_out[r][c] = total / mask_sum

            for r2 in range(width):
                window[r2].popleft()
                try:
                    window[r2].append(im_arr[r][c + half_width])
                except:
                    continue
    print 'completed'
    return arr_out


def noise_filter(image, mask):
    image_filtered = cv2.filter2D(image, 3, mask, anchor=(2, 2))
    mask_sum = 0
    for row in mask:
        for val in row:
            mask_sum += val
    image_out = np.empty((len(image), len(image[0])), dtype=np.uint8)
    for r in range(len(image)):
        for c in range(len(image[0])):
            image_out[r][c] = int(image_filtered[r][c])
    return image_out


class MAFThread(threading.Thread):
    def __init__(self, im_arr, width, thread_name=None):
        threading.Thread.__init__(self)
        self.im_arr = im_arr
        self.width = width
        self.thread_name = thread_name

    def run(self):
        threadLock.acquire()
        moving_average_filter(self.im_arr, self.width)
        threadLock.release()


# ---------- ---------- ---------- ---------- ---------- ----------#

threadLock = threading.Lock()

mask5 = [[0.0073068827452812644, 0.03274717653776802, 0.05399096651318985, 0.03274717653776802, 0.0073068827452812644], [0.03274717653776802, 0.14676266317374237, 0.24197072451914536, 0.14676266317374237, 0.03274717653776802], [0.05399096651318985, 0.24197072451914536, 0.3989422804014327, 0.24197072451914536, 0.05399096651318985], [0.03274717653776802, 0.14676266317374237, 0.24197072451914536, 0.14676266317374237, 0.03274717653776802], [0.0073068827452812644, 0.03274717653776802, 0.05399096651318985, 0.03274717653776802, 0.0073068827452812644]]
mask3 = [[0.14676266317374237, 0.24197072451914536, 0.14676266317374237], [0.24197072451914536, 0.3989422804014327, 0.24197072451914536], [0.14676266317374237, 0.24197072451914536, 0.14676266317374237]]
mask7 = [[0.011467427226951498, 0.026386273579782998, 0.04350361050550067, 0.05139344326792439, 0.04350361050550067, 0.026386273579782998, 0.011467427226951498], [0.026386273579782998, 0.06071417935758214, 0.10010075893994747, 0.11825507390946054, 0.10010075893994747, 0.06071417935758214, 0.026386273579782998], [0.04350361050550067, 0.10010075893994747, 0.16503825047751605, 0.1949696557227417, 0.16503825047751605, 0.10010075893994747, 0.04350361050550067], [0.05139344326792439, 0.11825507390946054, 0.1949696557227417, 0.23032943298089034, 0.1949696557227417, 0.11825507390946054, 0.05139344326792439], [0.04350361050550067, 0.10010075893994747, 0.16503825047751605, 0.1949696557227417, 0.16503825047751605, 0.10010075893994747, 0.04350361050550067], [0.026386273579782998, 0.06071417935758214, 0.10010075893994747, 0.11825507390946054, 0.10010075893994747, 0.06071417935758214, 0.026386273579782998], [0.011467427226951498, 0.026386273579782998, 0.04350361050550067, 0.05139344326792439, 0.04350361050550067, 0.026386273579782998, 0.011467427226951498]]
mask5 = np.array(mask5)
mask3 = np.array(mask3)
mask7 = np.array(mask7)

def main():
    amp = 100
    img = cv2.imread('/home/max/internship/mapping/ZoomedOut.png')
    cv2.imshow('original', img)

    print 'resizing image (down)'
    b, g, r = cv2.split(img)
    b = resize(b, 4)
    g = resize(g, 4)
    r = resize(r, 4)
    img2 = cv2.merge([b, g, r])
    cv2.imshow('scaled down', img2)

    print 'resizing image (up)'
    b, g, r = cv2.split(img2)
    b = resize(b, .25)
    g = resize(g, .25)
    r = resize(r, .25)
    img3 = cv2.merge([b, g, r])
    cv2.imshow('rescaled original', img3)

    print 'applying moving average filter'
    b, g, r = cv2.split(img3)
    moving_average_filter(b, 5)
    moving_average_filter(g, 5)
    moving_average_filter(r, 5)
    img4 = cv2.merge([b, g, r])
    cv2.imshow('moving average filter', img4)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


def resize_test():
    img = cv2.imread('/home/max/internship/mapping/ZoomedOut.png')
    cv2.imshow('original', img)
    b, g, r = cv2.split(img)
    b = resize(b)
    g = resize(g)
    r = resize(r)
    b = moving_average_filter2(b, 3)
    g = moving_average_filter2(g, 3)
    r = moving_average_filter2(r, 3)
    cv2.imshow('resized', cv2.merge([b, g, r]))
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def time_trial(i=1):
    img = cv2.imread('/home/max/internship/mapping/ZoomedOut.png')
    cv2.imshow('original', img)
    b, g, r = cv2.split(img)

    print 'PROCESSING 3x3'
    t_init = time.time()
    b = moving_average_filter3(b, 3)
    print time.time() - t_init
    t_init = time.time()
    b = moving_average_filter2(b, 3)
    print time.time() - t_init
    t_init = time.time()
    moving_average_filter(b, 3)
    print time.time() - t_init
    print

    if i > 1:
        print 'PROCESSING 5x5'
        t_init = time.time()
        b = moving_average_filter3(b, 5)
        print time.time() - t_init
        t_init = time.time()
        b = moving_average_filter2(b, 5)
        print time.time() - t_init
        t_init = time.time()
        moving_average_filter(b, 5)
        print time.time() - t_init
    if i > 2:
        print 'PROCESSING 7x7'
        t_init = time.time()
        b = moving_average_filter3(b, 7)
        print time.time() - t_init
        t_init = time.time()
        b = moving_average_filter2(b, 7)
        print time.time() - t_init
        t_init = time.time()
        moving_average_filter(b, 7)
        print time.time() - t_init


def test_function():
    mask = [[0.0073068827452812644, 0.03274717653776802, 0.05399096651318985, 0.03274717653776802, 0.0073068827452812644], [0.03274717653776802, 0.14676266317374237, 0.24197072451914536, 0.14676266317374237, 0.03274717653776802], [0.05399096651318985, 0.24197072451914536, 0.3989422804014327, 0.24197072451914536, 0.05399096651318985], [0.03274717653776802, 0.14676266317374237, 0.24197072451914536, 0.14676266317374237, 0.03274717653776802], [0.0073068827452812644, 0.03274717653776802, 0.05399096651318985, 0.03274717653776802, 0.0073068827452812644]]
    mask = np.array(mask)
    mask_ones = np.array([[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1]])
    img = cv2.imread('/home/max/internship/mapping/ZoomedOut.png')
    cv2.imshow('original', img)
    b, g, r = cv2.split(img)
    print 'applying noise'
    b = make_noise(b, 0)
    print b
    print 'blue - DONE'
    g = make_noise(g, 0)
    print 'green - DONE'
    r = make_noise(r, 0)
    print 'red - DONE'
    cv2.imshow('noisy', cv2.merge([b, g, r]))
    print 'filtering'
    b = noise_filter(b, mask_ones)
    print b
    print 'blue - DONE'
    g = noise_filter(g, mask_ones)
    print 'green - DONE'
    r = noise_filter(r, mask_ones)
    print 'red - DONE'
    cv2.imshow('filtered', cv2.merge([b, g, r]))
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def test_filtering_noise():
    amp = 500
    img = cv2.imread('/home/max/internship/LinearAlgebra/Lenna.png')
    cv2.imshow('original', img)
    b, g, r = cv2.split(img)
    b = make_noise(b, amp)
    g = make_noise(g, amp)
    r = make_noise(r, amp)
    cv2.imshow('noisy', cv2.merge([b, g, r]))
    b = moving_average_filter3(b, mask5)
    g = moving_average_filter3(g, mask5)
    r = moving_average_filter3(r, mask5)
    cv2.imshow('filtered', cv2.merge([b, g, r]))
    b = moving_average_filter3(b, mask5)
    g = moving_average_filter3(g, mask5)
    r = moving_average_filter3(r, mask5)
    cv2.imshow('filtered2x', cv2.merge([b, g, r]))
    b = moving_average_filter3(b, mask5)
    g = moving_average_filter3(g, mask5)
    r = moving_average_filter3(r, mask5)
    cv2.imshow('filtered3x', cv2.merge([b, g, r]))
    cv2.waitKey(0)

def test_filtering_resize():
    amp = 6
    img = cv2.imread('/home/max/internship/LinearAlgebra/Lenna.png')
    cv2.imshow('original', img)
    b, g, r = cv2.split(img)
    b = resize(b, amp)
    g = resize(g, amp)
    r = resize(r, amp)
    cv2.imshow('downsized', cv2.merge([b, g, r]))
    b = resize(b, 1. / amp)
    g = resize(g, 1. / amp)
    r = resize(r, 1. / amp)
    cv2.imshow('upsized', cv2.merge([b, g, r]))
    b2 = moving_average_filter3(b, mask3)
    g2 = moving_average_filter3(g, mask3)
    r2 = moving_average_filter3(r, mask3)
    cv2.imshow('filtered - small mask', cv2.merge([b2, g2, r2]))
    b2 = moving_average_filter3(b, mask7)
    g2 = moving_average_filter3(g, mask7)
    r2 = moving_average_filter3(r, mask7)
    cv2.imshow('filtered - large mask', cv2.merge([b2, g2, r2]))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

test_filtering_noise()
