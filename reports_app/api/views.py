from rest_framework.views import APIView
from reports_app.models import ScamPost,SupportPost
from .permissions import PostPermission
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import ScamPostSerializer,SupportPostSerializer
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework import generics
class ScamPostsList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self,request):
        scamposts = ScamPost.objects.all()
        serializer = ScamPostSerializer(scamposts,many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer = ScamPostSerializer(data=request.data)
        if serializer.is_valid():
          serializer.save()
          return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return(serializer.errors)
        
class ScamPostsDetails(APIView):
     def get(self,request,pk):
         try:
          scampost = ScamPost.objects.get(pk=pk)
         except ScamPost.DoesNotExist:
             return Response({"error":"No report found"},status=status.HTTP_404_NOT_FOUND)
         serializer = ScamPostSerializer(scampost)
         return Response(serializer.data)
     def put (self,request,pk):
         scampost = ScamPost.objects.get(pk=pk)
         serializer = ScamPostSerializer(scampost,data= request.data)
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