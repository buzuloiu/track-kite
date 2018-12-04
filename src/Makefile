PYTHON_INCLUDE = /usr/local/Cellar/python@2/2.7.15_1/Frameworks/Python.framework/Versions/2.7/include/python2.7
BOOST_INCLUDE = /usr/local/Cellar/boost-python/1.68.0/include
SDL_INCLUDE = /usr/local/include

BASE_LIB_DIR = /usr/local/lib
PYTHON_LIB_DIR = /usr/local/Cellar/python@2/2.7.15_1/Frameworks/Python.framework/Versions/2.7/lib
FORTRAN_LIB_DIR = /usr/local/Cellar/gcc/8.2.0/lib

PYTHON_LIB = python2.7
BOOST_LIB = boost_python27
SDL_LIB = SDL

# got the below line from running sdl-config --cflags --libs
FLAGS_FROM_SDL = -L/usr/local/lib -lSDLmain -lSDL -Wl,-framework,Cocoa -I/usr/local/include/SDL -D_GNU_SOURCE=1 -D_THREAD_SAFE

TARGET = boost_xbox_controller

COMBINED_FLAGS = -L$(FORTRAN_LIB_DIR) -L$(BASE_LIB_DIR) -L$(PYTHON_LIB_DIR) -l$(BOOST_LIB) -l$(PYTHON_LIB) -l$(SDL_LIB) -I$(PYTHON_INCLUDE) -I$(BOOST_INCLUDE) -I$(SDL_INCLUDE) $(FLAGS_FROM_SDL)

# .so file is the file that python will import as a module
$(TARGET).so: $(TARGET).o
	g++ -shared -Wl, $(TARGET).o $(COMBINED_FLAGS) -o $(TARGET).so

$(TARGET).o: $(TARGET).cpp
	g++ $(COMBINED_FLAGS) -fPIC -c $(TARGET).cpp
