from rest_framework import serializers
from rm_app.models import (
    MyUser, DetailResepMasakan, MenuUtama, StatusModel, Kategori, Jenis, Profil
)
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

class DetailResepMasakanSerializers(serializers.ModelSerializer):
    class Meta:
        model = DetailResepMasakan
        fields = ('id', 'nama', 'deskripsi', 'bahan', 'cara_buat', 'gambar', 'kategori', 'jenis')

class MenuUtamaSerializers(serializers.ModelSerializer):
    class Meta:
        model = MenuUtama
        fields = ('id', 'nama', 'informasi', 'rekomendasi')

class RegisterMyUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required = True,
        validators = [UniqueValidator(queryset= MyUser.objects.all())])
    password1 = serializers.CharField(write_only = True,
        required = True, validators = [validate_password])
    password2 = serializers.CharField(write_only = True,
        required = True)
    
    class Meta:
        model = MyUser
        fields = ['username', 'email', 'password1', 'password2', 'is_active', 'is_admin', 'is_user', 'first_name', 'last_name']
        extra_kwargs = {
            'first_name' : {'required' : True},
            'last_name' : {'required' : True}
        }

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError({
                'password' : 'Kata Sandi dan Ulang kata sandi tidak sama....'
            })
        return attrs
    
    def create(self, validated_data):
        user = MyUser.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
            is_active = validated_data['is_active'],
            is_admin = validated_data['is_admin'],
            is_user = validated_data['is_user'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name']
        )

        user.set_password(validated_data['password1'])
        user.save()
        return user 
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username', '')
        password = data.get('password', '')

        if username and password:
            user = authenticate(username = username, password = password)
            if user:
                if user.is_active:
                    data['user'] = user
                #update : User baca dowang (done)
                else:
                    msg = 'Status pengguna tidak aktif...'
                    raise ValidationError({'message' : msg})
            else:
                msg = 'Anda tidak memiliki akses masuk...'
                raise ValidationError({'massage' : msg})
            
        else: 
            msg = 'Mohon mengisi kolom nama pengguna dan kata sandi.....'
            raise ValidationError({'message' : msg})
        return data
    
