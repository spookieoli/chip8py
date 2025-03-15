import tkinter
from keyboard import Keyboard


class Screen(tkinter.Canvas):
    def __init__(self, title: str, width: int, height: int, screen_multiplier: int, keyboard: Keyboard):
        """
        Represents a graphical window for rendering a screen with pixel-based drawing
        and responding to keyboard events. It uses tkinter for graphical rendering
        and manages pixel data in a byte array format.

        :param title: The title of the tkinter window.
        :type title: str
        :param width: Number of pixels in the horizontal dimension of the screen.
        :type width: int
        :param height: Number of pixels in the vertical dimension of the screen.
        :type height: int
        :param screen_multiplier: Factor by which each logical pixel is scaled
            for rendering to the screen, defining the size of each pixel visually.
        :type screen_multiplier: int
        :param keyboard: An instance of the Keyboard class to handle user input.
        :type keyboard: Keyboard
        """

        # create a tkinter window
        master = tkinter.Tk()
        master.title(title)
        master.resizable(False, False)
        master.geometry(f"{width * screen_multiplier}x{height * screen_multiplier}")

        # Call super
        super().__init__(master, width=width * screen_multiplier, height=height * screen_multiplier, bg="black")

        # add the keyboard to the screen
        self._keyboard = keyboard

        # map the keyevvents to the keyboard
        self.bind("<Key>", self._keyboard.key_event)
        self.bind("<KeyRelease>", self._keyboard.key_event)
        self.focus_set()

        # set geometry instance vars
        self._width = width
        self._height = height
        self._screen_multiplier = screen_multiplier
        self._pixel_size = screen_multiplier

        # represent screen as Byte array
        self._pixel = bytearray(width * height)

        # add the canvas to the master
        self.pack()

        # initially clear the screen
        self.clear()

    def set_pixel(self, x: int, y: int) -> bool:
        """
        Flips the state of a pixel and returns True if the pixel was previously set.

        This function toggles the state (0 or 1) of a pixel at `(x, y)` and
        returns `True` if the pixel was set to 1 before the operation, and `False`
        otherwise.

        :param x: Horizontal coordinate of the pixel.
        :type x: int
        :param y: Vertical coordinate of the pixel.
        :type y: int
        :return: True if the pixel was previously set (1), False otherwise.
        :rtype: bool
        """
        index = x + y * self._width
        was_set = self._pixel[index] == 1
        self._pixel[index] ^= 1
        return was_set

    def is_pixel_set(self, x: int, y: int) -> bool:
        """
        Checks if a specific pixel at the given coordinates (x, y) is set or not.

        The function determines whether a pixel is "set" based on a pre-defined internal
        representation of the object's pixel array and the object's width. Pixels are
        accessed via the equation ``x + y * self._width`` and the function returns
        a boolean indicating the state of the pixel.

        :param x: The horizontal coordinate of the pixel to check.
                  It indicates the column index in the 2D pixel representation.
        :type x: int
        :param y: The vertical coordinate of the pixel to check.
                  It indicates the row index in the 2D pixel representation.
        :type y: int
        :return: ``True`` if the pixel at the specified coordinates is set, otherwise ``False``.
        :rtype: bool
        """
        return bool(self._pixel[x + y * self._width])

    def draw_sprite(self, x: int, y: int, sprite: bytearray) -> bool:
        """
        Draws a sprite onto a display at the specified coordinates (x, y) using
        the provided sprite data represented as a bytearray. The sprite's bits
        are drawn sequentially, with a bit value of `1` indicating an active
        pixel and a bit value of `0` leaving the pixel unchanged. If any
        existing pixels are unset as a result of this drawing operation (i.e.,
        XOR collision detection), the method returns `True`. Otherwise, it
        returns `False`.

        :param x: The x-coordinate where the sprite should be drawn.
        :type x: int
        :param y: The y-coordinate where the sprite should be drawn.
        :type y: int
        :param sprite: The sprite data to be drawn, represented as an advance
           bytearray, where each byte corresponds to one horizontal 8-pixel
           row of the sprite.
        :type sprite: bytearray
        :return: A boolean indicating whether any previously set pixels were
            erased as a result of the drawing operation.
        :rtype: bool
        """
        erased = False
        for j, byte in enumerate(sprite):
            for i in range(8):
                if byte & (0x80 >> i):
                    if self.set_pixel((x + i) % self._width, (y + j) % self._height):
                        erased = True
        return erased

    def write_screen(self) -> None:
        """
        Renders and displays the screen based on the current state of pixels. For each pixel
        that is set, a rectangle is created on the canvas at the corresponding position.
        """
        self.clear()
        # Get a list of all pixels to draw
        pixels_to_draw = self.compute_pixels_to_draw(self._height, self._width, self.is_pixel_set)

        for x, y in pixels_to_draw:
            x1 = x * self._screen_multiplier
            y1 = y * self._screen_multiplier
            x2 = (x + 1) * self._pixel_size
            y2 = (y + 1) * self._pixel_size
            self.create_rectangle(x1, y1, x2, y2, fill="white", outline="")

        # Refresh the display
        self.update_idletasks()
        self.update()

    def compute_pixels_to_draw(self, height, width, is_pixel_set_func):
        """
        Precomputes all set pixels to draw using Numba for performance.
        :param height: Screen height.
        :param width: Screen width.
        :param is_pixel_set_func: Function to check if a pixel is set (works as a callable).
        :return: List of (x, y) coordinates for pixels to draw.
        """
        pixels = []
        for y in range(height):
            for x in range(width):
                if is_pixel_set_func(x, y):
                    pixels.append((x, y))
        return pixels

    def clear(self):
        """
        Clear the screen to black
        :return:
        """
        self.delete(tkinter.ALL)

    def clear_screen_array(self) -> None:
        self._pixel = bytearray(self._width * self._height)
