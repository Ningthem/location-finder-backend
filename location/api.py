from rest_framework.views import APIView
from rest_framework import status
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from django.conf import settings
from rest_framework.viewsets import ViewSet
from .serializers import UploadSerializer

import os
import random
import geocoder
import pandas as pd


class GetLatLongAPI(APIView):
    """ API to take excel file from post data and geocode through MapQuest to get
        Latitude and Longitude.
    """

    serializer_class = UploadSerializer

    def post(self, request):
        file_suffix = random.randint(100,999)
        file_uploaded = request.FILES.get('file_uploaded')

        file_extension = file_uploaded.name.split(".")[-1]

        # Checking if the file is an excel file
        if file_extension not in ['xlsx', 'xls']:
            return Response({"message": 'Please upload excel files only'}, status=status.HTTP_400_BAD_REQUEST)

        # Saving excel file to media folder
        file_path = f'{str(settings.MEDIA_ROOT)}/Location_{file_suffix}.xlsx'
        with open(file_path, 'wb+') as destination:
            for chunk in file_uploaded.chunks():
                destination.write(chunk)
        
        # Using Pandas to open and manipulate excel data
        df = pd.read_excel(file_path)
        
        # File integrity checks
        if df.columns[0] != 'Places':
            os.remove(file_path)
            return Response({"message": 'The uploaded file should have "Places" as first column'}, status=status.HTTP_400_BAD_REQUEST)
        
        if df.shape[1] != 1:
            os.remove(file_path)
            return Response({"message": 'The uploaded file should have a single column "Places"'}, status=status.HTTP_400_BAD_REQUEST)
        
        locations = df['Places'].tolist()

        # Getting geocoded data from MapQuest API
        g = geocoder.mapquest(location=locations, method='batch', key='MAPQUEST_SECRETE_KEY')
        latitudes = []
        longitudes = []

        for result in g:
            latitudes.append(result.lat)
            longitudes.append(result.lng)

        # Setting new columns for latitudes and longitudes in pandas dataframe
        df['Latitude'] = latitudes
        df['Longitude'] = longitudes
        
        output_filename = f'output_{file_suffix}.xlsx'
        output_file_path = f'{str(settings.MEDIA_ROOT)}/output'
        # saving new excel file in media/output folder
        df.to_excel(f'{output_file_path}/{output_filename}', index=False, header=True)
        os.remove(file_path)
        
        return Response({"message": "Uploaded", "output_path": f'{settings.HOST_NAME}/media/output/{output_filename}'}, status=status.HTTP_200_OK)

    