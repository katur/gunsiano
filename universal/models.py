from django.contrib import auth


def has_personnel_admin_privileges(self):
    """
    Determine whether a user has admin privileges to edit
    personnel information
    (certain non-superusers need this privilege).
    """
    if (self.is_active and (self.is_superuser or self.username=='jessica')):
        return True
    else:
        return False


auth.models.User.add_to_class(
    'has_personnel_admin_privileges', has_personnel_admin_privileges)
