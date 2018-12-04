#include <iostream>
#include "SDL/SDL.h"

#include "pyport.h"
#include "Python.h"

#include <boost/python.hpp>
#include <boost/array.hpp>
#include <boost/tuple/tuple.hpp>


#define LEFT_THUMBSTICK_HORIZONTAL 1
#define LEFT_THUMBSTICK_VERTICAL 2
#define RIGHT_THUMBSTICK_HORIZONTAL 3
#define RIGHT_THUMBSTICK_VERTICAL 4
#define BUTTON_PRESSED 5
#define BUTTON_RELEASED 6

boost::python::tuple items_to_tuple(int event_id, int value){
    boost::python::list python_list;
    python_list.append(event_id);
    python_list.append(value);
    return boost::python::tuple(python_list);
}

bool initialize_sdl(){
    if (SDL_Init( SDL_INIT_VIDEO | SDL_INIT_JOYSTICK ) < 0){
        return false;
    }
    SDL_JoystickEventState(SDL_ENABLE);
    return true;
}

class XBoxControllerManager{
    private:
        SDL_Joystick *xbox_controller;
        bool controller_ready;
        SDL_Event event;
    public:
        XBoxControllerManager();
        ~XBoxControllerManager();
        bool controller_is_ready(){ return controller_ready; }
        bool initialize();
        boost::python::tuple get_next_event();

};
XBoxControllerManager::XBoxControllerManager(){
    controller_ready = false;
}

XBoxControllerManager::~XBoxControllerManager(){
    SDL_JoystickClose(this->xbox_controller);
    SDL_Quit();
}

bool XBoxControllerManager::initialize(){
    bool success = initialize_sdl();
    if (!success){
        return false;
    }
    SDL_JoystickEventState(SDL_ENABLE);
    this->xbox_controller = SDL_JoystickOpen(0);
    if(this->xbox_controller == NULL){
        return false;
    }
    this->controller_ready = true;
    return true;
}

boost::python::tuple XBoxControllerManager::get_next_event(){
    if(!this->controller_ready){
        return items_to_tuple(0, 0);
    }
    bool event_exists = SDL_PollEvent(&this->event);
    if (!event_exists){
        return items_to_tuple(0, 0);
    }
    switch(event.type){
        case SDL_JOYAXISMOTION:  /* Handle Joystick Motion */
            if ( ( event.jaxis.value < -3200 ) || (event.jaxis.value > 3200 ) ){
                int joystick_value = event.jaxis.value;
                if( event.jaxis.axis == 0) {
                    return items_to_tuple(LEFT_THUMBSTICK_HORIZONTAL, joystick_value);
                }
                else if( event.jaxis.axis == 1) {
                    return items_to_tuple(LEFT_THUMBSTICK_VERTICAL, joystick_value);
                }
                else if( event.jaxis.axis == 2){
                    return items_to_tuple(RIGHT_THUMBSTICK_HORIZONTAL, joystick_value);
                }
                else if( event.jaxis.axis == 3){
                    return items_to_tuple(RIGHT_THUMBSTICK_VERTICAL, joystick_value);
                }
            }
            break;
        case SDL_JOYBUTTONUP:
            return items_to_tuple(BUTTON_RELEASED, event.jbutton.button);
            break;
        case SDL_JOYBUTTONDOWN:  /* Handle Joystick Button Presses */
            return items_to_tuple(BUTTON_PRESSED, event.jbutton.button);
            break;
    }
    return items_to_tuple(0, 0);
}


using namespace boost::python;
BOOST_PYTHON_MODULE(boost_xbox_controller) // this parameter needs to match filename
{
    class_<XBoxControllerManager>("XBoxControllerManager")
        .def("initialize", &XBoxControllerManager::initialize)
        .def("controller_is_ready", &XBoxControllerManager::controller_is_ready)
        .def("get_next_event", &XBoxControllerManager::get_next_event);
}
// If you want to run a program from C++ your main() function MUST have the following params
int main(int argc, char *argv[]){
    return 1;
}
