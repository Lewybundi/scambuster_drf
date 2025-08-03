from django.urls import path
from .views import ScamPostsList,ScamPostsDetails,SupportList,SupportDetail,CreateSupport,DownvoteToggle

urlpatterns = [
    path('list/',ScamPostsList.as_view(),name='reports'),
    path('<int:pk>/',ScamPostsDetails.as_view(),name='report'),
    path('supports/',SupportList.as_view(),name = "supports"),
    path('<int:pk>/supports/',SupportDetail.as_view(),name = "support_detail"),
    path('<int:pk>/support-create/',CreateSupport.as_view(),name = "support_create"),
    path('<int:pk>/downvote/',DownvoteToggle.as_view(),name='downvote')
]
