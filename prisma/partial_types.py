from prisma.models import User

User.create_partial('UserRequest', exclude=['id'], exclude_relational_fields=True)
User.create_partial('UserResponse', exclude_relational_fields=True)

User.create_partial('UserAuthentication', exclude=['id', 'name', 'department', 'picture', 'passphrase'])