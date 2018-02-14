#include "Bot.h"
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void Bot::findEnemyShip(Point & shipLocation, bool & found, Direction & shipDirection) {
	for (int x = 0; x < size; x++) {
		for (int y = 0; y < size; y++) {
			if (map[x][y].damaged) {
				found = true;
				shipDirection.horizontal = false;
				shipDirection.vertical = false;
				// A case to check if the iterator is in the left edge of the array
				// x v v v
				// x v v v
				// x v v v
				// x v v v
				// v is the acceptable case
				if (x > 0) {
					if (map[x - 1][y].damaged)
						shipDirection.horizontal = true;
				}
				// A case to check if the iterator is in the right edge of the array
				// v v v x
				// v v v x
				// v v v x
				// v v v x
				// v is the acceptable case
				if (x < size - 1) {
					if (map[x + 1][y].damaged)
						shipDirection.horizontal = true;
				}
				// A case to check if the iterator is in the top edge of the array
				// x x x x
				// v v v v
				// v v v v
				// v v v v
				// v is the acceptable case
				if (y > 0) {
					if (map[x][y - 1].damaged)
						shipDirection.vertical = true;
				}
				// A case to check if the iterator is in the bottom edge of the array
				// v v v v
				// v v v v
				// v v v v
				// x x x x
				// v is the acceptable case
				if (y < size - 1) {
					if (map[x][y + 1].damaged) {
						shipDirection.vertical = true;
					}
				}

				// Check if there are no damaged ship surrounding the are
				// Because the minimum size of ship is 3
				// If the bots only find a dot of damaged ship in the area
				// There must be a surrounding ship
				if (!shipDirection.horizontal && !shipDirection.vertical && found) {
					shipLocation.x = x;
					shipLocation.y = y;
					break;
				}

				// Case if there is still a possibility that the ship exist
				// But it is not 100% as there is still a chance that the ship
				// has already been destroyed
				if (shipDirection.horizontal) {
					// Check if we iterate through the horizontal axis
					// Will we find other damaged ship or not
					shipDirection.right = true;
					shipDirection.left = true;
					if (x == 0)
						shipDirection.left = false; // Can't find to the left of starting point
					else if (x == size - 1)
						shipDirection.right = false; // Can't find to the right of starting point
					// Checking to the left of starting point
					checkLeft(x, y, shipDirection.left, shipDirection.right);
					// Checking to the right of starting point
					checkRight(x, y, shipDirection.left, shipDirection.right);
					if (!shipDirection.left && !shipDirection.right) {
						shipDirection.horizontal = false;
						found = false;
					}
				}
				if (shipDirection.vertical) {
					// Check if we iterate through the vertical axis
					// Will we find other damaged ship or not
					shipDirection.up = true;
					shipDirection.down = true;
					if (y == 0)
						shipDirection.down = false; // Can't find above the starting point
					else if (y == size - 1)
						shipDirection.up = false; // Can't find below the starting point
					// Check below the starting point
					checkBelow(x, y, shipDirection.up, shipDirection.down);
					// Check above the starting point
					checkAbove(x, y, shipDirection.up, shipDirection.down);
					if (!shipDirection.up && !shipDirection.down) {
						shipDirection.vertical = false;
						found = false;
					}
				}
				if (found) {
					shipLocation.x = x;
					shipLocation.y = y;
					break;
				}
			}
		}
		if (found) break;
	}
}

