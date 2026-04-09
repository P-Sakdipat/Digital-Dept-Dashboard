from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .excel_handler import db

class SalesSummaryView(APIView):
    def get(self, request):
        time_filter = request.GET.get('time_filter', 'all')
        ref_date = request.GET.get('ref_date')
        summary = db.get_summary(time_filter=time_filter, ref_date=ref_date)
        return Response(summary)

class SalesDataView(APIView):
    def get(self, request):
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 50))
        
        # Build filters dictionary from request.GET
        filters = {}
        for key in ['SoldToName1', 'MatGrDes', 'VBELN']:
            if val := request.GET.get(key):
                filters[key] = val
                
        data = db.get_paginated(page=page, page_size=page_size, filters=filters)
        return Response(data)

    def post(self, request):
        success = db.add_row(request.data)
        if success:
            return Response({"message": "Row added successfully"})
        return Response({"error": "Failed to add row"}, status=status.HTTP_400_BAD_REQUEST)

class SalesDetailView(APIView):
    def put(self, request, vbeln, posnr):
        success = db.update_row(vbeln, posnr, request.data)
        if success:
            return Response({"message": "Row updated successfully"})
        return Response({"error": "Record not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, vbeln, posnr):
        success = db.delete_row(vbeln, posnr)
        if success:
            return Response({"message": "Row deleted successfully"})
        return Response({"error": "Record not found"}, status=status.HTTP_404_NOT_FOUND)
