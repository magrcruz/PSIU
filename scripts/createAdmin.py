from django.core.exceptions import ObjectDoesNotExist
from psiu.models import User, Perfil

def run():
    print("Starting verification...")
    admin = User.objects.filter(username='admin')
    if not admin.exists():
        admin = User.objects.create_superuser('admin', 'admin@gmail.com', 'admin')
        print("Admin user created")
    else:
        admin = admin[0]
        print("Admin already exists")

    try:
        admin.perfil
        print("Perfil already exists")
    except ObjectDoesNotExist:
        perfil = Perfil(user=admin, bio = "bio", instagram = "insta", twitter = "twi")
        perfil.save()
        print("Perfil created")
