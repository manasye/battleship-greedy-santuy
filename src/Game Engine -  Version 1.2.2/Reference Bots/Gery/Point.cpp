#include "Point.h"

Point::Point(int x, int y) {
	this->x = x;
	this->y = y;
}

bool Point::valid() {
	return x >= 0 && y >= 0;
}