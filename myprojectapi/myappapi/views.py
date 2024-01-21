from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
# Create your views here.

@api_view(["POST", "GET"])
def books(request):
    # return HttpResponse("list of the books", status=status.HTTP_200_OK)
    return Response("list of the books", status=status.HTTP_200_OK)


class Orders:
    @staticmethod
    @api_view()
    def list_orders(request):
        return Response({"message": "list of orders"}, 200)
    

# class BookView(APIView):
#     def get(self, request, pk):
#         return Response(
#             {"message": "single book with id " + str(pk)},
#             status=status.HTTP_200_OK
#         )
        
#     def put(self, request, pk):
#         return Response(
#             {"title": request.data.get("title")},
#             status=status.HTTP_200_OK
#         )
        
class BookView(ViewSet):
    def list(self, request):
        return Response({"message":"All books"}, status.HTTP_200_OK)
    
    def create(self, request):
        return Response({"message": "Creating a book"}, status.HTTP_201_CREATED)
    
    def update(self, request, pk=None):
        return Response({"message": "Updating a book"}, status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        return Response({"message": "Display a book"}, status.HTTP_200_OK)
    
    def partial_update(self, request, pk=None):
        return Response({"message": "Partial updating a book"}, status.HTTP_200_OK)
    
    def destroy(self, request, pk=None):
        return Response({"message": "Deleting a book"}, status.HTTP_200_OK)
    
    
class BookList(APIView):
    def get(self, request):
        author = request.GET.get("author")
        if author:
            return Response({"message":"list of the books by " + author }, status.HTTP_200_OK)
        return Response({"message": "list of the books"}, status.HTTP_200_OK)
    
    def post(self, request):
        return Response({"title": request.data.get("title")}, status.HTTP_201_CREATED)
    

class Book(APIView):
    def get(self, request, pk):
        return Response({"message": "single book with id " + str(pk)}, status.HTTP_200_OK)
    
    def put(self, request, pk):
        return Response({"title": request.data.get("title")}, status.HTTP_200_OK)

