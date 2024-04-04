import pygame
import random
import numpy as np
import time
import copy
from pymongo import MongoClient

# Database connection
CONNECTION_STRING = "mongodb://localhost:27017"
client = MongoClient(CONNECTION_STRING)
db = client.pdsa
collection = db.sort

BACKGROUND_COLOR = (245, 245, 245)   # Light gray
BAR_COLOR_START = (64, 114, 196)     # Blue
BAR_COLOR_END = (255, 192, 0)        # Yellow
MARK_COLOR_1 = (255, 0, 0)           # Red
MARK_COLOR_2 = (0, 255, 0)           # Green
TEXT_COLOR = (70, 70, 70)            # Dark gray
BUTTON_COLOR = (76, 175, 80)         # Green
BUTTON_HOVER_COLOR = (46, 139, 87)   # Dark green

MAX_IM_SIZE = 5000

class Button:
    def __init__(self, screen, text, x, y, width, height, font_size=24, on_click=None):
        self.screen = screen
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font_size = font_size
        self.on_click = on_click

        self.font = pygame.font.Font(None, self.font_size)
        self.text_surface = self.font.render(self.text, True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.x < mouse_pos[0] < self.x + self.width and self.y < mouse_pos[1] < self.y + self.height:
            pygame.draw.rect(self.screen, BUTTON_HOVER_COLOR, (self.x, self.y, self.width, self.height), border_radius=10)
        else:
            pygame.draw.rect(self.screen, BUTTON_COLOR, (self.x, self.y, self.width, self.height), border_radius=10)

        self.screen.blit(self.text_surface, self.text_rect)

    def isOver(self, pos):
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.isOver(event.pos):
                if self.on_click:
                    self.on_click()

class DataSeq:
    MAX_IM_SIZE = 5000

    def __init__(self, Length, time_interval=1, sort_title="Sorting Visualizer", is_resampling=False, is_sparse=False, fps=25):
        self.data = [x for x in range(Length)]
        if is_resampling:
            self.data = random.choices(self.data, k=Length)
        else:
            self.Shuffle()
        if is_sparse:
            self.data = [x if random.random() < 0.3 else 0 for x in self.data]

        self.length = Length

        self.SetTimeInterval(time_interval)
        self.SetSortType(sort_title)
        self.Getfigure()
        self.InitTime()
        self.Visualize()

    def InitTime(self):
        self.start = time.time()
        self.time = 0
        self.StopTimer()

    def StartTimer(self):
        self.start_flag = True
        self.start = time.time()

    def StopTimer(self):
        self.start_flag = False

    def GetTime(self):
        if self.start_flag:
            self.time = time.time() - self.start

    def SetTimeInterval(self, time_interval):
        self.time_interval = time_interval

    def SetSortType(self, sort_title):
        self.sort_title = sort_title

    def Shuffle(self):
        random.shuffle(self.data)

    def Getfigure(self):
        _bar_lenght = 1
        figure = np.full((self.length * _bar_lenght, self.length * _bar_lenght, 3), BACKGROUND_COLOR, dtype=np.uint8)
        for i in range(self.length):
            val = self.data[i]
            figure[-1 - val * _bar_lenght:, i * _bar_lenght:i * _bar_lenght + _bar_lenght] = self.GetColor(val, self.length)
        self._bar_lenght = _bar_lenght
        self.figure = figure
        size = _bar_lenght * self.length 
        self.im_size = size if size < self.MAX_IM_SIZE else self.MAX_IM_SIZE

    @staticmethod
    def GetColor(val, TOTAL):
        return (
            int(BAR_COLOR_START[0] + (BAR_COLOR_END[0] - BAR_COLOR_START[0]) * val / (2 * TOTAL)),
            int(BAR_COLOR_START[1] + (BAR_COLOR_END[1] - BAR_COLOR_START[1]) * val / (2 * TOTAL)),
            int(BAR_COLOR_START[2] + (BAR_COLOR_END[2] - BAR_COLOR_START[2]) * val / (2 * TOTAL))
        )

    def _set_figure(self, idx, val):
        min_col = idx * self._bar_lenght
        max_col = min_col + self._bar_lenght
        min_row = -1 - val * self._bar_lenght
        self.figure[:, min_col:max_col] = BACKGROUND_COLOR
        self.figure[min_row:, min_col:max_col] = self.GetColor(val, self.length)

    def SetColor(self, img, marks, color):
        for idx in marks:
            min_col = idx * self._bar_lenght
            max_col = min_col + self._bar_lenght
            min_row = -1 - self.data[idx] * self._bar_lenght
            img[min_row:, min_col:max_col] = color

    def Mark(self, img, marks, color):
        self.SetColor(img, marks, color)

    def SetVal(self, idx, val):
        self.data[idx] = val
        self._set_figure(idx, val)

        self.Visualize((idx,))

    def Swap(self, idx1, idx2):
        self.data[idx1], self.data[idx2] = self.data[idx2], self.data[idx1]
        self._set_figure(idx1, self.data[idx1])
        self._set_figure(idx2, self.data[idx2])

        self.Visualize((idx1, idx2))

    def Visualize(self, mark1=None, mark2=None):
        img = self.figure.copy()
        if mark2:
            self.Mark(img, mark2, MARK_COLOR_2)
        if mark1:
            self.Mark(img, mark1, MARK_COLOR_1)

        img = np.transpose(img, (1, 0, 2))
        img = np.flip(img, 0)

        img = pygame.transform.scale(pygame.surfarray.make_surface(img), (self.im_size, self.im_size))

        self.GetTime()
        pygame.font.init()
        font = pygame.font.Font(None, 20)
        text = font.render(self.sort_title + " Time:%02.2fs" % self.time, True, TEXT_COLOR)
        img.blit(text, (20, 20))

        pygame.display.set_caption(self.sort_title)
        pygame.display.get_surface().blit(img, (0, 0))
        pygame.display.update()

        clock = pygame.time.Clock()
        for _ in range(5):
            time.sleep(self.time_interval / 1000 / 5)
            pygame.display.update()
            clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                pygame.quit()
                return

    def Hold(self):
        for idx in range(self.length):
            self.SetVal(idx, self.data[idx])

        self.SetTimeInterval(0)
        self.Visualize()

class SortAlgorithms:
    @staticmethod
    def GetPivot(ds, Left, Right):
        Mid = (Left + Right) // 2
        if ds.data[Left] > ds.data[Right]:
            ds.Swap(Left, Right)
        if ds.data[Left] > ds.data[Mid]:
            ds.Swap(Left, Mid)
        if ds.data[Mid] > ds.data[Right]:
            ds.Swap(Mid, Right)
        ds.Swap(Mid, Right - 1)
        return ds.data[Right - 1]

    @staticmethod
    def Qsort(ds, Left, Right):
        Cutoff = 10
        if Cutoff <= Right - Left:
            Pivot = SortAlgorithms.GetPivot(ds, Left, Right)
            low = Left + 1
            high = Right - 2
            while True:
                while ds.data[low] < Pivot:
                    low += 1
                while ds.data[high] > Pivot:
                    high -= 1
                if low < high:
                    ds.Swap(low, high)
                    low += 1
                    high -= 1
                else:
                    break
            ds.Swap(low, Right - 1)
            SortAlgorithms.Qsort(ds, Left, low - 1)
            SortAlgorithms.Qsort(ds, low + 1, Right)
        else:
            for p in range(Left, Right + 1):
                tmp = ds.data[p]
                i = p
                while i >= 1 and ds.data[i - 1] > tmp:
                    ds.SetVal(i, ds.data[i - 1])
                    i -= 1
                ds.SetVal(i, tmp)

    @staticmethod
    def QuickSort(ds):
        assert isinstance(ds, DataSeq), "Type Error"

        Length = ds.length
        SortAlgorithms.Qsort(ds, 0, Length - 1)

    @staticmethod
    def InsertionSort(ds):
        assert isinstance(ds, DataSeq), "Type Error"

        Length = ds.length
        for i in range(1, Length):
            key = ds.data[i]
            j = i - 1
            while j >= 0 and ds.data[j] > key:
                ds.SetVal(j + 1, ds.data[j])
                j -= 1
            ds.SetVal(j + 1, key)

    @staticmethod
    def SelectionSort(ds):
        assert isinstance(ds, DataSeq), "Type Error"

        Length = ds.length
        for i in range(Length - 1):
            min_idx = i
            for j in range(i + 1, Length):
                if ds.data[j] < ds.data[min_idx]:
                    min_idx = j
            ds.Swap(i, min_idx)

    @staticmethod
    def ShellSort(ds):
        assert isinstance(ds, DataSeq), "Type Error"

        Length = ds.length
        gap = Length // 2
        while gap > 0:
            for i in range(gap, Length):
                temp = ds.data[i]
                j = i
                while j >= gap and ds.data[j - gap] > temp:
                    ds.SetVal(j, ds.data[j - gap])
                    j -= gap
                ds.SetVal(j, temp)
            gap //= 2

    @staticmethod
    def Merge(ds, L, R, RightEnd):
        tmpData = copy.copy(ds.data)
        LeftEnd = R - 1
        i = L
        j = R
        k = L
        while i <= LeftEnd and j <= RightEnd:
            if tmpData[i] < tmpData[j]:
                ds.SetVal(k, tmpData[i])
                i += 1
            else:
                ds.SetVal(k, tmpData[j])
                j += 1
            k += 1
        while i <= LeftEnd:
            ds.SetVal(k, tmpData[i])
            k += 1
            i += 1
        while j <= RightEnd:
            ds.SetVal(k, tmpData[j])
            k += 1
            j += 1

    @staticmethod
    def Sort(ds, L, RightEnd):
        if RightEnd > L:
            mid = (L + RightEnd) // 2
            SortAlgorithms.Sort(ds, L, mid)
            SortAlgorithms.Sort(ds, mid + 1, RightEnd)
            SortAlgorithms.Merge(ds, L, mid + 1, RightEnd)

    @staticmethod
    def MergeSort(ds):
        assert isinstance(ds, DataSeq), "Type Error"

        Length = ds.length
        SortAlgorithms.Sort(ds, 0, Length - 1)

    @staticmethod
    def BubbleSort(ds):
        assert isinstance(ds, DataSeq), "Type Error"

        Length = ds.length
        for i in range(Length - 1, -1, -1):
            for j in range(0, i, 1):
                if ds.data[j] > ds.data[j + 1]:
                    ds.Swap(j, j + 1)

def main():
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sorting Visualizer")

    ds = DataSeq(500, is_sparse=True)

    button_width = WIDTH // 6 - 20
    button_height = 50
    button_x_positions = [10 + (button_width + 10) * i for i in range(6)]
    button_y = HEIGHT - button_height - 20

    def quick_sort_callback():
        SortAlgorithms.QuickSort(ds)

    def merge_sort_callback():
        SortAlgorithms.MergeSort(ds)

    def bubble_sort_callback():
        SortAlgorithms.BubbleSort(ds)

    def insertion_sort_callback():
        SortAlgorithms.InsertionSort(ds)

    def selection_sort_callback():
        SortAlgorithms.SelectionSort(ds)

    def shell_sort_callback():
        SortAlgorithms.ShellSort(ds)

    quick_sort_button = Button(WIN, 'Quick Sort', button_x_positions[0], button_y, button_width, button_height, on_click=quick_sort_callback)
    merge_sort_button = Button(WIN, 'Merge Sort', button_x_positions[1], button_y, button_width, button_height, on_click=merge_sort_callback)
    bubble_sort_button = Button(WIN, 'Bubble Sort', button_x_positions[2], button_y, button_width, button_height, on_click=bubble_sort_callback)
    insertion_sort_button = Button(WIN, 'Insertion Sort', button_x_positions[3], button_y, button_width, button_height, on_click=insertion_sort_callback)
    selection_sort_button = Button(WIN, 'Selection Sort', button_x_positions[4], button_y, button_width, button_height, on_click=selection_sort_callback)
    shell_sort_button = Button(WIN, 'Shell Sort', button_x_positions[5], button_y, button_width, button_height, on_click=shell_sort_callback)

    buttons = [quick_sort_button, merge_sort_button, bubble_sort_button, insertion_sort_button, selection_sort_button, shell_sort_button]

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            for button in buttons:
                button.handle_event(event)

        WIN.fill(BACKGROUND_COLOR)

        for button in buttons:
            button.draw()

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
