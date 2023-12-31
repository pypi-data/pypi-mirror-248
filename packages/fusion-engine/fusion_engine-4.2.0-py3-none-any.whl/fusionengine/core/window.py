import fusionengine.tools.debug as fe_debug
import pygame as pg
import pygame_gui as gui
from pygame.locals import DOUBLEBUF


class Window:
    def __init__(self, title: str, width: int, height: int) -> None:
        self._running = False
        self._fps = 60
        self._quittable = True
        self._clock = pg.time.Clock()

        self.title = title
        self.width = width
        self.height = height

        try:
            self.window = pg.display.set_mode((width, height), DOUBLEBUF, 16)
            pg.display.set_caption(title)

            self.manager = gui.UIManager((width, height))

            program_icon = pg.image.load(fe_debug.DEBUGIMAGE)
            pg.display.set_icon(program_icon)

            self._running = True

        except Exception:
            print("Error: Can't create a window.")

    def change_icon(self, image_path):
        """Changes icon

        Args:
            Icon_Path (str): Path to your icon

        """

        programIcon = pg.image.load(image_path)
        pg.display.set_icon(programIcon)

    def loop(self, your_loop) -> None:
        """A while loop decorator function.

        Args:
            your_loop (callable): Your main loop function
        """
        while self.running():
            your_loop()

    def running(self) -> bool:
        """Returns if the window is running. Used for the main loop.

        Args:
            window: Your window

        Returns:
            bool: returns true if the window is running else false
        """
        self._refresh()
        return self._running

    def set_fps(self, fps: int) -> None:
        """Sets the desired frames per second for the game loop.

        Args:
            fps (int): The desired frames per second
        """
        self._fps = fps

    def get_fps(self) -> int:
        return self._fps

    def force_quit(self) -> None:
        """Force quits the window.
        Specifically, stops and deletes window.
        Args:
            window: Your window
        """
        self._running = False
        del self.window

    def toggle_quittable(self) -> None:
        """Toggles whether the window is quittable."""
        self._quittable = not self._quittable

    def _refresh(self) -> None:
        """Does all things for refreshing window. (Not for the user)

        Args:
            window: Your window
        """

        self.DELTATIME = self._clock.tick(self._fps)

        for event in pg.event.get():
            if event.type == pg.QUIT and self._quittable:
                self._running = False

            self.manager.process_events(event)

        self.manager.update(self.DELTATIME)
        self.manager.draw_ui(self.window)

        pg.display.update()

        self.window.fill((0, 0, 0))
