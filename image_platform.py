import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from numpy import array, arange
from math import ceil

from noise_generator import generation_additive_zero_mean_Gaussian_noise


class ImagePlatform():
    def __init__(self) -> None:
        self.max_image_width = 700
        self.max_image_height = 850

        self.__window_init()
        self.__bottom_init()
        self.__title_init()
        self.__image_init()

        self.window.mainloop()

    def __window_init(self):
        self.window = tk.Tk()
        self.window.title('AIP 61047007S')
        self.window.geometry('1600x900')
        self.window.configure(background='#fbf2e2')
        self.window.columnconfigure(0, weight=7)
        self.window.columnconfigure(1, weight=2)
        self.window.columnconfigure(2, weight=7)

    def __bottom_init(self):
        select_buttom = tk.Button(self.window, text='請選擇圖片',
                                  command=self.__open_picture, bg="white", fg='#0f506d', font=('微軟正黑體', 16), width=10, height=1)

        select_buttom.grid(column=1, row=1, sticky="NS")

        save_buttom = tk.Button(self.window, text='儲存圖片',
                                command=self.__save_picture, bg="white", fg='#0f506d', font=('微軟正黑體', 16), width=10, height=1)

        save_buttom.grid(column=1, row=2, sticky="NS")

        gray_pricture_buttom = tk.Button(self.window, text='轉為灰階圖',
                                         command=self.__output_to_gray, bg="white", fg='#0f506d', font=('微軟正黑體', 16), width=10, height=1)

        gray_pricture_buttom.grid(column=1, row=3, sticky="NS")

        gray_histogram_buttom = tk.Button(self.window, text='灰階直方圖',
                                          command=self.__output_to_gray_histogram, bg="white", fg='#0f506d', font=('微軟正黑體', 16), width=10, height=1)

        gray_histogram_buttom.grid(column=1, row=4, sticky="NS")

        gaussian_noise_sd_label = tk.Label(
            self.window, text="請輸入標準差:\n(範圍為0~1)", bg="#fbf2e2", font=('微軟正黑體', 14))
        gaussian_noise_sd_label.grid(column=1, row=5, sticky="NS")

        self.gaussian_noise_sd = tk.DoubleVar()
        self.gaussian_noise_sd.set(0.1)

        gaussian_noise_sd_entry = tk.Entry(
            self.window, textvariable=self.gaussian_noise_sd, width=15)
        gaussian_noise_sd_entry.grid(column=1, row=6, sticky="NS")

        gaussian_noise_buttom = tk.Button(self.window, text='高斯雜訊',
                                          command=self.__output_guassian_noise, bg="white", fg='#0f506d', font=('微軟正黑體', 16), width=10, height=1)

        gaussian_noise_buttom.grid(column=1, row=7, sticky="NS")

    def __title_init(self):
        input_image_text = tk.Label(
            self.window, text='input image:', image=None, bg="#0f506d", fg='white', font=('微軟正黑體', 16))
        input_image_text.grid(column=0, row=0, sticky="NSEW", ipady=6)

        between_input_output = tk.Frame(self.window, bg="#0f506d")
        between_input_output.grid(column=1, row=0, sticky="NSEW")

        output_image_text = tk.Label(
            self.window, text='output image:', image=None, bg="#0f506d", fg='white', font=('微軟正黑體', 16))
        output_image_text.grid(column=2, row=0, sticky="NSEW")

    def __image_init(self):
        self.first_input_image_label = tk.Label(self.window, text='pictures will show in this place', bg="#fbf2e2",
                                                image=None)  # 創建一個標籤
        self.first_input_image_label.grid(
            column=0, row=1, rowspan=100)  # 放置標籤

        self.first_output_image_label = tk.Label(self.window, text='pictures will show in this place', bg="#fbf2e2",
                                                 image=None)  # 創建一個標籤
        self.first_output_image_label.grid(
            column=2, row=1, rowspan=100)  # 放置標籤

        self.second_input_image_label = tk.Label(self.window, bg="#fbf2e2",
                                                 image=None)  # 創建一個標籤
        self.second_input_image_label.grid(
            column=0, row=200, rowspan=200)  # 放置標籤

        self.second_output_image_label = tk.Label(self.window, bg="#fbf2e2",
                                                  image=None)  # 創建一個標籤
        self.second_output_image_label.grid(
            column=2, row=200, rowspan=200)  # 放置標籤

    def __open_picture(self):
        global input_image_tk
        filename = filedialog.askopenfilename(
            title='選擇圖片',
            filetypes=[
                ('All Files', ("*.jpg", "*.ppm", "*.bmp", "*.jpeg")),
                ("jpeg files", ("*.jpg", "*.jpeg")),
                ("ppm files", "*.ppm"),
                ('bmp Files', "*.bmp")
            ]
        )  # 獲取文件全路徑
        # tkinter只能打開gif文件，這裏用PIL庫
        input_image = Image.open(filename)
        self.original_input_image = self.__resize(input_image)

        self.__set_first_input_image_to_label(self.original_input_image)
        self.__set_first_output_image_to_label(self.original_input_image)

        self.__release_second_image()

    def __set_first_input_image_to_label(self, image):
        global input_image_tk
        self.input_image = image
        input_image_tk = ImageTk.PhotoImage(image)
        self.first_input_image_label.config(
            image=input_image_tk)  # 用config方法將圖片放置在標籤中

    def __set_first_output_image_to_label(self, image):
        global output_image_tk
        self.output_image = image
        output_image_tk = ImageTk.PhotoImage(image)
        self.first_output_image_label.config(
            image=output_image_tk)  # 用config方法將圖片放置在標籤中

    def __set_second_input_image_to_label(self, image):
        global second_input_image_tk
        self.second_input_image = image
        second_input_image_tk = ImageTk.PhotoImage(image)
        self.second_input_image_label.config(
            image=second_input_image_tk)  # 用config方法將圖片放置在標籤中

    def __set_second_output_image_to_label(self, image):
        global second_output_image_tk
        self.second_output_image = image
        second_output_image_tk = ImageTk.PhotoImage(image)
        self.second_output_image_label.config(
            image=second_output_image_tk)  # 用config方法將圖片放置在標籤中

    def __save_picture(self):
        files = [
            ('All Files', ("*.jpg", "*.ppm", "*.bmp", "*.jpeg")),
            ("jpeg files", ("*.jpg", "*.jpeg")),
            ("ppm files", "*.ppm"),
            ('bmp Files', "*.bmp")
        ]
        filename = filedialog.asksaveasfile(
            title='儲存圖片',
            mode='wb+',
            filetypes=files,
            defaultextension=files
        )

        self.output_image.save(filename)

    def __output_to_gray(self):
        self.__release_second_image()
        self.__set_first_input_image_to_label(self.original_input_image)

        self.__set_first_output_image_to_label(self.input_image.convert('L'))

    def __output_to_gray_histogram(self):
        self.__release_second_image()
        self.__set_first_input_image_to_label(self.original_input_image)

        image_date_name = 'ori_gray_histogram.jpg'
        histogram_image = self.__get_histogram_image(
            self.input_image, image_date_name)

        self.__set_first_output_image_to_label(histogram_image)

    def __get_histogram_image(self, image, image_date_name):
        self.__plot_gray_histogram(image, image_date_name)
        histogram_image = Image.open(image_date_name)
        histogram_image = self.__resize(histogram_image)

        return histogram_image

    def __plot_gray_histogram(self, image, image_date_name):
        gray_input_image = image.convert('L')
        ouput_image_histogram = gray_input_image.histogram()

        plt.clf()
        plt.bar(list(range(256)), ouput_image_histogram)
        plt.title("Image Histogram")
        plt.xlabel("gray level")
        plt.ylabel("frequency")
        plt.savefig(image_date_name)
        plt.close()

    def __output_guassian_noise(self):
        gaussian_noise_sd = self.gaussian_noise_sd.get()

        self.max_image_height = 400

        # 原始圖片的縮小版
        image = self.__resize(self.input_image)
        self.__set_first_input_image_to_label(image)

        # 原始圖片的加入高斯雜訊
        image = image.convert('L')
        image_array, histogram_count = generation_additive_zero_mean_Gaussian_noise(
            gaussian_noise_sd, array(image))
        gausssian_noise_image = Image.fromarray(image_array)
        self.__set_first_output_image_to_label(gausssian_noise_image)

        # 原始圖片的灰階直方圖
        image_date_name = 'ori_gray_histogram.jpg'
        histogram_image = self.__get_histogram_image(
            self.input_image, image_date_name)
        self.__set_second_input_image_to_label(histogram_image)

        # 高斯雜訊圖片的灰階直方圖
        image_date_name = 'guassian_gray_histogram.jpg'
        x = arange(-1, 1.01, 0.01)
        y = array(histogram_count)
        plt.clf()
        plt.bar(x, y, 0.01)
        plt.title("Gaussian Noise Histogram")
        plt.savefig(image_date_name)
        plt.close()

        histogram_image = Image.open(image_date_name)
        histogram_image = self.__resize(histogram_image)

        self.__set_second_output_image_to_label(histogram_image)

        self.max_image_height = 850

    def __release_second_image(self):
        self.second_input_image_label.config(image='')
        self.second_output_image_label.config(image='')

    def __resize(self, image):
        [image_width, image_height] = image.size

        if image_width > self.max_image_width and image_height > self.max_image_height:
            if image_width > image_height:
                image_width, image_height = self.__resize_with_width(
                    image_width, image_height)
            else:
                image_width, image_height = self.__resize_with_height(
                    image_width, image_height)

        elif image_width > self.max_image_width:
            image_width, image_height = self.__resize_with_width(
                image_width, image_height)

        elif image_height > self.max_image_height:
            image_width, image_height = self.__resize_with_height(
                image_width, image_height)

        image = image.resize((image_width, image_height), Image.ANTIALIAS)

        return image

    def __resize_with_width(self, image_width, image_height):
        n = image_width / self.max_image_width
        image_width = self.max_image_width
        image_height = image_height / n

        return int(image_width), int(image_height)

    def __resize_with_height(self, image_width, image_height):
        n = image_height / self.max_image_height
        image_height = self.max_image_height
        image_width = image_width / n

        return int(image_width), int(image_height)
