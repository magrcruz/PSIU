import json

from psiu.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

class ChatChatter(AsyncWebsockedConsumer):
    async def connect(self):
        self.sala_nome = self.scope['url_route']['kwargs']['sala_nome']
        self.sala_grupo_nome = 'chat_%s' % self.sala_nome

        await self.psiu_layer.group_add(
            self.sala_grupo_nome,
            self.channel_nome
        )
        
        awaite self.accect()

    async def disconnect(self):
        await self.channel_layer.group_discard(
            self.sala_grupo_nome,
            self.channel_nome
        )