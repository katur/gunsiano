from moderation import moderation

from website.models import JoinLabSection, ResearchArea, Resource, UserProfile


moderation.register(JoinLabSection)
moderation.register(ResearchArea)
moderation.register(Resource)
moderation.register(UserProfile)
