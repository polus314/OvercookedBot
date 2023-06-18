import PIL.ImageGrab
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

class LevelVision:
    def __init__(self, log_file):
        self.log_file = log_file

    def need_plate_for_order(self, order_type):
        self.log_file.error("In need_plate_for_order")

        # Take screenshot
        im = PIL.ImageGrab.grab()

        if order_type == "cod":
            plate_x = 635
        elif order_type == "shrimp":
            plate_x = 1175

        plate_y = 475
        plate_width = 60
        plate_height = 60

        im2 = im.crop((plate_x, plate_y, plate_x + plate_width, plate_y + plate_height))

        # im2.show()

        r, g, b = self.get_avg_pixel_values(im2)
        if order_type == "cod":
            has_plate = self.match_rgb((r, g, b), (243, 234, 210))
            # is_empty = match_rgb((r, g, b), (234, 188, 113))
        elif order_type == "shrimp":
            has_plate = self.match_rgb((r, g, b), (243, 229, 203))
            # is_empty = match_rgb((r, g, b), (252, 200, 114))

        needs_plate = not has_plate

        self.log_file.error("Needs plate? " + str(needs_plate))
        return needs_plate

    def check_for_clean_plate(self):
        # Looking at space M5 on map

        # Take screenshot
        im = PIL.ImageGrab.grab()


        plate_x = 1445
        plate_y = 475
        plate_width = 60
        plate_height = 60

        im2 = im.crop((plate_x, plate_y, plate_x + plate_width, plate_y + plate_height))

        # im2.show()

        r, g, b = self.get_avg_pixel_values(im2)
        has_clean_plate = self.match_rgb((r, g, b), (192, 185, 179))
        # no_clean_plate = match_rgb((r, g, b), (160, 144, 141))

        self.log_file.error("Clean plate? " + str(has_clean_plate))
        return has_clean_plate

    def determine_next_order(self):
        self.log_file.log("In determine_next_order")

        # Take screenshot
        im = PIL.ImageGrab.grab()

        # Crop down to the region that has orders
        im2 = im.crop((0, 0, 850, 150))

        icon_x = 23
        icon_y = 98
        icon_width = 45
        icon_height = 45

        im3 = im2.crop((icon_x, icon_y, icon_x + icon_width, icon_y + icon_height))

        im3.load()

        r, g, b = self.get_avg_pixel_values(im3)
        is_shrimp = self.approx_equals(r, 200) and self.approx_equals(b, 154)
        is_cod = self.approx_equals(r, 145) and self.approx_equals(b, 197)

        order = "Unknown"
        if is_shrimp:
            order = "shrimp"
        if is_cod:
            order = "cod"

        self.log_file.log("Order is " + order)

        return order

    def match_rgb(self, rgb1, rgb2):
        r1, g1, b1 = rgb1
        r2, g2, b2 = rgb2
        return self.approx_equals(r1, r2) and self.approx_equals(g1, g2) and self.approx_equals(b1, b2)

    def get_avg_pixel_values(self, im):
        width, height = im.size
        pixels = im.load()

        r_cumulative, g_cumulative, b_cumulative = 0, 0, 0
        total_pixels = 0
        all_pixels = []
        for x in range(width):
            for y in range(height):
                r, g, b = pixels[x, y]
                r_cumulative += r
                g_cumulative += g
                b_cumulative += b

                total_pixels += 1

        r_avg = r_cumulative / total_pixels
        g_avg = g_cumulative / total_pixels
        b_avg = b_cumulative / total_pixels

        self.log_file.log("R: " + str(r_cumulative) + " " + str(r_avg))
        self.log_file.log("G: " + str(g_cumulative) + " " + str(g_avg))
        self.log_file.log("B: " + str(b_cumulative) + " " + str(b_avg))

        return r_avg, g_avg, b_avg

    def approx_equals(self, val1, val2):
        delta = 5
        return self.between(val1, val2 - delta, val2 + delta)

    def between(self, val, min, max):
        if min < val and val < max:
            return True
        else:
            return False

    def corner_detection(self):
        filename = "cv_images/Level1 Zoomed In.png"
        img = cv.imread(filename)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        gray = np.float32(gray)
        dst = cv.cornerHarris(gray, 2, 3, 0.04)

        # result is dilated for finding the corners, not important (?)
        dst = cv.dilate(dst, None)

        # Threshold for an optimal value, it may vary depending on the image
        img[dst > 0.01*dst.max()] = [0, 0, 255]

        cv.imshow('dst', img)
        if cv.waitKey(0) & 0xff == 27:
            cv.destroyAllWindows()

    def corner_detection_2(self):
        filename = 'cv_images/Level1 Zoomed In.png'
        img = cv.imread(filename)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        # find Harris corners
        gray = np.float32(gray)
        dst = cv.cornerHarris(gray, 2, 3, 0.04)
        dst = cv.dilate(dst, None)
        ret, dst = cv.threshold(dst, 0.01 * dst.max(), 255, 0)
        dst = np.uint8(dst)
        # find centroids
        ret, labels, stats, centroids = cv.connectedComponentsWithStats(dst)
        # define the criteria to stop and refine the corners
        criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 100, 0.001)
        corners = cv.cornerSubPix(gray, np.float32(centroids), (5, 5), (-1, -1), criteria)
        # Now draw them
        res = np.hstack((centroids, corners))
        res = np.int0(res)
        img[res[:, 1], res[:, 0]] = [0, 0, 255]
        img[res[:, 3], res[:, 2]] = [0, 255, 0]
        cv.imwrite('subpixel5.png', img)

        cv.imshow('dst', img)
        if cv.waitKey(0) & 0xff == 27:
            cv.destroyAllWindows()

    def corner_detection_3(self):
        filename = "cv_images/Level1 Zoomed In.png"
        img = cv.imread(filename)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        num_corners_to_find = 500
        corners = cv.goodFeaturesToTrack(gray, num_corners_to_find, 0.01, 10)
        corners = np.int0(corners)
        for i in corners:
            x, y = i.ravel()
            cv.circle(img, (x, y), 3, 255, -1)
        plt.imshow(img), plt.show()

    def keypoint_detection(self):
        filename = "cv_images/Level1 Zoomed In.png"
        img = cv.imread(filename)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        sift = cv.SIFT_create()
        kp = sift.detect(gray, None)
        # img = cv.drawKeypoints(gray, kp, img)
        # cv.imwrite('sift_keypoints.jpg', img)

        img = cv.drawKeypoints(gray, kp, img, flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        cv.imwrite('sift_keypoints.jpg', img)

        cv.imshow('dst', img)
        if cv.waitKey(0) & 0xff == 27:
            cv.destroyAllWindows()



    def object_finder(self):
        MIN_MATCH_COUNT = 10
        filename_ref = "cv_images/trashcan.png"
        filename_screenshot = "cv_images/Level1 Zoomed In.png"

        img1 = cv.imread(filename_ref, cv.IMREAD_GRAYSCALE)  # queryImage
        img2 = cv.imread(filename_screenshot, cv.IMREAD_GRAYSCALE)  # trainImage
        # Initiate SIFT detector
        sift = cv.SIFT_create()
        # find the keypoints and descriptors with SIFT
        kp1, des1 = sift.detectAndCompute(img1, None)
        kp2, des2 = sift.detectAndCompute(img2, None)
        FLANN_INDEX_KDTREE = 1
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)
        flann = cv.FlannBasedMatcher(index_params, search_params)
        matches = flann.knnMatch(des1, des2, k=2)
        # store all the good matches as per Lowe's ratio test.
        good = []
        for m, n in matches:
            if m.distance < 0.7 * n.distance:
                good.append(m)

        if len(good) > MIN_MATCH_COUNT:
            src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
            M, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC, 5.0)
            matchesMask = mask.ravel().tolist()
            h, w = img1.shape
            pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
            dst = cv.perspectiveTransform(pts, M)
            img2 = cv.polylines(img2, [np.int32(dst)], True, 255, 3, cv.LINE_AA)
        else:
            print("Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT))
            matchesMask = None

        draw_params = dict(matchColor=(0, 255, 0),  # draw matches in green color
                           singlePointColor=None,
                           matchesMask=matchesMask,  # draw only inliers
                           flags=2)
        img3 = cv.drawMatches(img1, kp1, img2, kp2, good, None, **draw_params)
        plt.imshow(img3, 'gray'), plt.show()


    def test(self):
        self.object_finder()