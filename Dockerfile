# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip3 install -r requirements.txt

# Run app.py when the container launches
EXPOSE 8501
#CMD ["python", "./src/app.py"]
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

# docker build -t virtu-jira .
# docker run -p 8501:8501 virtu-jira