Point Bot::getShotLocation() {
	bool found = false;
	Point shipLocation(-1, -1);
	Direction shipDirection{};
	findEnemyShip(shipLocation, found, shipDirection);
	Point shotLocation(shipLocation);

			cout << "cek" << endl;


	const auto & ships = state["PlayerMap"]["Owner"]["Ships"];
	
	if (	found && 
			string(ships[4]["ShipType"].GetString()) == "Cruiser" && 
			!ships[4]["Destroyed"].GetBool() && 
			ships[4]["Weapons"][1]["EnergyRequired"].GetInt() <= state["PlayerMap"]["Owner"]["Energy"].GetInt() &&
			validCrossShotHorizontal(shotLocation)
		) {

			mode = 6;
	}

	else if (	found && 
				string(ships[1]["ShipType"].GetString()) == "Destroyer" && 
				!ships[1]["Destroyed"].GetBool() &&
				ships[1]["Weapons"][1]["EnergyRequired"].GetInt() <= state["PlayerMap"]["Owner"]["Energy"].GetInt() &&
				validDoubleShotVertical(shotLocation)
			) {

			mode = 2;
	}

	else if (	found && 
				string(ships[1]["ShipType"].GetString()) == "Destroyer" && 
				!ships[1]["Destroyed"].GetBool() &&
				ships[1]["Weapons"][1]["EnergyRequired"].GetInt() <= state["PlayerMap"]["Owner"]["Energy"].GetInt() &&
				validCrossShotHorizontal(shotLocation)
			) {
			
			mode = 3;
	}

	else if (found) {
		// If the ship is not vertical or horizontal
		// Meaning there is no surrounding damaged or missed tile
		// Bots will check the closest tile in this order
		// left, right, down, up
		if (!shipDirection.horizontal && !shipDirection.vertical) {
			if (shotLocation.x > 0 && !map[shotLocation.x - 1][shotLocation.y].missed)
				shotLocation.x--;
			else if (shotLocation.x < size - 1 && !map[shotLocation.x + 1][shotLocation.y].missed)
				shotLocation.x++;
			else if (shotLocation.y > 0 && !map[shotLocation.x][shotLocation.y - 1].missed)
				shotLocation.y--;
			else shotLocation.y++;
		}
		// If the ship is horizontal
		// Meaning there is damaged part to the right or to the left of the ship
		// Bot will check the rightmost tile first
		// and then the leftmost tile
		else if (shipDirection.horizontal) {
			if (shipDirection.right) {
				while (map[shotLocation.x][shotLocation.y].damaged)
					shotLocation.x++;
			}
			else if (shipDirection.left) {
				while (map[shotLocation.x][shotLocation.y].damaged)
					shotLocation.x--;
			}
		}
		// If the ship is vertical
		// Meaning there is damaged part above or bellow the ship
		// Bot will check above the ship first
		// and then below the ship
		else {
			if (shipDirection.up) {
				while (map[shotLocation.x][shotLocation.y].damaged)
					shotLocation.y++;
			}
			else if (shipDirection.down) {
				while (map[shotLocation.x][shotLocation.y].damaged)
					shotLocation.y--;
			}
		}
	}

	return shotLocation;
}

rapidjson::Document Bot::parseState() {
	ifstream ifs(workingDirectory + "/" + stateFilename);
	stringstream buffer;
	buffer << ifs.rdbuf();
	auto bufferString = buffer.str();
	rapidjson::Document jsonDoc;
	jsonDoc.Parse(bufferString.c_str());
	return jsonDoc;
}

void Bot::fireShot() {
	random_device rd;
	default_random_engine generator(rd());
	Direction shipDirection{};
	Point shotLocation(getShotLocation());
	if (!shotLocation.valid()) {
		uniform_int_distribution<int> distribution(0, validRandomLocation.size() - 1);

		srand (time(NULL));

		int i = rand() % validRandomLocation.size();

		shotLocation.x = validRandomLocation.at(i).x;
		shotLocation.y = validRandomLocation.at(i).y;
		cout << shotLocation.x << endl;
		cout << shotLocation.y << endl;
		/*
		while (validShotLocation(shotLocation)) {
			cout << "y: " << shotLocation.x << endl;
			cout << "x: " << shotLocation.y << endl;
			cout << "damaged: " << map[shotLocation.x][shotLocation.y].damaged << endl;
			cout << "missed: " << map[shotLocation.x][shotLocation.y].missed << endl;
			cout << "shiledHit: " << map[shotLocation.x][shotLocation.y].shieldHit << endl;
			shotLocation.x = validRandomLocation.at(distribution(generator)).x;
			shotLocation.y = validRandomLocation.at(distribution(generator)).y;
		}
		*/
		const auto& ships = state["PlayerMap"]["Owner"]["Ships"];
		cout << "FOO" << endl;
		for (auto it = ships.Begin(); it != ships.End(); it++) {
			const auto& ship = (*it);
			
			if (string(ship["ShipType"].GetString()) == "Battleship" && !ship["Destroyed"].GetBool()) {
				if (ship["Weapons"][1]["EnergyRequired"].GetInt() <= state["PlayerMap"]["Owner"]["Energy"].GetInt() && 
					validCrossShotDiagonal(shotLocation)
				)
					mode = 5;
			}

			else if (string(ship["ShipType"].GetString()) == "Carrier" && !ship["Destroyed"].GetBool()) {
				if (ship["Weapons"][1]["EnergyRequired"].GetInt() <= state["PlayerMap"]["Owner"]["Energy"].GetInt() &&
					validCornerShot(shotLocation) &&
					!validCrossShotDiagonal(shotLocation)
				)
					mode = 4;
			}						

			else if (string(ship["ShipType"].GetString()) == "Submarine" && !ship["Destroyed"].GetBool()) {
				if (ship["Weapons"][1]["EnergyRequired"].GetInt() <= state["PlayerMap"]["Owner"]["Energy"].GetInt() &&
					!validCrossShotHorizontal(shotLocation) &&
					!validCrossShotDiagonal(shotLocation) &&
					!validCornerShot(shotLocation)
				)
					mode = 7;
			}

		}
				
	}

	cout << shotLocation.x << endl;
	cout << shotLocation.y << endl;

	ofstream ofs(workingDirectory + "/" + commandFilename);
	ofs << mode << "," << shotLocation.x << "," << shotLocation.y << "\n";
}

