import sys
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.files.uploadedfile import InMemoryUploadedFile
from datetime import datetime, timedelta
from PIL import Image
from io import BytesIO
from django.utils import timezone


class MyUser(AbstractUser):
    is_user = models.BooleanField(default= False)
    is_admin = models.BooleanField(default= False)
    def __str__(self):
        return str(self.username)

class StatusModel(models.Model):
    pilihan_status = (
        ('Aktif', 'Aktif'),
        ('Tidak Aktif', 'Tidak Aktif')
    )
    
    nama = models.CharField(max_length=20, null=False, blank= False)
    deskripsi = models.TextField(blank=True, null=True)
    status = models.CharField(max_length= 15, choices= pilihan_status, default= 'Aktif')
    user_create = models.ForeignKey(MyUser, related_name='user_create_status_model', blank= True, null= True, on_delete=models.SET_NULL)
    user_update = models.ForeignKey(MyUser, related_name='user_update_status_model', blank= True, null= True, on_delete=models.SET_NULL)
    data_created = models.DateTimeField(auto_now_add= True)
    data_last_update = models.DateTimeField(auto_now= True)
    
    def __str__(self):
        return self.nama
     
class Kategori(models.Model):
    nama = models.CharField(max_length= 170)
    status = models.ForeignKey(StatusModel, related_name='status_category', default= StatusModel.objects.first().pk, on_delete=models.PROTECT)
    user_create = models.ForeignKey(MyUser, related_name='user_create_category', blank= True, null= True, on_delete=models.SET_NULL)
    user_update = models.ForeignKey(MyUser, related_name='user_update_category', blank= True, null= True, on_delete=models.SET_NULL)
    data_created = models.DateTimeField(auto_now_add= True)
    data_last_update = models.DateTimeField(auto_now= True)
    
    def __str__(self):
        return self.nama
    
class Jenis(models.Model):
    nama = models.CharField(max_length= 130)
    status = models.ForeignKey(StatusModel, related_name='status_jenis', default= StatusModel.objects.first().pk, on_delete=models.PROTECT)
    user_create = models.ForeignKey(MyUser, related_name='user_create_jenis', blank= True, null= True, on_delete=models.SET_NULL)
    user_update = models.ForeignKey(MyUser, related_name='user_update_jenis', blank= True, null= True, on_delete=models.SET_NULL)
    data_created = models.DateTimeField(auto_now_add= True)
    data_last_update = models.DateTimeField(auto_now= True)
    
    def __str__(self):
        return self.nama
    
    
def compress_image(image, filename):
    curr_datetime = datetime.now().strftime('%y%m%d %H%M%S')
    im = Image.open(image)
    if im.mode != 'RGB':
        im = im.convert('RGB')
    im_io = BytesIO()
    im.save(im_io, 'jpeg', quality = 50, optimize = True)
    im.seek(0)
    new_image = InMemoryUploadedFile(im_io,'ImageField', '%' + '-' +str(filename) + str(curr_datetime) + '.jpg', 'image/jpeg', sys.getsizeof(im_io), None)
    return new_image

class DetailResepMasakan(models.Model):
    nama = models.CharField(max_length= 200, null= False, blank= False)
    deskripsi = models.TextField(null= True, blank=True)
    bahan = models.TextField(null=False, blank=False)
    cara_buat = models.TextField(null=False, blank= True)
    gambar = models.ImageField(default= None, upload_to= 'gambar/resep_masakan', blank= True, null= True)
    kategori = models.ForeignKey(Kategori, related_name='kategori_detail_resep_masakan', on_delete=models.PROTECT)
    jenis = models.ForeignKey(Jenis, related_name='jenis_detail_resep_masakan', on_delete=models.PROTECT)
    status = models.ForeignKey(StatusModel, related_name='status_detail_resep', default=StatusModel.objects.first().pk, on_delete=models.PROTECT)
    user_create = models.ForeignKey(MyUser, related_name='user_create_detail_resep', blank= True, null= True, on_delete=models.SET_NULL)
    user_update = models.ForeignKey(MyUser, related_name='user_update_detail_resep', blank= True, null= True, on_delete=models.SET_NULL)
    
    def save(self, force_insert= True, force_update= True, using= None , update_fields= None , *args, **kwargs):
        if self.id:
            try :
                this = DetailResepMasakan.objects.get(id =self.id)
                if this.gambar != self.gambar:
                    var_gambar = self.gambar
                    self.gambar = compress_image(var_gambar, 'menu')
                    this.gambar.delete()
        
            except: pass
            super(DetailResepMasakan, self).save(*args, **kwargs)
        
        else :
            if self.gambar :
                var_gambar = self.gambar
                self.gambar = compress_image (var_gambar, 'menu')
            super(DetailResepMasakan, self).save(*args, **kwargs)
            
    def __str__(self):
        return str(self.nama) + ' | ' + str(self.kategori) + ' | ' + str(self.jenis)
    
class Profil(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.PROTECT, related_name='user_profile')
    gambar = models.ImageField(default=None, upload_to='gambar/profile')
    bio = models.TextField()
    status = models.ForeignKey(StatusModel, related_name='status_profile', default= StatusModel.objects.first().pk, on_delete=models.PROTECT)
    user_create = models.ForeignKey(MyUser, related_name='user_create_profile', blank= True, null= True, on_delete=models.SET_NULL)
    user_update = models.ForeignKey(MyUser, related_name='user_update_profile', blank= True, null= True, on_delete=models.SET_NULL)
    data_created = models.DateTimeField(auto_now_add= True)
    data_last_update = models.DateTimeField(auto_now= True)
    
    def save(self, force_insert= False, force_update= False, using= None , update_fields= None , *args, **kwargs):
        if self.id:
            try :
                this = Profil.objects.get(id =self.id)
                if this.gambar != self.gambar:
                    var_gambar = self.gambar
                    self.gambar = compress_image(var_gambar, 'profile')
                    this.gambar.delete()
        
            except: pass
            super(Profil, self).save(*args, **kwargs)
        
        else :
            if self.gambar :
                var_gambar = self.gambar
                self.gambar = compress_image (var_gambar, 'profile')
            super(Profil, self).save(*args, **kwargs)
    
    def __str__(self):
        return str(self.user)
    

class MenuUtama(models.Model):
    nama = models.CharField(max_length=100, null=False, blank=False)
    informasi = models.TextField(blank=True, null=True)
    rekomendasi = models.ManyToManyField(DetailResepMasakan, related_name='menu_utama')
    user_create = models.ForeignKey(MyUser, related_name='user_create_menu_utama', blank=True, null=True, on_delete=models.SET_NULL)
    user_update = models.ForeignKey(MyUser, related_name='user_update_menu_utama', blank=True, null=True, on_delete=models.SET_NULL)
    data_created = models.DateTimeField(auto_now_add=True)
    data_last_update = models.DateTimeField(auto_now=True)
    #statusTambahin
    def __str__(self):
        return self.nama