"""
Django REST Framework Views for Reports Application

This module contains API views for managing scam reports, support posts, and downvote functionality.
The application appears to be a community-driven platform where users can report scams and 
support each other's reports.

Models involved:
- ScamPost: Main reports about scams
- SupportPost: User support/endorsement for scam reports
- Downvote: User downvotes for scam posts

Key Features:
- CRUD operations for scam posts and support posts
- Pagination for scam post listings
- Downvote toggle functionality
- Permission-based access control
"""



from rest_framework.views import APIView
from reports_app.models import ScamPost,SupportPost,Downvote
from .permissions import PostPermission
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
from .serializers import ScamPostSerializer,SupportPostSerializer,SupportDetailSerializer
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework import generics
from .pagination import ScamPostListPagination
class ScamPostsList(APIView):
    """
    API View for listing and creating scam posts.
    
    GET: Returns paginated list of all scam posts (accessible to authenticated and anonymous users)
    POST: Creates a new scam post (requires authentication)
    
    Permissions: IsAuthenticatedOrReadOnly - allows read access to all users, 
    write access only to authenticated users
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self,request):
        scamposts = ScamPost.objects.all().order_by('-created_at')
        paginator = ScamPostListPagination()
        paginated_scamposts = paginator.paginate_queryset(scamposts,request,view=self)
        
        serializer = ScamPostSerializer(paginated_scamposts,many=True)
        return paginator.get_paginated_response(serializer.data)
    def post(self,request):
        serializer = ScamPostSerializer(data=request.data)
        if serializer.is_valid():
          serializer.save()
          return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return(serializer.errors)
        
class ScamPostsDetails(APIView):
     """
    API View for retrieving, updating, and deleting individual scam posts.
    
    GET: Retrieve a specific scam post by ID
    PUT: Update a specific scam post by ID
    DELETE: Delete a specific scam post by ID
     """
     def get(self,request,pk):
         try:
          scampost = ScamPost.objects.get(pk=pk)
         except ScamPost.DoesNotExist:
             return Response({"error":"No report found"},status=status.HTTP_404_NOT_FOUND)
         serializer = SupportDetailSerializer(scampost)
         return Response(serializer.data)
     def put (self,request,pk):
         scampost = ScamPost.objects.get(pk=pk)
         serializer = SupportDetailSerializer(scampost,data= request.data)
         if serializer.is_valid():
             serializer.save()
             return Response(serializer.data)
         else:
             return Response(serializer.errors)
     def delete(self,request,pk):
         scampost = ScamPost.objects.get(pk=pk)
         scampost.delete()
         return Response(status=status.HTTP_204_NO_CONTENT)
     
     
class SupportList(generics.ListCreateAPIView):
    queryset = SupportPost.objects.all()
    serializer_class = SupportPostSerializer
class SupportDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SupportPost.objects.all()
    permission_classes =[PostPermission]
    serializer_class = SupportPostSerializer
class CreateSupport(generics.CreateAPIView):
     queryset = SupportPost.objects.all()
     serializer_class = SupportPostSerializer
     def get_queryset(self):
        return SupportPost.objects.all()
     def perform_create(self, serializer):
         pk = self.kwargs.get('pk')
         scampost = ScamPost.objects.get(pk=pk)
         supporter = self.request.user 
         support_querryset = SupportPost.objects.filter(scampost=scampost,supporter=supporter)
         if support_querryset.exists():
             raise ValidationError("You have already created support for this report!")
         else:
             scampost.save()
             serializer.save(scampost=scampost,supporter=supporter)
class DownvoteToggle(APIView):
   """
    Toggle downvote for a ScamPost. If user has already downvoted, remove the downvote.
    If user hasn't downvoted, create a new downvote.
    """
   permission_classes = [IsAuthenticated]
   def post(self,request,pk):
       try:
           scampost = ScamPost.objects.get(pk=pk)
       except ScamPost.DoesNotExist:
           return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
       user = request.user
       try:
           downvote = Downvote.objects.get(user=user,post=scampost)
           downvote.delete()
           return Response({
            "message": "Downvote removed",
            "is_downvoted": False,
            "downvote_count": scampost.downvotes.count()
           })
       except Downvote.DoesNotExist:
           # If downvote doesn't exist, create it
            downvote = Downvote.objects.create(user=user, post=scampost)
            return Response({
                "message": "Post downvoted",
                "is_downvoted": True,
                "downvote_count": scampost.downvotes.count()
            }, status=status.HTTP_201_CREATED)
