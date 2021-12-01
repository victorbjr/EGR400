from Constants import *
from pygame.math import Vector2


def _unitsToPixels(self, srcPos):
		srcPos = self._toVector(srcPos)
		src = np.float32([[srcPos.x, srcPos.y]])
		src = np.array([src])

		out = cv2.perspectiveTransform(src, self.u2pTranformMatrix)
		return Vector2(int(out[0][0][0]), int(out[0][0][1]))

def _pixelsToUnits(self, srcPos): #pixelpostion is input
		srcPos = self._toVector(srcPos)
		src = np.float32([[srcPos.x, srcPos.y]])
		src = np.array([src])

		out = cv2.perspectiveTransform(src, self.p2uTranformMatrix)
		return Vector2(int(out[0][0][0]), int(out[0][0][1]))

def _toVector(self, vector):
		if isinstance(vector, Vector2):
			return Vector2(int(vector.x), int(vector.y))
		else:
			return Vector2(int(vector[0]), int(vector[1]))


def u2pX(x):
    return round(u2pDist(x) + X_OFF)


def u2pY(y):
    try:
        return round(u2pDist(-y) + Y_OFF)
    except:
        print('NaN!')
        return 0


def u2pXY(pos):
    pos = toList(pos)
    return (u2pX(pos[0]), u2pY(pos[1]))


def u2pDist(distance):
    return round(distance * UNITS_TO_PIXELS_SCALE)


def p2uX(x):
    return p2uDist(x - X_OFF)


def p2uY(y):
    return p2uDist(-(y - Y_OFF))


def p2uXY(pos):
    pos = toList(pos)
    return (p2uX(pos[0]), p2uY(pos[1]))


def p2uDist(distance):
    return distance / UNITS_TO_PIXELS_SCALE

def toList(vector, roundDigit = 0):
	if isinstance(vector, Vector2):
		return [int(vector.x) if roundDigit == 0 else round(vector.x, roundDigit), int(vector.y) if roundDigit == 0 else round(vector.y, roundDigit)]
	else:
		return [int(vector[0]) if roundDigit == 0 else round(vector[0], roundDigit), int(vector[1]) if roundDigit == 0 else round(vector[1], roundDigit)]

#Constants
X_OFF=
Y_OFF=
UNITS_TO_PIXELS_SCALE=8.63;
distance, vector, pos, x, y, srcPos
