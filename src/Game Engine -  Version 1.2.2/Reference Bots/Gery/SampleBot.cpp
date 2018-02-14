// C++ Sample Bot for Entelect Challenge 2017


#include <random>
#include <vector>
#include <iostream>
#include <fstream>
#include <sstream>
#include "rapidjson/document.h"
#include "Bot.h"

using namespace std;

int main(int argc, char** argv)
{
	if (argc != 3) {
		cout << "Usage: SampleBot.exe PlayerKey WorkingDirectory" << endl;
		return 1;
	}

	cout << "cek" << endl;
	Bot bot(argv[2]);
	
    return 0;
}
