from decimal import Decimal
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from restaurant_app.forms import ContactForm, ReservationForm, RegisterProfileForm
from restaurant_app.models import Category, ContactMessage, Order, OrderItem, Product, Profile, Reservation


# ==============================================================================
# MODEL TESTS
# ==============================================================================

class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Sushi", order=1)

    def test_category_creation(self):
        self.assertEqual(self.category.name, "Sushi")
        self.assertEqual(self.category.order, 1)

    def test_category_str(self):
        self.assertEqual(str(self.category), "Sushi")


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Sushi", order=1)
        self.product = Product.objects.create(
            category=self.category,
            name="Salmon Roll",
            description="Rulou cu somon",
            price=Decimal("35.00"),
            availability=True,
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, "Salmon Roll")
        self.assertEqual(self.product.price, Decimal("35.00"))
        self.assertTrue(self.product.availability)

    def test_product_str(self):
        self.assertEqual(str(self.product), "Salmon Roll")

    def test_product_default_availability_is_true(self):
        product = Product.objects.create(
            category=self.category,
            name="Tuna Roll",
            price=Decimal("30.00"),
        )
        self.assertTrue(product.availability)


class ContactMessageModelTest(TestCase):
    def setUp(self):
        self.message = ContactMessage.objects.create(
            name="Ion Popescu",
            email="ion@test.com",
            subject="Intrebare",
            message="Am o intrebare.",
        )

    def test_contact_message_creation(self):
        self.assertEqual(self.message.name, "Ion Popescu")
        self.assertEqual(self.message.subject, "Intrebare")

    def test_contact_message_default_is_read_false(self):
        self.assertFalse(self.message.is_read)

    def test_contact_message_str(self):
        self.assertEqual(str(self.message), "Intrebare - Ion Popescu")


class ReservationModelTest(TestCase):
    def test_reservation_creation(self):
        reservation = Reservation.objects.create(
            full_name="Maria Ionescu",
            email="maria@test.com",
            phone="0721000000",
            date="2025-12-01",
            time_slot="13:00:00",
            guests=2,
        )
        self.assertEqual(reservation.full_name, "Maria Ionescu")
        self.assertEqual(reservation.guests, 2)

    def test_reservation_str(self):
        reservation = Reservation.objects.create(
            full_name="Maria Ionescu",
            email="maria@test.com",
            phone="0721000000",
            date="2025-12-01",
            time_slot="13:00:00",
            guests=2,
        )
        self.assertIn("Maria Ionescu", str(reservation))


class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@test.com",
            password="testpass123",
        )
        self.profile = Profile.objects.create(
            user=self.user,
            username="testuser",
            email="test@test.com",
            name="Test User",
            phone="0721000000",
            home_address="Str. Test 1",
            city="Bucuresti",
            district="Sector 1",
        )

    def test_profile_creation(self):
        self.assertEqual(self.profile.name, "Test User")
        self.assertEqual(self.profile.city, "Bucuresti")

    def test_profile_str(self):
        self.assertEqual(str(self.profile), "testuser")


class OrderModelTest(TestCase):
    def setUp(self):
        self.order = Order.objects.create(
            order_number="TEST123",
            full_name="Ion Test",
            email="ion@test.com",
            phone="0721000000",
            address="Str. Test 1",
            city="Bucuresti",
            district="Sector 1",
            zipcode="010101",
            payment_method="cash",
            total_price=Decimal("100.00"),
        )

    def test_order_creation(self):
        self.assertEqual(self.order.order_number, "TEST123")
        self.assertEqual(self.order.status, "pending")
        self.assertEqual(self.order.total_price, Decimal("100.00"))

    def test_order_str(self):
        self.assertIn("TEST123", str(self.order))
        self.assertIn("Ion Test", str(self.order))


class OrderItemModelTest(TestCase):
    def setUp(self):
        self.order = Order.objects.create(
            order_number="TEST456",
            full_name="Ion Test",
            email="ion@test.com",
            phone="0721000000",
            address="Str. Test 1",
            city="Bucuresti",
            district="Sector 1",
            zipcode="010101",
            payment_method="cash",
            total_price=Decimal("70.00"),
        )
        self.item = OrderItem.objects.create(
            order=self.order,
            product_name="Salmon Roll",
            product_price=Decimal("35.00"),
            quantity=2,
        )

    def test_order_item_creation(self):
        self.assertEqual(self.item.product_name, "Salmon Roll")
        self.assertEqual(self.item.quantity, 2)

    def test_order_item_get_total_price(self):
        self.assertEqual(self.item.get_total_price(), Decimal("70.00"))

    def test_order_item_str(self):
        self.assertEqual(str(self.item), "2x Salmon Roll")


# ==============================================================================
# FORM TESTS
# ==============================================================================

