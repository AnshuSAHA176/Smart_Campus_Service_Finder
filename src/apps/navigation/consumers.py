from channels.consumer import AsyncConsumer


class LiveLocationConsumer(AsyncConsumer):
    async def connect(self):
        self.user = self.scope['user']

        self.group_name = f"user_{self.user.id}"
        self.channel_layer.group_add(self.group_name,self.channel_name)

        

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data = None, bytes_data = None):
        await self.send(f'hello {text_data}')

    # Receive message from room group
    