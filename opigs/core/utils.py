from .models import *
from taggit.models import Tag

def create_user(user_data, user_type, form_data):
    if user_type == 'S':
        new_user = Student.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            password=user_data['password1'],
            user_role=user_type,
            user_contact=user_data['user_contact'],
            roll_no=form_data['roll_no'],
            dept=form_data['dept'],
            CV=form_data['CV']
        )
    elif user_type == 'A':
        new_user = Alumni.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            password=user_data['password1'],
            user_role=user_type,
            user_contact=user_data['user_contact'],
            graduating_year=form_data['graduating_year'],
            dept=form_data['dept']
        )
    elif user_type == 'C':
        new_user = Company.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            password=user_data['password1'],
            user_role=user_type,
            user_contact=user_data['user_contact'],
            company_name=form_data['company_name'],
            desc=form_data['desc']
        )
    else:
        new_user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            password=user_data['password1'],
            user_role=user_type,
            user_contact=user_data['user_contact'],
        )
    tag_names = user_data['tags']
    for tag_name in tag_names:
        tag, created = Tag.objects.get_or_create(name=tag_name)
        new_user.tags.add(tag)

    return new_user