class ContactFormTest(TestCase):
    def test_valid_form(self):
        form = ContactForm(data={
            "name": "Ion Popescu",
            "email": "ion@test.com",
            "subject": "Test",
            "message": "Mesaj de test.",
        })
        self.assertTrue(form.is_valid())

    def test_invalid_form_missing_fields(self):
        form = ContactForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
        self.assertIn("email", form.errors)
        self.assertIn("message", form.errors)

    def test_invalid_form_bad_email(self):
        form = ContactForm(data={
            "name": "Ion",
            "email": "nu-este-email",
            "subject": "Test",
            "message": "Mesaj.",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)


class ReservationFormTest(TestCase):
    def test_valid_form(self):
        form = ReservationForm(data={
            "full_name": "Maria Test",
            "email": "maria@test.com",
            "phone": "0721000000",
            "date": "2025-12-01",
            "time_slot": "13:00:00",
            "guests": 2,
        })
        self.assertTrue(form.is_valid())

    def test_invalid_form_missing_required_fields(self):
        form = ReservationForm(data={})
        self.assertFalse(form.is_valid())

    def test_invalid_form_bad_email(self):
        form = ReservationForm(data={
            "full_name": "Maria",
            "email": "nu-email",
            "phone": "0721000000",
            "date": "2025-12-01",
            "time_slot": "13:00:00",
            "guests": 2,
        })
        self.assertFalse(form.is_valid())


class RegisterProfileFormTest(TestCase):
    def test_valid_registration_form(self):
        form = RegisterProfileForm(data={
            "username": "newuser",
            "email": "new@test.com",
            "password1": "TestPass123!",
            "password2": "TestPass123!",
            "name": "New User",
            "phone": "0721000000",
            "home_address": "Str. Nou 1",
            "city": "Cluj",
            "district": "Cluj",
        })
        self.assertTrue(form.is_valid())

    def test_invalid_form_passwords_dont_match(self):
        form = RegisterProfileForm(data={
            "username": "newuser",
            "email": "new@test.com",
            "password1": "TestPass123!",
            "password2": "AltParola999!",
            "name": "New User",
            "phone": "0721000000",
            "home_address": "Str. Nou 1",
            "city": "Cluj",
            "district": "Cluj",
        })
        self.assertFalse(form.is_valid())

    def test_invalid_form_missing_phone(self):
        form = RegisterProfileForm(data={
            "username": "newuser",
            "email": "new@test.com",
            "password1": "TestPass123!",
            "password2": "TestPass123!",
            "name": "New User",
            "phone": "",
            "home_address": "Str. Nou 1",
            "city": "Cluj",
            "district": "Cluj",
        })
        self.assertFalse(form.is_valid())


# ==============================================================================
# VIEW TESTS - PAGINI PUBLICE
# ==============================================================================

class HomeViewTest(TestCase):
    def test_home_page_returns_200(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")


class AboutUsViewTest(TestCase):
    def test_about_us_page_returns_200(self):
        response = self.client.get(reverse("about_us"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "about_us.html")


class MenuViewTest(TestCase):
    def test_menu_page_returns_200(self):
        response = self.client.get(reverse("menu"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "menu.html")

    def test_menu_page_shows_available_products(self):
        category = Category.objects.create(name="Sushi", order=1)
        Product.objects.create(category=category, name="Salmon Roll", price=Decimal("35.00"), availability=True)
        Product.objects.create(category=category, name="Indisponibil Roll", price=Decimal("20.00"), availability=False)

        response = self.client.get(reverse("menu"))
        self.assertContains(response, "Salmon Roll")
        self.assertNotContains(response, "Indisponibil Roll")


class ContactUsViewTest(TestCase):
    def test_contact_page_returns_200(self):
        response = self.client.get(reverse("contact_us"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "contact_us.html")

    def test_contact_form_post_valid_saves_message(self):
        response = self.client.post(reverse("contact_us"), data={
            "name": "Ion Test",
            "email": "ion@test.com",
            "subject": "Test subiect",
            "message": "Mesaj de test.",
        })
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertRedirects(response, reverse("contact_us"))

    def test_contact_form_post_invalid_does_not_save(self):
        self.client.post(reverse("contact_us"), data={
            "name": "",
            "email": "nu-email",
            "subject": "",
            "message": "",
        })
        self.assertEqual(ContactMessage.objects.count(), 0)


class BookReservationViewTest(TestCase):
    def test_reservation_page_returns_200(self):
        response = self.client.get(reverse("book_reservation"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reservation.html")

    def test_valid_reservation_is_saved(self):
        response = self.client.post(reverse("book_reservation"), data={
            "full_name": "Maria Test",
            "email": "maria@test.com",
            "phone": "0721000000",
            "date": "2025-12-01",
            "time_slot": "13:00:00",
            "guests": 2,
        })
        self.assertEqual(Reservation.objects.count(), 1)

    def test_reservation_rejected_when_slot_full(self):
        for _ in range(5):
            Reservation.objects.create(
                full_name="Persoana Test",
                email="p@test.com",
                phone="0721000000",
                date="2025-12-01",
                time_slot="13:00:00",
                guests=2,
            )
        self.client.post(reverse("book_reservation"), data={
            "full_name": "Nou Test",
            "email": "nou@test.com",
            "phone": "0722000000",
            "date": "2025-12-01",
            "time_slot": "13:00:00",
            "guests": 2,
        })
        self.assertEqual(Reservation.objects.count(), 5)


# ==============================================================================
# VIEW TESTS - PAGINI FOOTER
# ==============================================================================

class FooterPagesViewTest(TestCase):
    def test_complaints_page_returns_200(self):
        response = self.client.get(reverse("complaints"))
        self.assertEqual(response.status_code, 200)

    def test_payments_page_returns_200(self):
        response = self.client.get(reverse("payments"))
        self.assertEqual(response.status_code, 200)

    def test_allergens_page_returns_200(self):
        response = self.client.get(reverse("allergens"))
        self.assertEqual(response.status_code, 200)

    def test_terms_page_returns_200(self):
        response = self.client.get(reverse("terms"))
        self.assertEqual(response.status_code, 200)

    def test_privacy_page_returns_200(self):
        response = self.client.get(reverse("privacy"))
        self.assertEqual(response.status_code, 200)

    def test_cookies_page_returns_200(self):
        response = self.client.get(reverse("cookies"))
        self.assertEqual(response.status_code, 200)

    def test_data_security_page_returns_200(self):
        response = self.client.get(reverse("data"))
        self.assertEqual(response.status_code, 200)

    def test_company_page_returns_200(self):
        response = self.client.get(reverse("company"))
        self.assertEqual(response.status_code, 200)


# ==============================================================================
# VIEW TESTS - AUTENTIFICARE
# ==============================================================================

class RegisterViewTest(TestCase):
    def test_register_page_returns_200(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register.html")

    def test_valid_registration_creates_user_and_profile(self):
        self.client.post(reverse("register"), data={
            "username": "newuser",
            "email": "new@test.com",
            "password1": "TestPass123!",
            "password2": "TestPass123!",
            "name": "New User",
            "phone": "0721000000",
            "home_address": "Str. Nou 1",
            "city": "Cluj",
            "district": "Cluj",
            "terms": "on",
        })
        self.assertTrue(User.objects.filter(username="newuser").exists())
        self.assertTrue(Profile.objects.filter(username="newuser").exists())

    def test_registration_without_terms_fails(self):
        self.client.post(reverse("register"), data={
            "username": "newuser",
            "email": "new@test.com",
            "password1": "TestPass123!",
            "password2": "TestPass123!",
            "name": "New User",
            "phone": "0721000000",
            "home_address": "Str. Nou 1",
            "city": "Cluj",
            "district": "Cluj",
        })
        self.assertFalse(User.objects.filter(username="newuser").exists())


class LoginViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")

    def test_login_page_returns_200(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_valid_login_redirects(self):
        response = self.client.post(reverse("login"), data={
            "username": "testuser",
            "password": "testpass123",
        })
        self.assertNotEqual(response.status_code, 401)

    def test_invalid_login_stays_on_page(self):
        response = self.client.post(reverse("login"), data={
            "username": "testuser",
            "password": "parolagresita",
        })
        self.assertEqual(response.status_code, 200)


class LogoutViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")

    def test_logout_redirects_to_home(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("logout"))
        self.assertRedirects(response, reverse("home"))


# ==============================================================================
# VIEW TESTS - PROFIL (PROTECTED)
# ==============================================================================

class ProfileViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        Profile.objects.create(
            user=self.user,
            username="testuser",
            email="test@test.com",
        )

    def test_profile_requires_login(self):
        response = self.client.get(reverse("profile"))
        self.assertRedirects(response, "/conectare/?next=/profil/")

    def test_logged_in_user_can_access_profile(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user_profile.html")


# ==============================================================================
# VIEW TESTS - COS
# ==============================================================================

class CartViewTest(TestCase):
    def test_empty_cart_returns_200(self):
        response = self.client.get(reverse("cart"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cart.html")

    def test_cart_total_is_zero_when_empty(self):
        response = self.client.get(reverse("cart"))
        self.assertEqual(response.context["total"], 0)

    def test_add_to_cart_adds_product(self):
        category = Category.objects.create(name="Sushi", order=1)
        product = Product.objects.create(
            category=category,
            name="Salmon Roll",
            price=Decimal("35.00"),
            availability=True,
        )
        self.client.post(reverse("add_to_cart", args=[product.id]))
        cart = self.client.session.get("cart", {})
        self.assertIn(str(product.id), cart)
        self.assertEqual(cart[str(product.id)]["quantity"], 1)

    def test_add_same_product_twice_increases_quantity(self):
        category = Category.objects.create(name="Sushi", order=1)
        product = Product.objects.create(
            category=category,
            name="Salmon Roll",
            price=Decimal("35.00"),
            availability=True,
        )
        self.client.post(reverse("add_to_cart", args=[product.id]))
        self.client.post(reverse("add_to_cart", args=[product.id]))
        cart = self.client.session.get("cart", {})
        self.assertEqual(cart[str(product.id)]["quantity"], 2)

    def test_remove_from_cart_removes_product(self):
        category = Category.objects.create(name="Sushi", order=1)
        product = Product.objects.create(
            category=category,
            name="Salmon Roll",
            price=Decimal("35.00"),
            availability=True,
        )
        self.client.post(reverse("add_to_cart", args=[product.id]))
        self.client.post(reverse("remove_from_cart", args=[product.id]))
        cart = self.client.session.get("cart", {})
        self.assertNotIn(str(product.id), cart)


# ==============================================================================
# VIEW TESTS - CHECKOUT
# ==============================================================================

class CheckoutViewTest(TestCase):
    def test_checkout_with_empty_cart_redirects(self):
        response = self.client.get(reverse("checkout"))
        self.assertRedirects(response, reverse("cart"))

    def test_checkout_with_items_returns_200(self):
        session = self.client.session
        session["cart"] = {"1": {"name": "Salmon Roll", "price": 35.00, "quantity": 1}}
        session.save()
        response = self.client.get(reverse("checkout"))
        self.assertEqual(response.status_code, 200)


# ==============================================================================
# VIEW TESTS - COMENZI
# ==============================================================================

class OrderSuccessViewTest(TestCase):
    def setUp(self):
        self.order = Order.objects.create(
            order_number="TEST789",
            full_name="Ion Test",
            email="ion@test.com",
            phone="0721000000",
            address="Str. Test 1",
            city="Bucuresti",
            district="Sector 1",
            zipcode="010101",
            payment_method="cash",
            total_price=Decimal("100.00"),
        )

    def test_order_success_page_returns_200(self):
        response = self.client.get(reverse("order_success", args=[self.order.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "order_success.html")

    def test_order_success_page_shows_order_number(self):
        response = self.client.get(reverse("order_success", args=[self.order.id]))
        self.assertContains(response, "TEST789")

    def test_invalid_order_id_returns_404(self):
        response = self.client.get(reverse("order_success", args=[99999]))
        self.assertEqual(response.status_code, 404)


# ==============================================================================
# VIEW TESTS - FAVORITE
# ==============================================================================

class FavoritesViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.profile = Profile.objects.create(
            user=self.user,
            username="testuser",
            email="test@test.com",
        )
        self.category = Category.objects.create(name="Sushi", order=1)
        self.product = Product.objects.create(
            category=self.category,
            name="Salmon Roll",
            price=Decimal("35.00"),
            availability=True,
        )

    def test_add_to_favorites_requires_login(self):
        response = self.client.post(reverse("add_favorite", args=[self.product.id]))
        self.assertEqual(response.status_code, 302)
        self.assertNotIn(self.product, self.profile.favorites.all())

    def test_logged_in_user_can_add_favorite(self):
        self.client.login(username="testuser", password="testpass123")
        self.client.post(reverse("add_favorite", args=[self.product.id]))
        self.assertIn(self.product, self.profile.favorites.all())

    def test_adding_existing_favorite_removes_it(self):
        self.client.login(username="testuser", password="testpass123")
        self.profile.favorites.add(self.product)
        self.client.post(reverse("add_favorite", args=[self.product.id]))
        self.assertNotIn(self.product, self.profile.favorites.all())


# ==============================================================================
# URL TESTS
# ==============================================================================

class URLTest(TestCase):
    def test_home_url_resolves(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_about_us_url_resolves(self):
        response = self.client.get(reverse("about_us"))
        self.assertEqual(response.status_code, 200)

    def test_menu_url_resolves(self):
        response = self.client.get(reverse("menu"))
        self.assertEqual(response.status_code, 200)

    def test_contact_us_url_resolves(self):
        response = self.client.get(reverse("contact_us"))
        self.assertEqual(response.status_code, 200)

    def test_reservation_url_resolves(self):
        response = self.client.get(reverse("book_reservation"))
        self.assertEqual(response.status_code, 200)

    def test_cart_url_resolves(self):
        response = self.client.get(reverse("cart"))
        self.assertEqual(response.status_code, 200)
