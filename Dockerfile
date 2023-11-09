# specify the base image
FROM python:3.9

# set the working directory
WORKDIR /app
# copy the requirements file
COPY requirements.txt /app/
# install dependencies
RUN pip install -r requirements.txt
# copy the rest of the project files
COPY . /app/
# expose the port that the Django application will run on
EXPOSE 8000
# run the Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]