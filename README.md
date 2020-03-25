# wat_bal
A repository for a conceptual hydrological model. (Exercise 2 Watershed Modelling, ETH Zurich)

## Instructions set up Environemnt
1. Download the zip file wat_bal_python.zip and extract it.

2. Install python 3.7.6 (Required)[(Its Free!)](https://www.python.org/downloads/release/python-367/)
    - To check that python is installed on your desktop:
        - For Mac open terminal and type pyrhon3 (Mac comes with preinstalled python 2.7.6 but you still need to install python 3.7.6)
        - For Windows 10, open Windows Power Shell and then type Python

3. Install Visual Studio Code (Recommended)[Its Free](https://code.visualstudio.com)
    - Visual Studio Code is an editor and will comes with autocomplete and syntax highlighting features
    - Any other editor should work as well but from here on the setup will be in Visual Studio Code
    - Download the version depending on your OS.

4. Setting up the project. Installing packages.
    - Open Terminal/Windows Power Shell
    - Install pipenv by running "pip3 install pipenv" (without quotes) in Terminal/Windows Power Shell
    - Open Visual Studio Code
    - A welcome screen will appear, in the left side bar select the Extension (icon with 4 squares)
    - Search Python. Select Python (Linting, Debugging,..)
    - Once it is installed open Explorer on the top left bar. (shift+ctrl+e)
    - Select Open Folder, Browse to the directory water_bal_python. 
    - The folder should contain Pipfile and Pipfile.lock
    - Go to Terminal at the top and select new terminal
    - Terminal will open at the bottom, Run the command "pipenv install"
    - This step may take some time and the internet connection is required 
    - Restart the VSCode. Now on the lef side of blue colored bottom bar you can see the python version adn in bracket name of the folder along with pipenv. ('wat_bal_python:pipenv')
  
## Instruction to run the scripts

- There are 5 scripts namely model.py, plots.py, utils.py run_opt.py, run_param_plot.py, run_sim.py and two folders name data and plots.
- All the required data is in the data folder.
- All the plots will be created in the plots folder
- Two more files will be added namely parameter.h5 and gof.csv
- Parameter.h5 will have the list of parameters for different runs
- gof.csv will contain the goodness of fit values for observation and simulation
- Run the scripts in order
    - (run_opt.py) run_opt will optimize the model and save the value of parameters in Parameters.h5
        - Number of runs (nruns) needs to be selected here. Roughly it takes 70-120 runs per iteration depending on the computer. 
    - (run_param_plot.py) run_param_plot will generate the plots of the parameters
    - Seeing the histogram of parameters chose the value of the parameter and add the values to the script run_sim.py
    - (run_sim.py) Run the script run_sim.py to save the plots and gof values
    - Any change in the structure of the model needs to be made in model.py
    - For adding parameters to calibrate some changes also needs to be made in run_opt.py and run_sim.py

