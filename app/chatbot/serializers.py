from rest_framework import serializers
from .models import Thread, Message, Chunk

class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = ['id', 'name']

class MessageSerializer(serializers.ModelSerializer):
    thread_id = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['type', 'content', 'thread_id']

    def get_thread_id(self, obj):
        return obj.thread.id

class ChunkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chunk
        fields = ['id', 'file', 'content']