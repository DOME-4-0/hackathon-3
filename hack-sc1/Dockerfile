# Use the official Jupyter Docker image
FROM jupyter/scipy-notebook

# Set the working directory
WORKDIR /home/jovyan/work

# Copy the requirements.txt file into the Docker image
COPY requirements.txt .

# Install the packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Generate a Jupyter Notebook configuration file
RUN jupyter notebook --generate-config

# Set the Jupyter Notebook password
RUN echo "c.ServerApp.password = u'sha1:0c4df96dddc2:3ea0872a48818d70937903b7bb9f3976ea38d0df'" >> /home/jovyan/.jupyter/jupyter_server_config.py
# Expose the port Jupyter Notebook runs on
EXPOSE 8888