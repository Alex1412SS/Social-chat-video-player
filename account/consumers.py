import json

from asgiref.sync import sync_to_async, async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.exceptions import ObjectDoesNotExist


from .models import chat_messages, Chat, Message, notification
from toons.models import toons_model, Review, Review_review

class reviews(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'review_room'
        self.room_group_name = 'review_group'

        # Join chat room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
    async def disconnect(self, close_code):
        # Leave chat room
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        review = text_data_json.get('review')
        comment = text_data_json.get('comment')
        review_id = text_data_json.get('review_id')

        if review:
            user = self.scope['user']
            toon = text_data_json.get('toon')

            await self.save_message(user, review, toon)

            # Send message to the group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'review': review,
                    'username': user.username,
                    'toon': toon,

                }
            )
        if comment:
            user = self.scope['user']

            await self.save_review_review(user, comment, review_id)

            # Send message to the group
            await self.channel_layer.group_send(
                self.room_group_name,
                    {
                        'type': 'chat_review',
                        'comment': comment,
                        'review_id': review_id,
                        'username': user.username,


                    }
                )

    async def chat_review(self, event):
        comment = event['comment']
        username = event['username']
        review_id = event['review_id']


        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'comment': comment,
            'username': username,
            'review_id': review_id,

        }))

    async def save_review_review(self, user, comment, review_id):
        await sync_to_async(self._save_review_review_sync)(user, comment, review_id)


    def _save_review_review_sync(self, user, comment, review_id):
        review_rev = Review_review(user=user, comment=comment)
        review_rev.save()
        review = Review.objects.get(id=review_id)
        review.otvet.add(review_rev)
        review.save()
        notif = notification.objects.create(not_text=f"Ответ на ваш комментарий от {user.username}!")
        notif.for_user.add(review.user)



    async def chat_message(self, event):
        review = event['review']
        username = event['username']
        toon = event['toon']


        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'review': review,
            'username': username,
            'toon': toon,
        }))

    async def save_message(self, user, review, toon):
        await sync_to_async(self._save_message_sync)(user, review, toon)
    def _save_message_sync(self, user, review, toon):
            reviewss = Review(user=user, comment=review)
            reviewss.save()
            toon = toons_model.objects.get(slug=toon)
            toon.reviews.add(reviewss)
class private_chat(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'chat_room'
        self.room_group_name = 'chat_group'

        # Join chat room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave chat room
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')

        if message:
            user = self.scope['user']
            chat = text_data_json.get('chat')
            await self.save_message(user, message, chat)

            # Send message to the group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': user.username,
                    'chat': chat
                }
            )


    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        chat = event['chat']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'chat': chat
        }))

    async def save_message(self, user, message, chat):
        await sync_to_async(self._save_message_sync)(user, message, chat)
    def _save_message_sync(self, user, message, chat):
            chat_message = Message(author=user, message=message, chat_id=chat)
            chat_message.save()





class ChatMessagesConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'chat_room'
        self.room_group_name = 'chat_group'

        # Join chat room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave chat room
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')

        if message:
            user = self.scope['user']
            await self.save_message(user, message)

            # Send message to the group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': user.username
                }
            )

        if text_data_json.get('message_id'):
            user = self.scope['user']
            message_id = text_data_json.get('message_id')
            if user:
                try:
                    await self.delete_messages(message_id, user)
                except ObjectDoesNotExist:
                    return print(f"Message with id {message_id} does not exist")



    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

    async def delete_message(self, event):
        message_id = event['message_id']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message_id': message_id
        }))

    async def delete_messages(self, message_id, user):
        await sync_to_async(self._delete_messages_sync)(message_id, user)

    def _delete_messages_sync(self, message_id, user):
        chat_message = chat_messages.objects.get(id=message_id, user=user)
        chat_message.delete()
    async def save_message(self, user, message):

        await sync_to_async(self._save_message_sync)(user, message)

    def _save_message_sync(self, user, message):
            chat_message = chat_messages(user=user, message=message)
            chat_message.save()

