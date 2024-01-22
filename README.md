# **Outline**

- [**Project: Taxi Trip Duration in NYC**](#project-taxi-trip-duration-in-nyc)
- [**Project Setup**](#project-setup)
   - [Virtual Environment and Dependencies](#virtual-environment-and-dependencies)
   - [Docker and Local Service](#docker-and-local-service)
   - [Web Service](#web-service)


# **Project: Taxi Trip Duration in NYC**

<center><img src = "reports/figures/taxi-trip-nyc.png" width="970" height="270"/></center>

In this project, we will build a machine learning model to predict the trip duration of taxi rides in New York City. The dataset is from [Kaggle](https://www.kaggle.com/competitions/nyc-taxi-trip-duration). The original dataset have approximately 1.4 million entries for the training set and 630k for the test set, although only the training set is used in this project. The dataset is then preprocessed, outliers are removed, and new features are created, followed by splitting it into train, test, and validation sets.

The goal is to predict the trip duration of taxi trips in New York City. The evaluation metric used for this project is the Root Mean Squared Logarithmic Error (RMSLE). The RMSLE is calculated by taking the log of the predictions and actual values. This metric ensures that errors in predicting short trip durations are less penalized compared to errors in predicting longer ones. For this purpose, we employ three types of machine learning models: mini-batch k-means to create new cluster features for the locations, and the Decision Tree Regressor and XGBoost to predict the trip duration.


Initially, the dataset has just 11 columns, offering great possibilities for creating new features and visualizations. The dataset has the following features:


- **id** - a unique identifier for each trip.

- **vendor_id** - a code indicating the provider associated with the trip record.

- **pickup_datetime** - date and time when the meter was engaged.

- **dropoff_datetime** - date and time when the meter was disengaged.

- **passenger_count** - the number of passengers in the vehicle (driver entered value).

- **pickup_longitude** - the longitude where the meter was engaged.

- **pickup_latitude** - the latitude where the meter was engaged.

- **dropoff_longitude** - the longitude where the meter was disengaged.

- **dropoff_latitude** - the latitude where the meter was disengaged.

- **store_and_fwd_flag** - This flag indicates whether the trip record was held in vehicle memory before sending to the vendor because the vehicle did not have a connection to the server Y=store and forward; N=not a store and forward trip.

- **trip_duration** - duration of the trip in seconds.

The notebooks for the project are located in the folder [`taxi-trip-regression/notebooks/`](https://github.com/marcosbenicio/taxi-trip-regression/tree/main/notebooks). 


# **Project Setup**


## Virtual Environment and Dependencies

To run the Jupyter notebooks in this project or a web service, is required to set up a virtual environment and install the dependencies.

1. Clone the repository to your local machine and navigate to the project directory (root):

```bash
git clone https://github.com/marcosbenicio/taxi-trip-regression
```

2. Ensure that `pipenv` is installed. If it is not installed, use the following command:

```sh
pip install pipenv
```

3. In the root directory of the project, where the `Pipfile` is located, set up the virtual environment and install the dependencies:

```sh
pipenv install
```

4. You can start the Jupyter notebook within the `pipenv` environment using:

```sh
pipenv shell
jupyter notebook
```
    
this will start the Jupyter Notebook in the virtual environment context on your browser.

## Virtual Environment and Local Service

To host the service locally using the virtual environment, run the python script [`src/models/predict_model.py`](https://github.com/marcosbenicio/taxi-trip-regression/blob/main/src/models/predict_model.py)  to start the Flask application:

```sh
python3 src/models/predict_model.py
```

With the Flask application running, we can make HTTP requests to port 9696. For example, in the Jupyter notebook located in [`taxi-trip-duration.ipynb`](https://github.com/marcosbenicio/taxi-trip-regression/blob/main/notebooks/taxi-trip-duration.ipynb), and run the following code in Section 9 to test the local service: 


```python
url_local = "http://127.0.0.1:9696/predict"
# Sample one trip to make prediction
trip = df_test.sample(n=1).to_dict(orient='records')[0]
# Make a POST request to predict trip duration
requests.post(url_local, json = trip).json()
```

## Docker and Local Service

1. Open a terminal or command prompt. Navigate to the directory containing the Dockerfile. Run the following command to build the Docker image named taxi-trip-predict (you can give a different name to the image if you prefer):

```bash
sudo docker build -t taxi-trip-predict .
```

or simple download the image from the Docker Hub ([Docker image](https://hub.docker.com/r/marcosbenicio/taxi-trip-predict/tags)):

```bash
sudo docker pull marcosbenicio/taxi-trip-predict:latest
```

2. To list all the Docker images on your system and verify that the image is there, use:

```bash
sudo docker images
```

3. After the image is built or pushed, run a container from it with the following command:

```bash
sudo docker run -p 9696:9696 marcosbenicio/taxi-trip-predict
```

With the Flask application running inside Docker, we can make HTTP requests to port 9696. For example, in the Jupyter notebook located in [`taxi-trip-duration.ipynb`](https://github.com/marcosbenicio/taxi-trip-regression/blob/main/notebooks/taxi-trip-duration.ipynb),and run the following code in Section 9 to test the local service with docker: 

```python
url_local = "http://127.0.0.1:9696/predict"
# Sample one trip to make prediction
trip = df_test.sample(n=1).to_dict(orient='records')[0]
# Make a POST request to predict trip duration
requests.post(url_local, json = trip).json()
```

## Docker and Web Service

The Docker image for the model has been deployed to the [Render cloud service](https://render.com/) for interaction via HTTP requests. Navigate to the Jupyter notebook [`taxi-trip-duration.ipynb`](https://github.com/marcosbenicio/taxi-trip-regression/blob/main/notebooks/taxi-trip-duration.ipynb) and run the following code in Section 9 to test the cloud service:  

```python
# Render Clound URL
url_clound = "https://taxi-trip-predict.onrender.com/predict"
trip = df_test.sample(n=1).to_dict(orient='records')[0]
requests.post(url_clound, json = trip).json()
```