bool Bot::validCrossShotDiagonal(Point & shotLocation) {
	if (shotLocation.x == 0 || shotLocation.x == size - 1 || shotLocation.y == 0 || shotLocation.y == size - 1)
		return false;
	else {
		if (!map[shotLocation.x + 1][shotLocation.y + 1].missed && 
			!map[shotLocation.x + 1][shotLocation.y - 1].missed &&
			!map[shotLocation.x - 1][shotLocation.y + 1].missed &&
			!map[shotLocation.x - 1][shotLocation.y + 1].missed &&
			!map[shotLocation.x][shotLocation.y].missed &&
			!map[shotLocation.x + 1][shotLocation.y + 1].damaged && 
			!map[shotLocation.x + 1][shotLocation.y - 1].damaged &&
			!map[shotLocation.x - 1][shotLocation.y + 1].damaged &&
			!map[shotLocation.x - 1][shotLocation.y + 1].damaged &&
			!map[shotLocation.x][shotLocation.y].damaged &&
			!map[shotLocation.x + 1][shotLocation.y + 1].shieldHit && 
			!map[shotLocation.x + 1][shotLocation.y - 1].shieldHit &&
			!map[shotLocation.x - 1][shotLocation.y + 1].shieldHit &&
			!map[shotLocation.x - 1][shotLocation.y + 1].shieldHit &&
			!map[shotLocation.x][shotLocation.y].shieldHit
		)
			return true;
		return false;
	}
}

bool Bot::validDoubleShotHorizontal(Point & shotLocation) {
	if (shotLocation.x == 0 || shotLocation.x == size - 1)
		return false;
	else {
		if (!map[shotLocation.x + 1][shotLocation.y].missed &&
			!map[shotLocation.x - 1][shotLocation.y].missed &&
			!map[shotLocation.x + 1][shotLocation.y].damaged &&
			!map[shotLocation.x - 1][shotLocation.y].damaged &&
			!map[shotLocation.x + 1][shotLocation.y].shieldHit &&
			!map[shotLocation.x - 1][shotLocation.y].shieldHit
		)
			return true;
		return false;
	}
}

bool Bot::validDoubleShotVertical(Point & shotLocation) {
	if (shotLocation.x == 0 || shotLocation.x == size - 1)
		return false;
	else {
		if (!map[shotLocation.x][shotLocation.y + 1].missed &&
			!map[shotLocation.x][shotLocation.y - 1].missed &&
			!map[shotLocation.x][shotLocation.y + 1].damaged &&
			!map[shotLocation.x][shotLocation.y - 1].damaged &&
			!map[shotLocation.x][shotLocation.y + 1].shieldHit &&
			!map[shotLocation.x][shotLocation.y - 1].shieldHit
		)
			return true;
		return false;
	}
}

bool Bot::validCrossShotHorizontal(Point & shotLocation) {
	if (shotLocation.x == 0 || shotLocation.x == size - 1 || shotLocation.y == 0 || shotLocation.y == size - 1)
		return false;
	else {
		if (!map[shotLocation.x + 1][shotLocation.y].missed && 
			!map[shotLocation.x - 1][shotLocation.y].missed &&
			!map[shotLocation.x][shotLocation.y - 1].missed &&
			!map[shotLocation.x][shotLocation.y + 1].missed &&
			!map[shotLocation.x][shotLocation.y].missed &&
			!map[shotLocation.x + 1][shotLocation.y].damaged && 
			!map[shotLocation.x - 1][shotLocation.y].damaged &&
			!map[shotLocation.x][shotLocation.y - 1].damaged &&
			!map[shotLocation.x][shotLocation.y + 1].damaged &&
			!map[shotLocation.x][shotLocation.y].damaged &&
			!map[shotLocation.x + 1][shotLocation.y].shieldHit && 
			!map[shotLocation.x - 1][shotLocation.y].shieldHit &&
			!map[shotLocation.x][shotLocation.y - 1].shieldHit &&
			!map[shotLocation.x][shotLocation.y + 1].shieldHit &&
			!map[shotLocation.x][shotLocation.y].shieldHit
		)
			return true;
		return false;
	}
}

