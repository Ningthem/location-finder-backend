# Latitude Longitude Finder

This API accepts an excel file with one or more physical addresses and returns another excel file with its corresponding Latitude and Longitudes. Django Rest Framework is used to serve the backend APIs.

## Live Working App
Please visit the [link](https://frontend-theta-six.vercel.app/) to check the actual working of the app. The frontend is built on React and hosted on [Vercel](https://vercel.com/) and the backend is hosted on [PythonAnyWhere](https://www.pythonanywhere.com/)

## Main Libraries or Frameworks Used
Django, Django Rest Framework, Django Knox Authentication, Geocoder, Pandas

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install.

```bash
pip install -r requirements.txt
```

## MapQuest API Key
1. Goto [MapQuest Developer Site](https://developer.mapquest.com/) and get an API Key

2. Update the key inside the app "location/api.py", line 53

```python
 g = geocoder.mapquest(location=locations, method='batch', key='MAPQUEST_SECRETE_KEY')
```

## RUN
Go to the project folder and run as a normal Django app
```bash
python manage.py runserver
```

## API Endpoint
Url for sending excel post data in localhost

```python
   http://localhost:8000/api/location/upload
```

## Excel Data Format
The API accepts only excel file (.xlsx, .xls) with a Header column "Places" indicating addresses of the physical address. Download the excel template from the [link](https://github.com/Ningthem/location-finder-backend/blob/master/Locations.xlsx). Only excel files in this format will be accepted

## POST body data
```json
   {
     "file_uploaded": JSON FormData
   }
```

## License
[MIT](https://choosealicense.com/licenses/mit/)