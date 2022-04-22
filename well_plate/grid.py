import numpy as np


class GridPattern:

    def __init__(self,
                 center: np.ndarray = None,
                 corner: np.ndarray = None,
                 x_length: (int, float) = 10,
                 y_length: (int, float) = None,
                 x_count: int = None,
                 y_count: int = None,
                 num_points: int = 25):
        """
        Generates x,y locations for a grid pattern
        Parameters
        ----------
        center: np.ndarray[2]
            center of pattern
            default is [0, 0]
            * only give one center or corner
        corner: np.ndarray[2]
            corner of pattern [x, y]
            * only give one center or corner
        x_length: int, float
            x span of the pattern
        y_length: int, float
            y span of the pattern
            * if not given, it will make square
        x_count: int
             number of rows (x-direction) in pattern
             * if not provide sqrt(num_points) will be used
        y_count: int
            number of columns (y-direction) in pattern
            * if not provide sqrt(num_points) will be used
            * If offset_op=True, some layers will have "col-1" columns
        num_points: int
            number of points
            * do not provide if col and row are provided
        """
        self.x_length = x_length
        if y_length is None:
            self.y_length = x_length  # make a square
        else:
            self.y_length = y_length

        if y_count is None and x_count is not None:
            self.y_length = 0
        elif y_count is not None and x_count is None:
            self.x_length = 0

        self.x_count = None
        self.y_count = None
        self.num_points = None
        self._set_counts(x_count, y_count, num_points)

        self.corner = None
        self.center = None
        self._set_center_corner(center, corner)

        self._xy_points: np.ndarray = np.empty((self.num_points, 2))
        self._get_points()

    @property
    def xy_points(self):
        return self._xy_points

    def _set_counts(self, x_count, y_count, num_points):
        if x_count is None and y_count is None:
            self.x_count = int(np.sqrt(num_points))  # make square with equal number points in grid
            self.y_count = self.x_count
            if (self.x_count * self.y_count) != num_points:
                import warnings
                warnings.warn(
                    f"'num_points' changed! The given num_points ({num_points}) was adjusted/set to "
                    f"{self.num_points} to get a complete pattern.")
        elif x_count is not None and y_count is not None:
            self.x_count = x_count
            self.y_count = y_count
        elif x_count is not None and y_count is None:
            self.x_count = x_count
            self.y_count = 1
        else:  # x_count is None and y_count is not None
            self.x_count = 1
            self.y_count = y_count

        self.num_points = self.x_count * self.y_count

    def _set_center_corner(self, center, corner):
        if corner is not None:
            self.corner = corner
            self.center = self._corner_to_center(self.corner, self.x_length, self.y_length)
        elif center is not None:
            self.center = center
            self.corner = self._center_to_corner(self.center, self.x_length, self.y_length)
        else:
            self.center = np.array([0, 0])
            self.corner = self._center_to_corner(self.center, self.x_length, self.y_length)

    @staticmethod
    def _center_to_corner(center: np.ndarray, x_length: (int, float), y_length: (int, float)) -> np.ndarray:
        """ Calculate the corner x,y position given the center. """
        return np.array([center[0] - x_length / 2, center[1] - y_length / 2])

    @staticmethod
    def _corner_to_center(corner: np.ndarray, x_length: (int, float), y_length: (int, float)) -> np.ndarray:
        """ Calculate the corner x,y position given the center. """
        return np.array([corner[0] + x_length / 2, corner[1] + y_length / 2])

    def _get_points(self):
        """ Main function that calculates grid xy positions. """
        if self.y_count == 1:
            dy = 0
        else:
            dy = self.y_length / (self.y_count - 1)
        if self.x_count == 1:
            dx = 0
        else:
            dx = self.x_length / (self.x_count - 1)

        k = 0
        for i in range(self.y_count):  # loop over row
            for ii in range(self.x_count):  # loop over column
                self.xy_points[k, :] = [
                    self.corner[0] + dx * ii,
                    self.corner[1] + dy * i
                ]
                k += 1