bool Bot::validCornerShot(Point & shotLocation) {
	if (shotLocation.x == 0 || shotLocation.x == size - 1 || shotLocation.y == 0 || shotLocation.y == size - 1)
		return false;
	else {
		if (!map[shotLocation.x + 1][shotLocation.y + 1].missed && 
			!map[shotLocation.x + 1][shotLocation.y - 1].missed &&
			!map[shotLocation.x - 1][shotLocation.y + 1].missed &&
			!map[shotLocation.x - 1][shotLocation.y + 1].missed &&
			!map[shotLocation.x + 1][shotLocation.y + 1].damaged && 
			!map[shotLocation.x + 1][shotLocation.y - 1].damaged &&
			!map[shotLocation.x - 1][shotLocation.y + 1].damaged &&
			!map[shotLocation.x - 1][shotLocation.y + 1].damaged &&
			!map[shotLocation.x + 1][shotLocation.y + 1].shieldHit && 
			!map[shotLocation.x + 1][shotLocation.y - 1].shieldHit &&
			!map[shotLocation.x - 1][shotLocation.y + 1].shieldHit &&
			!map[shotLocation.x - 1][shotLocation.y + 1].shieldHit 
		)
			return true;
		return false;
	}	
}

void Bot::placeShips() {
	ofstream ofs(workingDirectory + "/" + placeFilename);
	ofs << "Carrier 1 1 East\n";
	ofs << "Battleship 7 7 South\n";
	ofs << "Cruiser 9 0 North\n";
	ofs << "Submarine 4 4 West\n";
	ofs << "Destroyer 0 9 East\n";
}

bool Bot::validShotLocation(Point & shotLocation) {
	return (shotLocation.x + shotLocation.y) % 2 == 0 &&
		!map[shotLocation.x][shotLocation.y].damaged &&
		!map[shotLocation.x][shotLocation.y].missed &&
		!map[shotLocation.x][shotLocation.y].shieldHit;
}

void Bot::checkLeft(int startingX, int startingY, bool & left, bool & right) {
	int x = startingX - 1;
	while (x >= 0) {
		if (map[x][startingY].missed) {
			left = false;
			break;
		}
		else if (!map[x][startingY].damaged)
			break;
		x--;
		if (x == -1)
			left = false;
	}
}

void Bot::checkRight(int startingX, int startingY, bool & left, bool & right) {
	int x = startingX + 1;
	while (x < size) {
		if (map[x][startingY].missed) {
			right = false;
			break;
		}
		else if (!map[x][startingY].damaged)
			break;
		x++;
		if (x == size)
			right = false;
	}
}

void Bot::checkBelow(int startingX, int startingY, bool & up, bool & down) {
	int y = startingY - 1;
	while (y >= 0) {
		if (map[startingX][y].missed) {
			down = false;
			break;
		}
		else if (!map[startingX][y].damaged)
			break;
		y--;
		if (y == -1)
			down = false;
	}
}

void Bot::checkAbove(int startingX, int startingY, bool & up, bool & down) {
	int y = startingY + 1;
	while (y < size) {
		if (map[startingX][y].missed) {
			up = false;
			break;
		}
		else if (!map[startingX][y].damaged)
			break;
		y++;
		if (y == size)
			up = false;
	}
}

Bot::Bot(string workingDirectory) {
	this->workingDirectory = workingDirectory;
	commandFilename = "command.txt";
	placeFilename = "place.txt";
	stateFilename = "state.json";
	state = parseState();
	size = state["MapDimension"].GetInt();
	cout << "Cek" << endl;
	// Allocate a new memory for map
	map = new Square * [size];
	for (int i = 0; i < size; i++)
		map[i] = new Square[size];
	work();
}

void Bot::work() {
	parseMap();
	if (state["Phase"].GetInt() == 1)
		placeShips();
	else
		fireShot();
}

void Bot::parseMap() {
	const auto& cells = state["OpponentMap"]["Cells"];

	for (auto it = cells.Begin(); it != cells.End(); it++) {
		const auto& cell = (*it);

		// Get all the corresponding coordinates
		int x = cell["X"].GetInt();
		int y = cell["Y"].GetInt();

		map[x][y].damaged = cell["Damaged"].GetBool();
		map[x][y].missed = cell["Missed"].GetBool();
		map[x][y].shieldHit = cell["ShieldHit"].GetBool();

		Point shotLocation(x, y);

		if (validShotLocation(shotLocation)) {
			cout << "x: " << shotLocation.x << endl;
			cout << "y: " << shotLocation.y << endl;
			validRandomLocation.push_back(shotLocation);
		}
	}
}
