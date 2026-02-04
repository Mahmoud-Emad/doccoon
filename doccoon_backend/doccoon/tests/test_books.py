from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from doccoon.models.book import BOOK_STATUS, DoccoonPage, doccoon
from doccoon.models.user import User


def create_book(author, title="Test Book", **kwargs):
    """Helper to create a book with default values."""
    defaults = {
        "description": "Test description",
        "year": 2024,
        "status": BOOK_STATUS.Draft,
    }
    defaults.update(kwargs)
    return doccoon.objects.create(title=title, author=author, **defaults)


class BookCRUDTests(TestCase):
    """Tests for book CRUD operations."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@example.com",
            password="TestPass123!",
        )
        self.other_user = User.objects.create_user(
            email="other@example.com",
            password="OtherPass123!",
        )
        self.client.force_authenticate(user=self.user)
        self.books_url = "/api/books/"

    def test_create_book(self):
        """Test creating a new book."""
        response = self.client.post(
            self.books_url,
            {
                "title": "My Test Book",
                "description": "A test description",
                "year": 2024,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()["results"]
        self.assertEqual(data["title"], "My Test Book")
        self.assertEqual(data["status"], BOOK_STATUS.Draft)
        self.assertTrue(doccoon.objects.filter(title="My Test Book").exists())

    def test_list_books(self):
        """Test listing user's books."""
        create_book(self.user, title="Book 1")
        create_book(self.user, title="Book 2", status=BOOK_STATUS.Published)
        # Book from another user - should not appear
        create_book(self.other_user, title="Other Book")

        response = self.client.get(self.books_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertEqual(len(results), 2)
        titles = [book["title"] for book in results]
        self.assertIn("Book 1", titles)
        self.assertIn("Book 2", titles)
        self.assertNotIn("Other Book", titles)

    def test_get_book_detail(self):
        """Test getting a single book with pages."""
        book = create_book(self.user, title="Detail Book")
        DoccoonPage.objects.create(book=book, page_number=1, content="Page 1 content")
        DoccoonPage.objects.create(book=book, page_number=2, content="Page 2 content")

        response = self.client.get(f"{self.books_url}{book.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()["results"]
        self.assertEqual(data["title"], "Detail Book")
        self.assertEqual(len(data["pages"]), 2)

    def test_update_book(self):
        """Test updating a book."""
        book = create_book(self.user, title="Original Title")

        response = self.client.put(
            f"{self.books_url}{book.id}/",
            {"title": "Updated Title", "description": "New description", "year": 2024},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        book.refresh_from_db()
        self.assertEqual(book.title, "Updated Title")

    def test_delete_book(self):
        """Test soft-deleting a book."""
        book = create_book(self.user, title="To Delete")

        response = self.client.delete(f"{self.books_url}{book.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        book.refresh_from_db()
        self.assertEqual(book.status, BOOK_STATUS.Deleted)

    def test_deleted_book_not_in_list(self):
        """Test that deleted books don't appear in list."""
        create_book(self.user, title="Active Book")
        create_book(self.user, title="Deleted Book", status=BOOK_STATUS.Deleted)

        response = self.client.get(self.books_url)
        results = response.json()["results"]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "Active Book")

    def test_publish_book(self):
        """Test publishing a draft book."""
        book = create_book(self.user, title="Draft Book")

        response = self.client.post(f"{self.books_url}{book.id}/publish/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        book.refresh_from_db()
        self.assertEqual(book.status, BOOK_STATUS.Published)

    def test_unpublish_book(self):
        """Test unpublishing a published book."""
        book = create_book(
            self.user, title="Published Book", status=BOOK_STATUS.Published
        )

        response = self.client.post(f"{self.books_url}{book.id}/publish/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        book.refresh_from_db()
        self.assertEqual(book.status, BOOK_STATUS.Draft)

    def test_cannot_publish_others_book(self):
        """Test that user cannot publish another user's book."""
        book = create_book(self.other_user, title="Other's Book")

        response = self.client.post(f"{self.books_url}{book.id}/publish/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_book_not_found(self):
        """Test accessing non-existent book returns 404."""
        response = self.client.get(f"{self.books_url}99999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_access(self):
        """Test that unauthenticated users cannot access books."""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.books_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PageCRUDTests(TestCase):
    """Tests for page CRUD operations."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@example.com",
            password="TestPass123!",
        )
        self.client.force_authenticate(user=self.user)

        self.book = create_book(self.user, title="Test Book")
        self.pages_url = f"/api/books/{self.book.id}/pages/"

    def test_create_page(self):
        """Test creating a new page."""
        response = self.client.post(self.pages_url, {"content": "New page content"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()["results"]
        self.assertEqual(data["page_number"], 1)
        self.assertEqual(data["content"], "New page content")

    def test_create_page_auto_increments(self):
        """Test that page numbers auto-increment."""
        DoccoonPage.objects.create(book=self.book, page_number=1, content="Page 1")

        response = self.client.post(self.pages_url, {"content": "Page 2 content"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()["results"]
        self.assertEqual(data["page_number"], 2)

    def test_list_pages(self):
        """Test listing pages of a book."""
        DoccoonPage.objects.create(book=self.book, page_number=1, content="Page 1")
        DoccoonPage.objects.create(book=self.book, page_number=2, content="Page 2")

        response = self.client.get(self.pages_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertEqual(len(results), 2)

    def test_get_page_detail(self):
        """Test getting a single page."""
        page = DoccoonPage.objects.create(
            book=self.book, page_number=1, content="Page content"
        )

        response = self.client.get(f"{self.pages_url}{page.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()["results"]
        self.assertEqual(data["content"], "Page content")

    def test_update_page(self):
        """Test updating a page."""
        page = DoccoonPage.objects.create(
            book=self.book, page_number=1, content="Original content"
        )

        response = self.client.put(
            f"{self.pages_url}{page.id}/", {"content": "Updated content"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        page.refresh_from_db()
        self.assertEqual(page.content, "Updated content")

    def test_delete_page(self):
        """Test soft-deleting a page."""
        page = DoccoonPage.objects.create(
            book=self.book, page_number=1, content="To delete"
        )

        response = self.client.delete(f"{self.pages_url}{page.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        page.refresh_from_db()
        self.assertTrue(page.is_deleted)

    def test_deleted_page_not_in_list(self):
        """Test that deleted pages don't appear in list."""
        DoccoonPage.objects.create(book=self.book, page_number=1, content="Active")
        deleted_page = DoccoonPage.objects.create(
            book=self.book, page_number=2, content="Deleted"
        )
        deleted_page.is_deleted = True
        deleted_page.deleted_at = timezone.now()
        deleted_page.save()

        response = self.client.get(self.pages_url)
        results = response.json()["results"]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["content"], "Active")

    def test_page_not_found(self):
        """Test accessing non-existent page returns 404."""
        response = self.client.get(f"{self.pages_url}99999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class SoftDeleteTests(TestCase):
    """Tests to verify soft delete filtering works correctly."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@example.com",
            password="TestPass123!",
        )
        self.client.force_authenticate(user=self.user)

    def test_soft_deleted_book_not_accessible(self):
        """Test that soft-deleted books are not accessible via detail endpoint."""
        book = create_book(self.user, title="Soft Deleted")
        book.is_deleted = True
        book.deleted_at = timezone.now()
        book.save()

        response = self.client.get(f"/api/books/{book.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_soft_deleted_page_not_accessible(self):
        """Test that soft-deleted pages are not accessible."""
        book = create_book(self.user, title="Book")
        page = DoccoonPage.objects.create(book=book, page_number=1, content="Content")
        page.is_deleted = True
        page.deleted_at = timezone.now()
        page.save()

        response = self.client.get(f"/api/books/{book.id}/pages/{page.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
