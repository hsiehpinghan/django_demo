from django.contrib import admin
from .models import Thread, Message, File, Chunk

# Register your models here.
admin.site.register(Thread)
admin.site.register(Message)
admin.site.register(File)
admin.site.register(Chunk)
