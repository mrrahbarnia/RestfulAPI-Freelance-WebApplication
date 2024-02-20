from users.models import (
    BaseUser,
    Profile
)

def get_profile(*, user:BaseUser) -> Profile:
    return Profile.objects.get(user=user)

def profile_detail(*, uuid:str) ->Profile:
    profile = Profile.objects.get(uuid=uuid)
    profile.views += 1
    profile.save()
    # TODO: Caching views for profile views
    return profile
