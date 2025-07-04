from django.test import TestCase
from role.models import CustomUser
from students.models import Student

class StudentModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="amaz", password="amaz")

    def test_create_student(self):
        student = Student.objects.create(
            name="Amaz",
            email="amaz@gmail.com",
            order=1,
            user=self.user
        )

        self.assertEqual(student.name, "Amaz")
        self.assertEqual(student.email, "amaz@gmail.com")
        self.assertEqual(student.order, 1)
        self.assertEqual(student.user.username, "amaz")
# assertEqual is used in unit testing , checks whether 2 vals are equal