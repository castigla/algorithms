/******************************************************************************
* Project 4: TSP
* Description: algorithm for solving the travelling salesman problem (TSP)
* Sources:
*    - https://en.wikipedia.org/wiki/2-opt
*    - http://www.technical-recipes.com/2012/applying-c-implementations-of-2-opt-to-travelling-salesman-problems/
******************************************************************************/

#include <string>
#include <iostream>
#include <fstream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <cmath>


//data structures
struct City {
    int id;
    int xcoord;
    int ycoord;
};

struct Path {
    std::vector<City> cities;
    int distance;
};

//forward declarations
void twoOptTSP(struct Path& tour);
std::vector<City> twoOptSwap(std::vector<City> route, int i, int k);
int distanceCities(City city1, City city2);
int distanceTotal(std::vector<City>& route);


int main(int argc, char** argv) {
    //Check number of arguments
    if (argc < 2) {
        std::cout << "Did not provide input file as argument\n";
        exit(-1);
    }
    
    //Read input file
    std::string inputFileStr = argv[1];
    std::ifstream inputStream;
    inputStream.open(inputFileStr.c_str());
    if (!inputStream) {
        std::cout << "Unable to open input file " << &inputStream << std::endl;
        exit(1);
    }

    //Store the input graph in a vector using using input file
    struct Path tour;
    while (!inputStream.eof()) {
        struct City inputCity;
        int id = -1;
        int xcoord = -1;
        int ycoord = -1;
        inputStream >> id >> xcoord >> ycoord;
        inputCity.id = id;
        inputCity.xcoord = xcoord;
        inputCity.ycoord = ycoord;
        if (id != -1 && xcoord != -1 && ycoord != -1) {
            tour.cities.push_back(inputCity);
        }
    }
    inputStream.close();
    int initialDistance = distanceTotal(tour.cities);
    tour.distance = initialDistance;
    

    //Start timer
    clock_t start = clock();
    
        //Run algorithm
        twoOptTSP(tour);
   
    
    //End timer
    clock_t end = clock();

    //Calculate time in seconds
    long long clockCycles = end - start;
    float timeSeconds = ((float)clockCycles)/CLOCKS_PER_SEC;
    
    //print to screen for user
    std::cout << "\nTime elapsed: " << timeSeconds << " seconds\n";
    std::cout << "\nTour Length: " << tour.distance << "\n";
    
    //create output file
    std::string outputFileStr = argv[1];
    outputFileStr.append(".tour");
    std::ofstream outputStream;
    outputStream.open(outputFileStr.c_str());
    
    //write tour length to output file
    outputStream << tour.distance << "\r\n";
    
    //write tour cities to output file line by line
    for (int i = 0; i < tour.cities.size(); ++i) {
        outputStream << tour.cities[i].id << "\r\n";
    }
    
    //Close output file
    outputStream.close();
    
    return 0;
}

/**********************************************************************************
 input: Path struct, has vector of cities for a route and distance of that route
 output: Input argument will contain least distance path and corresponding distance
 **********************************************************************************/
void twoOptTSP(struct Path& tour) {
    bool continueflag = true;
    bool improvementMade;
    clock_t start = clock();
    float timeSeconds = 0;
    //calculate initial distance of route
    tour.distance = distanceTotal(tour.cities);
    do {
        
        improvementMade = false;
        int tourcitiessize = tour.cities.size();

        for (int i = 0; i < tour.cities.size() - 2 && continueflag; ++i) {
            for (int k = i + 1; k < tour.cities.size() - 1 && continueflag; ++k) {
                std::vector<City> newRoute = twoOptSwap(tour.cities, i, k);
                int newDistance = distanceTotal(newRoute);
                if (newDistance < tour.distance) {
                    tour.distance = newDistance;
                    tour.cities = newRoute;
                    improvementMade = true;
                }
                clock_t currentloop = clock();
                long long loopclockcycles = currentloop - start;
                float looptimeSeconds = ((float)loopclockcycles)/CLOCKS_PER_SEC;
                if (looptimeSeconds > 180)
                {
                    continueflag = false;
                }

            }
        }
        clock_t current = clock();
       long long clockCycles = current - start;
        timeSeconds = ((float)clockCycles)/CLOCKS_PER_SEC;
    //loop until no more improvements
    } while (improvementMade == true && timeSeconds < 180 && continueflag);
        
}

std::vector<City> twoOptSwap(std::vector<City> route, int i, int k) {
    std::vector<City> newRoute;
    for (int index = 0; index <= i - 1; ++index) {
        newRoute.push_back(route.at(index));
    }
    for (int index = k; index >= i; --index) {
        newRoute.push_back(route.at(index));
    }
    for (int index = k + 1; index < route.size(); ++index) {
        newRoute.push_back(route.at(index));
    }
    return newRoute;
}

int distanceCities(City city1, City city2) {
    int dist = round(sqrt(pow(city1.xcoord - city2.xcoord, 2) +
                         (pow(city1.ycoord - city2.ycoord, 2))));
    return dist;
}

int distanceTotal(std::vector<City>& route) {
    int dist = 0;
    for (int i = 1; i < route.size(); ++i) {
       dist += distanceCities(route.at(i - 1), route.at(i));
    }
    dist += distanceCities(route.at(route.size() - 1), route.at(0));
    return dist;
}