from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from role.models import CustomUser, Role

class RoleAssignmentTest(TestCase):
    def setUp(self):
        self.admin_role=Role.objects.create(name="admin")
        self.student_role=Role.objects.create(name="student")
        self.teacher_role=Role.objects.create(name="teacher")
    
    def test_create_user_with_roles(self):
        user = CustomUser.objects.create_user(
            username='testuser',
            password='testpassword',
        )
        user.roles.add(self.admin_role, self.student_role)
        user.save()

        self.assertIn(self.admin_role,user.roles.all())
        self.assertIn(self.student_role, user.roles.all())
        self.assertNotIn(self.teacher_role, user.roles.all())
        self.assertEqual(user.roles.count(),2)
    
    def test_user_without_roles(self):
        user = CustomUser.objects.create_user(
            username='testuser2',
            password='testpassword2',
        )
        self.assertEqual(user.roles.count(), 0)
    
    def test_user_with_single_role(self):
        user = CustomUser.objects.create_user(
            username='testuser3',
            password='testpassword3',
        )
        user.roles.add(self.teacher_role)
        user.save()

        self.assertIn(self.teacher_role, user.roles.all())
        self.assertEqual(user.roles.count(), 1)