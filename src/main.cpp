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
	    std::cout << "==";
		statement = (value_a == value_b);
		break;
	case 1:
		    std::cout << "!=";

		statement = (value_a != value_b);
		break;
	case 2:
		    std::cout << ">=";

		statement = (value_a >= value_b);
		break;
	case 3:
		    std::cout << ">";

		statement = (value_a > value_b);
		break;
	case 4:
		    std::cout << "<=";

		statement = (value_a <= value_b);
		break;
	case 5:
        std::cout << "<";
		statement = (value_a < value_b);
		break;
	}
	return statement;
}
long double arithmatic(int operand, long double value_a, long double value_b) {
	long double result;
	switch (operand) {
	case 0:
	    std::cout << "+";
		result = value_a + value_b;
		break;
	case 1:
        std::cout << "-";
		result = value_a - value_b;
		break;
	case 2:
        std::cout << "*";
		result = value_a * value_b;
		break;
	case 3:
        std::cout << "/";
		result = value_a / value_b;
		break;
	case 4:
        std::cout << "^";
		result = pow(value_a, value_b);
		break;
	}
	return result;
}
long double process(long double *afex_array, bool debug) {
	int index = 0;
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

			if(debug){std::cout << "COPY *" << index_a << " (" << afex_array[index_a] << ") -> *" << index_b << std::endl;}
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

            if(debug){std::cout << "MATHOP *" << index_a << " ("<<  value_a << ") ";}
			//Calculate result in arithmatic function and store to afex array result index
			afex_array[index_result] = arithmatic(afex_operator, value_a, value_b);
			//std::cout << "math\n";
            if(debug){std::cout << " *" << index_b <<" (" << value_b << ")" << " -> *" << index_result << std::endl;}

			//update index
			index = index + 5;

			break;
		case 2:
			//Determine operator
			afex_operator = afex_array[index + 1];

			//determine index locations
			index_a = afex_array[index + 2];
			index_b = afex_array[index + 3];
			goto_index = afex_array[index + 4];

			//determine operands;
			value_a = afex_array[index_a];
			value_b = afex_array[index_b];

			if(debug){std::cout << "TERNARY *" << index_a << " (" << value_a << ") ";}

			//Get boolean result
			result = logic(afex_operator, value_a, value_b);

            if(debug){std::cout << " *" << index_b << " (" << value_b << ") | GOTO " << goto_index << " IF FALSE | RESULT: " << result << "\n";}

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
            if(debug){std::cout << "GOTO " << index << "\n";}

			break;
		case 4:
			value = afex_array[0];
            if(debug){std::cout << "PRINT" << "\n";}

			std::cout << std::setprecision(50) << value << std::endl;
			index++;
			break;
		case 5:
			if(debug){std::cout << "terminating" << std::endl;}

			return 0;
		default:
			if(debug){std::cout << "error accessing index " << index << std::endl << "value" << afex_array[index] << std::endl;}
			return 0;
		}
    //std::cin.get();
	}
	std::cout << "River: process terminated\n";
	return 0;
}

//File processing functions
void unpack(std::string path, bool debug) {
	long double array[512]; //Fix this to be a vector FIXME
	std::ifstream file;
	file.open(path);

	long double value; 
	for (int i = 0; i < 512; i++) {
		file >> value;
		array[i] = value;
           if(debug){std::cout << "[" << i << " " << value << "]\n";}
	}

	process(array, debug);
}
int main(int argc, char *argv[])
{
bool debug = false;
std::cout << "River Build 0.1\n";
unpack(argv[1], debug);
}