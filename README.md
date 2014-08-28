#install virtualenv
pip install virtualenv

#create a virtual environment using python 3.4
virtualenv -p `which python3.4` --no-site-packages env 

#activate the newly created environment
source env/bin/activate

#install backend dependencies
pip install -r requirements.txt