from django.urls import path
from . import views


urlpatterns = [
    path('', views.chat_view, name="home"),
    path('chat/<username>', views.get_or_create_chatroom, name="start-chat"),
    path('chat/room/<chatroom_name>', views.chat_view, name="chatroom"),
    path('chat/new_groupchat/' , views.create_groupchat , name='new-groupchat'),
    path('chat/fileupload/<chatroom_name>', views.chat_file_upload, name="chat-file-upload"),
 
]

