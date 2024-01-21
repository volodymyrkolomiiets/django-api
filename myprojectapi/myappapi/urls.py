from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

# router = DefaultRouter(trailing_slash=False)
# router.register("books", views.BookView, basename="books")
# urlpatterns = router.urls


# from rest_framework.routers import SimpleRouter
# router = SimpleRouter(trailing_slash=False)
# router.register("books", views.BookView, basename="books")
# urlpatterns = router.urls

urlpatterns = [
    path("books/", views.BookList.as_view()),
    path("books/<int:pk>", views.Book.as_view()),

    # path("books", views.books), 
    # path("orders", views.Orders.list_orders),
    # path("books/<int:pk>", views.BookView.as_view()),
    # path("books", views.BookView.as_view(
    #    {
    #     "get": "list",
    #     "post": "create"
    #    })
    # ),
    # path("books/<int:pk>", views.BookView.as_view(
    #     {
    #         "get": "retrieve",
    #         "put": "update",
    #         "patch": "partial_update",
    #         "delete": "destroy"
    #     }
    # ))
    
]