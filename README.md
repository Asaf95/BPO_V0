# Docker Template for Plotly Dash App 
#### Why to use this project?   
This project provide simple example for dockerizing your Plotly Dash App.    
This project supports Multi-Page Apps and URL started in Dash version 2.5.0          
Prior knowledge is needed! you can simply change.       
This project service as a template for creating a Docker Image from Dash Plotly App      

#### Project Structure
  
├── project           
│   ├── app           
│   │   ├── __init__.py           
│   │   ├── app.py            
│   │   └── Other files / directory / scripts your app needs          
│   │        
│   ├── Dockerfile           
│   └── requirements.txt           
│           
└── README.md           
All files under the 'project' directory will be copied to the docker image.
All the files that are needed for the app (such as modules scripts or directory)
should be added under [app directory](project/app).    
The imports in the program should refer to app directory as the top path of the project.     
# Dockerize the App
The app will be packed as 'Docker Image' the steps to dockerize the app is as followed steps:
1. Create 'requirements.txt' file with all your Python packages that needed to run the app.
you can get the list of packages using the command ```pip list```
2. Add a Dockerfile
```
# set working directory in container
WORKDIR /usr/src/app

# Copy and install packages   
COPY requirements.txt /
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

# Copy app folder to app folder in container
COPY /app /usr/src/app/

# Changing to non-root user
RUN useradd -m appUser
USER appUser

# Run locally on port 8050
CMD gunicorn --bind 0.0.0.0:8050 app:server
```
3. Build the Docker Image 
```
systemctl start docker
sudo docker build -t docker-dash project/.
```

3. Run the App:
```
sudo docker run -p 8050:8050 docker-dash
```

4. Save the docker image as a local file
```
docker save my-image:latest > my-image.tar
```


### Helpfully links and referents
icon's   
https://www.dash-mantine-components.com/
https://icon-sets.iconify.design/bi/box/

Nav    
https://dash-bootstrap-components.opensource.faculty.ai/docs/components/nav/

Docker Dash Plotly
https://towardsdatascience.com/deploy-containerized-plotly-dash-app-to-heroku-with-ci-cd-f82ca833375c
