from typing import Union


class EditMessage:
    async def edit_message(
            self,
            object_guid: str,
            message_id: Union[int, str],
            text: str,
    ):
        return await self.builder('editMessage',
                                  input={
                                      'object_guid': object_guid,
                                      'message_id': str(message_id),
                                      'text': text.strip(),
                                  })