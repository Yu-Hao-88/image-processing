import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import matplotlib.pyplot as plt


class ImagePlatform():
    def __init__(self) -> None:
        self.max_image_width = 700
        self.max_image_height = 900

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
                                  command=self.__open_picture, bg="white", fg='#0f506d', font=('Courier', 16), width=10, height=1)

        select_buttom.grid(column=1, row=1, sticky="NS")

        save_buttom = tk.Button(self.window, text='儲存圖片',
                                command=self.__save_picture, bg="white", fg='#0f506d', font=('Courier', 16), width=10, height=1)

        save_buttom.grid(column=1, row=2, sticky="NS")

        gray_pricture_buttom = tk.Button(self.window, text='轉為灰階圖',
                                         command=self.__output_to_gray, bg="white", fg='#0f506d', font=('Courier', 16), width=10, height=1)

        gray_pricture_buttom.grid(column=1, row=3, sticky="NS")

        gray_histogram_buttom = tk.Button(self.window, text='灰階直方圖',
                                          command=self.__output_to_gray_histogram, bg="white", fg='#0f506d', font=('Courier', 16), width=10, height=1)

        gray_histogram_buttom.grid(column=1, row=4, sticky="NS")

    def __title_init(self):
        input_image_text = tk.Label(
            self.window, text='input image:', image=None, bg="#0f506d", fg='white', font=('Courier', 16))
        input_image_text.grid(column=0, row=0, sticky="NSEW", ipady=6)

        between_input_output = tk.Frame(self.window, bg="#0f506d")
        between_input_output.grid(column=1, row=0, sticky="NSEW")

        output_image_text = tk.Label(
            self.window, text='output image:', image=None, bg="#0f506d", fg='white', font=('Courier', 16))
        output_image_text.grid(column=2, row=0, sticky="NSEW")

    def __image_init(self):
        self.input_image_show = tk.Label(self.window, text='pictures will show in this place', bg="#fbf2e2",
                                         image=None)  # 創建一個標籤
        self.input_image_show.grid(column=0, row=2, rowspan=100)  # 放置標籤

        self.output_image_show = tk.Label(self.window, text='pictures will show in this place', bg="#fbf2e2",
                                          image=None)  # 創建一個標籤
        self.output_image_show.grid(column=2, row=2, rowspan=100)  # 放置標籤

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
        input_image = self.__resize(input_image)

        self.__set_input_image_to_label(input_image)
        self.__set_output_image_to_label(input_image)

    def __set_input_image_to_label(self, image):
        global input_image_tk
        self.input_image = image
        input_image_tk = ImageTk.PhotoImage(image)
        self.input_image_show.config(
            image=input_image_tk)  # 用config方法將圖片放置在標籤中

    def __set_output_image_to_label(self, image):
        global output_image_tk
        self.output_image = image
        output_image_tk = ImageTk.PhotoImage(image)
        self.output_image_show.config(
            image=output_image_tk)  # 用config方法將圖片放置在標籤中

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
        self.__set_output_image_to_label(self.input_image.convert('L'))

    def __output_to_gray_histogram(self):
        temp_input_image = self.input_image.convert('L')
        ouput_image_histogram = temp_input_image.histogram()

        plt.bar(list(range(256)), ouput_image_histogram)
        plt.title("Image Histogram")
        plt.xlabel("gray level")
        plt.ylabel("frequency")
        plt.savefig("gray_histogram.jpg")
        plt.close()

        self.__set_output_image_to_label(Image.open('gray_histogram.jpg'))

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
