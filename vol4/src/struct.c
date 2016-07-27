#include <stdio.h>

typedef struct Car{
    double x;
    double y;
} Car;

void show(Car* car){
    printf("Car: %lf,%lf\n", car->x, car->y);
}

int main(int argc, char** argv){
    Car car1, car2;
    car1.x = 1.0;
    car1.y = 1.0;
    car2.x = 5.0;
    car2.y = 5.0;
    return 0;
}
