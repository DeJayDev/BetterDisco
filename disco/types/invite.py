from disco.types.base import SlottedModel, Field, datetime, text, enum
from disco.types.user import User
from disco.types.guild import Guild, GuildScheduledEvent
from disco.types.channel import Channel, StageInstance
from disco.types.oauth import Application


class InviteTargetTypes:
    STREAM = 1
    EMBEDDED_APPLICATION = 2


class Invite(SlottedModel):
    """
    An invite object.

    Attributes
    ----------
    code : str
        The invite code.
    guild : :class:`disco.types.guild.Guild`
        The guild this invite is for.
    channel : :class:`disco.types.channel.Channel`
        The channel this invite is for.
    target_user_id : snowflake
        The user ID this invite targets.
    target_user_type : int
        The type of user target for this invite.
    approximate_presence_count : int
        The approximate count of online members.
    approximate_member_count : int
        The approximate count of total members.
    inviter : :class:`disco.types.user.User`
        The user who created this invite.
    uses : int
        The current number of times the invite was used.
    max_uses : int
        The maximum number of uses.
    max_age : int
        The time after this invite's creation at which it expires.
    temporary : bool
        Whether this invite only grants temporary membership.
    created_at : datetime
        When this invite was created.
    """
    code = Field(text)
    guild = Field(Guild)
    channel = Field(Channel)
    inviter = Field(User)
    target_type = Field(enum(InviteTargetTypes))
    target_user = Field(User)
    target_application = Field(Application)
    approximate_presence_count = Field(int)
    approximate_member_count = Field(int)
    expires_at = Field(datetime)
    stage_instance = Field(StageInstance)
    guild_scheduled_event = Field(GuildScheduledEvent)
    uses = Field(int)
    max_uses = Field(int)
    max_age = Field(int)
    temporary = Field(bool)
    created_at = Field(datetime)

    @classmethod
    def create_for_channel(cls, channel, *args, **kwargs):
        return channel.client.api.channels_invites_create(channel.id, *args, **kwargs)

    @property
    def link(self):
        return 'https://discord.gg/{}'.format(self.code)

    def delete(self, *args, **kwargs):
        self.client.api.invites_delete(self.code, *args, **kwargs)
