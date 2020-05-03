//aFex Language Compiler
#include <iostream>
#include <string>
#include <fstream>
#include <iomanip>
#include <cmath>
//Compiler functions

bool logic(int operand, long double value_a, long double value_b) {
	bool statement;
//	std::cout << value_a <<  " [comparator: " << operand << "] " << value_b << std::endl;
	switch (operand) {
	case 0:
		statement = (value_a == value_b);
		break;
	case 1:
		statement = (value_a != value_b);
		break;
	case 2:
		statement = (value_a >= value_b);
		break;
	case 3:
		statement = (value_a > value_b);
		break;
	case 4:
		statement = (value_a <= value_b);
		break;
	case 5:
		statement = (value_a < value_b);
		break;
	}
	return statement;
}
long double arithmatic(int operand, long double value_a, long double value_b) {
	long double result;
	switch (operand) {
	case 0:
		result = value_a + value_b;
		break;
	case 1:
		result = value_a - value_b;
		break;
	case 2:
		result = value_a * value_b;
		break;
	case 3:
		result = value_a / value_b;
		break;
	case 4:
		result = pow(value_a, value_b);
		break;
	}
	return result;
}
long double process(long double *afex_array) {
	int index = 1;
	int index_a;
	int index_b;
	int index_result;
	long double value_a;
	long double value_b;
	int goto_index;
	long double value;
	int afex_operator;
	bool result;
	while (afex_array[index] != 5) { //Cease execution if read 5 (stop)
	//	std::cout << "Index: " << index << std::endl;
		switch (static_cast<int>(afex_array[index])) {
		case 0:
			//Extract parameters
			index_a = afex_array[index + 1];
			index_b = afex_array[index + 2];

			//Copy value at index A into index B;
			afex_array[index_b] = afex_array[index_a];

			//Update index;
			index = index + 3;
			break;
		case 1:
			//Determine operator;
			afex_operator = afex_array[index + 1];

			//Determine index locations
			index_a = afex_array[index + 2];
			index_b = afex_array[index + 3];
			index_result = afex_array[index + 4];

			//determine operands;
			value_a = afex_array[index_a];
			value_b = afex_array[index_b];

			//Calculate result in arithmatic function and store to afex array result index
			afex_array[index_result] = arithmatic(afex_operator, value_a, value_b);
			//std::cout << "math\n";

			//update index
			index = index + 5;
			break;
		case 2:
			//std::cout << "Comparator\n";
			//Determine operator
			afex_operator = afex_array[index + 1];

			//determine index locations
			index_a = afex_array[index + 2];
			index_b = afex_array[index + 3];
			goto_index = afex_array[index + 4];

			//determine operands;
			value_a = afex_array[index_a];
			value_b = afex_array[index_b];

			//Get boolean result
			result = logic(afex_operator, value_a, value_b);

			//Continue if true, otherwise index becomes goto_index value
			if (result == true) {
				index = index + 5;
			}
			else {
				index = goto_index;
			}
			break;
		case 3:
			goto_index = afex_array[index + 1];
			index = goto_index;
			break;
		case 4:
			value = afex_array[0];
			std::cout << std::setprecision(50) << value << std::endl;
			index++;
			break;
		case 5:
			std::cout << "terminating" << std::endl;

			return 0;
		default:
			std::cout << "error accessing index " << index << std::endl << "value" << afex_array[index] << std::endl;
			//return 0;
		}

	}
	std::cout << "River: process terminated\n";
}
//File processing functio
void unpack(std::string path) {
	long double array[512]; //Fix this to be a vector FIXME
	std::ifstream file;
	file.open(path);

	long double value; 
	for (int i = 0; i < 512; i++) {
		file >> value; 
		array[i] = value;
		//std::cout << "[" << value << "],";
	}
	process(array);
}
int main(int argc, char *argv[])
{
std::cout << "River Build 0.1\n";
unpack(argv[1]);
}