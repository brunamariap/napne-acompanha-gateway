from prisma.models import User



User.create_partial('UserRequest', exclude=['id'], exclude_relational_fields=True)
User.create_partial('UserAuthRequest', exclude=['id', 'name', 'department', 'picture'])

