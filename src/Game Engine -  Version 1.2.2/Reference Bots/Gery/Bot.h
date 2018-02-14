#pragma once
#include <random>
#include <vector>
#include <iostream>
#include <fstream>
#include <sstream>
#include "Point.h"
#include "rapidjson/document.h"
#include "Square.h"
#include "Direction.h"

using namespace std;

class Bot {
private:
	Square **map;
	string workingDirectory, commandFilename, placeFilename, stateFilename;
	rapidjson::Document state;
	vector<Point> validRandomLocation;
	int size, mode = 1;

	rapidjson::Document parseState();
	Point getShotLocation();
	void findEnemyShip(Point&, bool&, Direction &);
	void parseMap();
	void checkLeft(int, int, bool&, bool&);
	void checkRight(int, int, bool&, bool&);
	void checkAbove(int, int, bool&, bool&);
	void checkBelow(int, int, bool&, bool&);
	bool validShotLocation(Point &);
	bool validCrossShotDiagonal(Point &);
	bool validCornerShot(Point &);
	bool validCrossShotHorizontal(Point &);
	bool validDoubleShotHorizontal(Point &);
	bool validDoubleShotVertical(Point &);
	void fireShot();
	void placeShips();
	void work();
public:
	Bot(string);
};
