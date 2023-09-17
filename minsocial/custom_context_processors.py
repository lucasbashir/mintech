from .models import Group

def my_groups_and_joined(request):
    if request.user.is_authenticated:
        my_groups = Group.objects.filter(creator=request.user)
        groups_i_joined = request.user.group_members.all()
    else:
        my_groups = []
        groups_i_joined = []

    return {
        'my_groups': my_groups,
        'groups_i_joined': groups_i_joined,
    }