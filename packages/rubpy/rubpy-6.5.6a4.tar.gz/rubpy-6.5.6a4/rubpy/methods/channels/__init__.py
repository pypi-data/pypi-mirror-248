from .add_channel import AddChannel # channel
from .add_channel_members import AddChannelMembers
from .ban_channel_member import BanChannelMember
from .create_channel_voice_chat import CreateChannelVoiceChat
from .edit_channel_info import EditChannelInfo
from .get_channel_admin_access_list import GetChannelAdminAccessList
from .get_channel_admin_members import GetChannelAdminMembers
from .get_channel_all_members import GetChannelAllMembers
from .get_channel_info import GetChannelInfo
from .get_channel_link import GetChannelLink
from .remove_channel import RemoveChannel
from .set_channel_link import SetChannelLink
from .set_channel_voice_chat_setting import SetChannelVoiceChatSetting


class Channels(
    AddChannel,
    AddChannelMembers,
    BanChannelMember,
    CreateChannelVoiceChat,
    EditChannelInfo,
    GetChannelAdminAccessList,
    GetChannelAdminMembers,
    GetChannelAllMembers,
    GetChannelInfo,
    GetChannelLink,
    RemoveChannel,
    SetChannelLink,
    SetChannelVoiceChatSetting,
):
    pass