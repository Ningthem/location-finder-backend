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

class ConnectionTest(APIView):

    def get(self, request):
        return Response({"message": "Test"}, status=status.HTTP_200_OK)


class GetLatLongAPI(APIView):
    serializer_class = UploadSerializer

    def post(self, request):
        file_suffix = random.randint(100,999)
        file_uploaded = request.FILES.get('file_uploaded')

        file_path = f'{str(settings.MEDIA_ROOT)}/Location_{file_suffix}.xlsx'
        with open(file_path, 'wb+') as destination:
            for chunk in file_uploaded.chunks():
                destination.write(chunk)
        
        df = pd.read_excel(file_path)
        
        if df.columns[0] != 'Places':
            os.remove(file_path)
            return Response({"message": 'The uploaded file should have "Places" as first column'}, status=status.HTTP_400_BAD_REQUEST)
        
        if df.shape[1] != 1:
            os.remove(file_path)
            return Response({"message": 'The uploaded file should have a single column "Places"'}, status=status.HTTP_400_BAD_REQUEST)
        
        print(df.columns[0])
        print(df.shape[1])

        locations = df['Places'].tolist()
        g = geocoder.mapquest(location=locations, method='batch', key='j0paRAfw1XI6k0MpkGG1okNyVPQoqjfR')
        latitudes = []
        longitudes = []

        for result in g:
            latitudes.append(result.lat)
            longitudes.append(result.lng)

        df['Latitude'] = latitudes
        df['Longitude'] = longitudes
        
        output_filename = f'output_{file_suffix}.xlsx'
        output_file_path = f'{str(settings.MEDIA_ROOT)}/output'
        df.to_excel(f'{output_file_path}/{output_filename}', index=False, header=True)
        os.remove(file_path)
        
        return Response({"message": "Uploaded", "output_path": f'{settings.HOST_NAME}/media/output/{output_filename}'}, status=status.HTTP_200_OK)

    