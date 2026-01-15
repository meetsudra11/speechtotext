# creating the directory structure for the project 
mkdir -p src
mkdir -p research

# creating the files
touch src/__init__.py
touch src/helper.py
touch src/prompt.py 
touch .env # this is to keep secrects like API keys
touch setup.py
touch app.py
touch research/trails.ipynb
touch requirements.txt

echo "Project structure created successfully."