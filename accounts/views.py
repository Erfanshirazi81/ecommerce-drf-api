from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer, UserprofileSerializer
from rest_framework.permissions import IsAuthenticated

class UserRegisterView(APIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        ser_data = UserRegisterSerializer(data = request.data)
        if ser_data.is_valid():
            ser_data.save()
            return Response({"message": "User registered successfully!"})
        return Response(ser_data.errors)
    
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated, ]   
    serializer_class = UserprofileSerializer
    def get(self, request):
        serializer = UserprofileSerializer(request.user)
        return Response(serializer.data)




