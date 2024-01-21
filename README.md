# django-api

## When a ViewSet is used to deal with a collection of resources

| Class method    | Supported HTTP method  |  Purpose                       |
|-----------------|------------------------|--------------------------------|
| **list()**      |  **GET**               |Display resource collection     |
| **create()**    |  **POST**              |Create new resource             |
| **retrieve()**  |  **GET**               |Display a single resource       |
| **update()**    |  **PUT**               |Completely replace a single resource with new data|
| **partial_update** | **PATCH**           |Partially update a single resource |
| **destroy**        |  **DELETE**         | Delete a single resource |


## Generic views
```from rest_framework import generics```
All generic view classes require a queryset and a serializer to work properly. 

|Generic view class | Supported method | Purpose |
|-------------------|------------------|---------|
|CreateAPIView | POST | Create a new resource |
| ListAPIView | GET | Display resource collection |
| RetrieveAPIView | GET | Display a single resource |
| DestroyAPIView | DELETE | Delete a single resource |
| UpdateAPIView | PUT and PATCH | Replace or partially update a single resource |
| ListCreateAPIView |GET, POST | Display resource collection and create a new resource |
| RetrieveUpdateAPIView | GET, PUT, PATCH | Display a single resource and replace or partially update it |
| RetrieveDestroyAPIView | GET, DELETE | Display a single resource and delete it |
| RetrieveUpdateDestroyAPIView | GET, PUT, PATCH, DELETE | Display, replace or update and delete a single resource |

## Return items for the authenticated user only 

```
class OrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Order.objects.all().filter(user=self.request.user)
```

