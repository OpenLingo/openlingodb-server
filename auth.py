from devfu.flask.auth import DevFUAuth, RoleBasedAuth


class OpenlingoAuth(RoleBasedAuth):
    def __init__(self, app, user_service):
        roles = ["VIEWER", "EDITOR", "AUTHOR", "ADMIN"]

        role_descriptions = {
            "VIEWER": "Can view/lists assets",
            "EDITOR": "Can edit assets",
            "AUTHOR": "Can create assets",
            "ADMIN": "Manage system and users"
        }

        permissions = {
            "VIEWER": {'*': {'list', 'access'}},
            "EDITOR": {'*': {'modify'}},
            "AUTHOR": {'*': {'create', 'delete'}},
            "ADMIN": {}  # Admin accesses everything
        }

        admin_assets = ['user']  # Protect the user table from interrogation by non-admins

        # These are just defaults, but shown for completeness
        inherit_roles = True
        role_field = 'role'

        RoleBasedAuth.__init__(self, app, user_service, permissions=permissions, roles=roles, admin_assets=admin_assets,
                               inherit_roles=inherit_roles, role_field=role_field, role_descriptions=role_descriptions)