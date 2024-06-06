from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, filters
from rest_framework import permissions
from rm_app.models import (
    MyUser, DetailResepMasakan, MenuUtama, StatusModel, Kategori, Jenis, Profil
)
from api.serializers import (
    DetailResepMasakanSerializers, MenuUtamaSerializers, RegisterMyUserSerializer, LoginSerializer
)
from rest_framework import generics
from rest_framework.authtoken.models import Token
from django.contrib.auth import login as rm_login, logout as rm_logout
from django.http import HttpResponse, JsonResponse 
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from .paginators import CustomPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import ValidationError

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # Tidak memeriksa CSRF token

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # Read Only untuk semua
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        
        # Full access untuk admin dowang
        return request.user.is_authenticated and request.user.is_admin

class DetailResepMasakanListApiView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication, TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request, *args, **kwargs):
        detail_resep = DetailResepMasakan.objects.all()
        serializers = DetailResepMasakanSerializers(detail_resep, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            # Handle list of items
            responses = []
            for item in request.data:
                serializer = DetailResepMasakanSerializers(data=item)
                if serializer.is_valid():
                    serializer.save()
                    responses.append({
                        'status': status.HTTP_201_CREATED,
                        'message': 'Data created successfully...',
                        'data': serializer.data
                    })
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(responses, status=status.HTTP_201_CREATED)
        
        elif isinstance(request.data, dict):
            # Handle single item
            serializer = DetailResepMasakanSerializers(data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {
                    'status': status.HTTP_201_CREATED,
                    'message': 'Data created successfully...',
                    'data': serializer.data
                }
                return Response(response, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            raise ValidationError({"message": "Expected a list or a dictionary."})


class MenuUtamaListApiView(APIView):
    def get(self, request, *args, **kwargs):
       menu_utama = MenuUtama.objects.all()
       serializers = MenuUtamaSerializers(menu_utama, many = True)
       return Response(serializers.data, status = status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        data = {
            'nama' : request.data.get('nama'),
            'informasi' : request.data.get ('informasi'),
        }
        rekomendasi_ids = request.data.getlist('rekomendasi')
        if rekomendasi_ids:
            data['rekomendasi'] = rekomendasi_ids
            
        serializer = MenuUtamaSerializers(data = data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status' : status.HTTP_201_CREATED,
                'message' : 'Data created successfully...',
                'data' : serializer.data
            }
            return Response(response, status = status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)



class DetailResepMasakanApiView(APIView):
    def get_object(self, id):
        try:
            return DetailResepMasakan.objects.get(id = id)
        except DetailResepMasakan.DoesNotExist:
            return None
        
    def get(self, request, id, *args, **kwargs):
        detail_resep_masakan_instance = self.get_object(id)
        if not detail_resep_masakan_instance:
            return Response(
                {
                    'status' : status.HTTP_400_BAD_REQUEST,
                    'message' : 'Data does not exists...',
                    'data' : {}
                }, status= status.HTTP_400_BAD_REQUEST
            )
        
        serializer = DetailResepMasakanSerializers(detail_resep_masakan_instance)
        response = {
            'status' : status.HTTP_200_OK,
            'message' : 'Data retrieve successfully...',
            'data' : serializer.data
        }
        return Response(response, status = status.HTTP_200_OK)
    
    def put(self, request, id, *args, **kwargs):
        detail_resep_masakan_instance = self.get_object(id)
        if not detail_resep_masakan_instance:
            return Response(
                {
                    'status' : status.HTTP_400_BAD_REQUEST,
                    'message' : 'Data does not exists....',
                    'data' : {}
                }, status = status.HTTP_400_BAD_REQUEST
            )
        
        data = {
            'nama' : request.data.get('nama'),
            'deskripsi' : request.data.get ('deskripsi'),
            'bahan' : request.data.get('bahan'),
            'cara_buat' : request.data.get('cara_buat'),
            'kategori' : request.data.get('kategori'),
            'jenis' : request.data.get('jenis'),
        }
        serializer = DetailResepMasakanSerializers(instance = detail_resep_masakan_instance, data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status' : status.HTTP_200_OK,
                'message' : 'Data created successfully...',
                'data' : serializer.data
            }
            return Response(response, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id, *args, **kwargs):
        detail_resep_masakan_instance = self.get_object(id)
        if not detail_resep_masakan_instance:
            return Response(
                {
                    'status' : status.HTTP_400_BAD_REQUEST,
                    'message' : 'Data does not exists....',
                    'data' : {}
                }, status = status.HTTP_400_BAD_REQUEST
            )
        
        detail_resep_masakan_instance.delete()
        response = {
            'status' : status.HTTP_200_OK,
            'message' : 'Data deleted successfully....'
        }
        return Response(response, status= status.HTTP_200_OK)
        
    

class MenuUtamaApiView(APIView):
    def get_object(self, id):
        try:
            return MenuUtama.objects.get(id = id)
        except MenuUtama.DoesNotExist:
            return None
        
    def get(self, request, id, *args, **kwargs):
        menu_utama_instance = self.get_object(id)
        if not menu_utama_instance:
            return Response(
                {
                    'status' : status.HTTP_400_BAD_REQUEST,
                    'message' : 'Data does not exists...',
                    'data' : {}
                }, status= status.HTTP_400_BAD_REQUEST
            )
        
        serializer = MenuUtamaSerializers(menu_utama_instance)
        response = {
            'status' : status.HTTP_200_OK,
            'message' : 'Data retrieve successfully...',
            'data' : serializer.data
        }
        return Response(response, status = status.HTTP_200_OK)
    
    def put(self, request, id, *args, **kwargs):
        menu_utama_instance = self.get_object(id)
        if not menu_utama_instance:
            return Response(
                {
                    'status' : status.HTTP_400_BAD_REQUEST,
                    'message' : 'Data does not exists....',
                    'data' : {}
                }, status = status.HTTP_400_BAD_REQUEST
            )
        
        data = {
            'nama' : request.data.get('nama'),
            'informasi' : request.data.get ('informasi'),
        }
        rekomendasi_ids = request.data.get('rekomendasi')
        if rekomendasi_ids:
            if isinstance(rekomendasi_ids, str):
                rekomendasi_ids = rekomendasi_ids.split(',')
            data['rekomendasi'] = rekomendasi_ids
        
        serializer = MenuUtamaSerializers(instance = menu_utama_instance, data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status' : status.HTTP_200_OK,
                'message' : 'Data created successfully...',
                'data' : serializer.data
            }
            return Response(response, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id, *args, **kwargs):
        menu_utama_instance = self.get_object(id)
        if not menu_utama_instance:
            return Response(
                {
                    'status' : status.HTTP_400_BAD_REQUEST,
                    'message' : 'Data does not exists....',
                    'data' : {}
                }, status = status.HTTP_400_BAD_REQUEST
            )
        
        menu_utama_instance.delete()
        response = {
            'status' : status.HTTP_200_OK,
            'message' : 'Data deleted successfully....'
        }
        return Response(response, status= status.HTTP_200_OK)
    
class RegisterUserAPIView(APIView):
    serializers_class = RegisterMyUserSerializer
    permission_classes = [AllowAny]

    def post(self, request, format = None):
        serializers = self.serializers_class(data = request.data)
        if serializers.is_valid():
            serializers.save()
            response_data = {
                'status' : status.HTTP_201_CREATED,
                'message' : 'Selamat anda telah terdaftar...',
                'data' : serializers.data,
            }
            return Response(response_data, status= status.HTTP_201_CREATED)
        return Response({
            'status' : status.HTTP_400_BAD_REQUEST,
            'data' : serializers.errors
        }, status= status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data = request.data)
        serializer.is_valid(raise_exception= True)
        user = serializer.validated_data['user']
        rm_login(request, user)
        token, created = Token.objects.get_or_create(user = user)
        return JsonResponse({
            'status' : 200,
            'message' : 'Selamat anda berhasil masuk...',
            'data' : {
                'token' : token.key,
                'id' : user.id,
                'first_name' : user.first_name,
                'last_name' : user.last_name,
                'email': user.email,
                'is_active' : user.is_active,
                'is_admin' : user.is_admin,
            }
        })
    
class LogoutAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        rm_logout(request)
        # Return success response
        return Response({"detail": "Logout Successful"}, status=status.HTTP_200_OK)
    
class DetailresepMasakanView(APIView):
    authentication_class = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        detail_resep = DetailResepMasakan.objects.select_related('status').\
            filter(status = StatusModel.objects.first())
        serializer = DetailResepMasakanSerializers(detail_resep, many = True,)
        response = {
            'status' : status.HTTP_200_OK,
            'message' : 'Pembacaan seluruh data berhasil.....',
            'user' : str(request.user),
            'auth' : str(request.auth),
            'data' : serializer.data,
        }
        return Response(response, status= status.HTTP_200_OK)

class MenuUtamaView(APIView):
    authentication_class = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        menu_utama = MenuUtama.objects.select_related('status').\
            filter(status = StatusModel.objects.first())
        serializer = MenuUtamaSerializers(menu_utama, many = True,)
        response = {
            'status' : status.HTTP_200_OK,
            'message' : 'Pembacaan seluruh data berhasil.....',
            'user' : str(request.user),
            'auth' : str(request.auth),
            'data' : serializer.data,
        }
        return Response(response, status= status.HTTP_200_OK)
    
class DetailResepMasakanFilterApi(generics.ListAPIView):
    queryset = DetailResepMasakan.objects.all()
    serializer_class = DetailResepMasakanSerializers
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['kategori__nama', 'jenis__nama',]
    ordering_fields = ['created_on']