import random
import os
import xlsxwriter
import matplotlib.pyplot as plt
import matplotlib.image as mpim


class DataSetBuilder(object):
    def __init__(self, directory):
        self.directory = directory
        self.row = 2
        # genere a random number for the file name
        randomID = random.randint(1, 10000000)
        self.workbook = xlsxwriter.Workbook(
            f"./database/result{randomID}.xlsx")
        self.worksheet = self.workbook.add_worksheet('result1')
        self.COLUMNS = ['A', 'B']
        self.worksheet.write(self.COLUMNS[0]+'1', 'Filename')
        self.worksheet.write(self.COLUMNS[1]+'1', 'Choice')

    def on_key_press(self, event):
        if event.key == 'delete':
            self.delete_images()
        else:
            if event.key == '1':
                self.worksheet.write(self.COLUMNS[1]+str(self.row), 1)
            elif event.key == '0':
                self.worksheet.write(self.COLUMNS[1]+str(self.row), 0)
            else:
                self.worksheet.write(self.COLUMNS[1]+str(self.row), 0)

            self.worksheet.write(self.COLUMNS[0]+str(self.row), self.f)
            self.row += 1
        plt.close()
        return event.key

    def lookup_images(self):
        for filename in os.listdir(self.directory):
            if filename.endswith('.jpg' or '.png' or '.jpeg'):
                self.f = os.path.join(self.directory, filename)
                print(self.f)
                img = mpim.imread(self.f)
                fig = plt.gcf()
                fig.canvas.set_window_title(
                    '1: good , 0: Bad, Delete: Delete Image')
                fig.canvas.mpl_connect('key_press_event', self.on_key_press)

                plt.imshow(img)
                plt.show()

        self.workbook.close()

    def delete_images(self):
        os.remove(self.f)


def main(path):
    dataset = DataSetBuilder(path)
    dataset.lookup_images()


if __name__ == '__main__':

    path = input('Enter the folder containing the images: ')
    path = '.\\images\\'+path
    main(path)
