import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from src.services.category import CategoryService
from src.schemas.category import CategoryCreate, CategoryUpdate
from src.exceptions.custom_exceptions import NotFoundException, AlreadyExistsException


class TestCategoryService:
    """Test suite for CategoryService"""

    @pytest.fixture
    def mock_db_session(self):
        """Mock database session"""
        return AsyncMock()

    @pytest.fixture
    def category_service(self, mock_db_session):
        """CategoryService instance with mocked session"""
        return CategoryService(mock_db_session)

    @pytest.fixture
    def sample_category_data(self):
        """Sample category data for testing"""
        return {
            "id": 1,
            "uuid": "123e4767-e89b-12d3-a456-426614174000",
            "name": "Test Category"
        }

    @pytest.fixture
    def sample_category_create(self):
        """CategoryCreate schema instance"""
        return CategoryCreate(name="New Category")

    @pytest.fixture
    def sample_category_update(self):
        """CategoryUpdate schema instance"""
        return CategoryUpdate(name="Updated Category")

    # Test create_category method
    @pytest.mark.asyncio
    async def test_create_category_success(self, category_service, sample_category_create, sample_category_data):
        """Test successful category creation"""
        # Mock repository methods
        category_service.repository.get_by_name = AsyncMock(return_value=None)
        category_service.repository.create = AsyncMock(return_value=sample_category_data)

        # Execute
        result = await category_service.create_category(sample_category_create)

        # Assertions
        category_service.repository.get_by_name.assert_called_once_with(sample_category_create.name)
        category_service.repository.create.assert_called_once_with(**sample_category_create.model_dump())
        assert result == sample_category_data

    @pytest.mark.asyncio
    async def test_create_category_already_exists(self, category_service, sample_category_create, sample_category_data):
        """Test category creation when name already exists"""
        # Mock existing category
        category_service.repository.get_by_name = AsyncMock(return_value=sample_category_data)

        # Execute and assert exception
        with pytest.raises(AlreadyExistsException) as exc_info:
            await category_service.create_category(sample_category_create)

        assert f"Category with name '{sample_category_create.name}' already exists" in str(exc_info.value)
        category_service.repository.get_by_name.assert_called_once_with(sample_category_create.name)

    # Test get_category method
    @pytest.mark.asyncio
    async def test_get_category_success(self, category_service, sample_category_data):
        """Test successful category retrieval by ID"""
        # Mock repository method
        category_service.repository.get_by_id = AsyncMock(return_value=sample_category_data)

        # Execute
        result = await category_service.get_category(pk_id=1)

        # Assertions
        category_service.repository.get_by_id.assert_called_once_with(1)
        assert result == sample_category_data

    @pytest.mark.asyncio
    async def test_get_category_not_found(self, category_service):
        """Test category retrieval when not found"""
        # Mock repository method
        category_service.repository.get_by_id = AsyncMock(return_value=None)

        # Execute and assert exception
        with pytest.raises(NotFoundException) as exc_info:
            await category_service.get_category(pk_id=999)

        assert "Category with id 999 not found" in str(exc_info.value)
        category_service.repository.get_by_id.assert_called_once_with(999)

    # Test get_category_by_uuid method
    @pytest.mark.asyncio
    async def test_get_category_by_uuid_success(self, category_service, sample_category_data):
        """Test successful category retrieval by UUID"""
        # Mock repository method
        uuid = "123e4567-e89b-12d3-a456-426614174000"
        category_service.repository.get_by_uuid = AsyncMock(return_value=sample_category_data)

        # Execute
        result = await category_service.get_category_by_uuid(uuid)

        # Assertions
        category_service.repository.get_by_uuid.assert_called_once_with(uuid)
        assert result == sample_category_data

    @pytest.mark.asyncio
    async def test_get_category_by_uuid_not_found(self, category_service):
        """Test category retrieval by UUID when not found"""
        # Mock repository method
        uuid = "non-existent-uuid"
        category_service.repository.get_by_uuid = AsyncMock(return_value=None)

        # Execute and assert exception
        with pytest.raises(NotFoundException) as exc_info:
            await category_service.get_category_by_uuid(uuid)

        assert f"Category with uuid {uuid} not found" in str(exc_info.value)
        category_service.repository.get_by_uuid.assert_called_once_with(uuid)

    # Test get_all_categories method
    @pytest.mark.asyncio
    async def test_get_all_categories_success(self, category_service, sample_category_data):
        """Test successful retrieval of all categories"""
        # Mock repository method
        categories_list = [sample_category_data, {**sample_category_data, "id": 2}]
        category_service.repository.get_all = AsyncMock(return_value=categories_list)

        # Execute with custom skip and limit
        result = await category_service.get_all_categories(skip=10, limit=50)

        # Assertions
        category_service.repository.get_all.assert_called_once_with(10, 50)
        assert result == categories_list
        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_get_all_categories_default_params(self, category_service):
        """Test get_all_categories with default parameters"""
        # Mock repository method
        category_service.repository.get_all = AsyncMock(return_value=[])

        # Execute with default parameters
        result = await category_service.get_all_categories()

        # Assertions
        category_service.repository.get_all.assert_called_once_with(0, 100)
        assert result == []

    # Test update_category method
    @pytest.mark.asyncio
    async def test_update_category_success(self, category_service, sample_category_data, sample_category_update):
        """Test successful category update"""
        # Mock repository methods
        category_service.repository.get_by_id = AsyncMock(return_value=sample_category_data)
        category_service.repository.get_by_name = AsyncMock(return_value=None)
        updated_data = {**sample_category_data, "name": sample_category_update.name}
        category_service.repository.update = AsyncMock(return_value=updated_data)

        # Execute
        result = await category_service.update_category(pk_id=1, category=sample_category_update)

        # Assertions
        category_service.repository.get_by_id.assert_called_once_with(1)
        category_service.repository.get_by_name.assert_called_once_with(sample_category_update.name)
        category_service.repository.update.assert_called_once()
        assert result == updated_data

    @pytest.mark.asyncio
    async def test_update_category_not_found(self, category_service, sample_category_update):
        """Test category update when category not found"""
        # Mock repository method
        category_service.repository.get_by_id = AsyncMock(return_value=None)

        # Execute and assert exception
        with pytest.raises(NotFoundException) as exc_info:
            await category_service.update_category(pk_id=999, category=sample_category_update)

        assert "Category with id 999 not found" in str(exc_info.value)
        category_service.repository.get_by_id.assert_called_once_with(999)

    @pytest.mark.asyncio
    async def test_update_category_name_exists(self, category_service, sample_category_data, sample_category_update):
        """Test category update when new name already exists"""
        # Mock repository methods
        category_service.repository.get_by_id = AsyncMock(return_value=sample_category_data)
        existing_with_new_name = {**sample_category_data, "id": 2, "name": sample_category_update.name}
        category_service.repository.get_by_name = AsyncMock(return_value=existing_with_new_name)

        # Execute and assert exception
        with pytest.raises(AlreadyExistsException) as exc_info:
            await category_service.update_category(pk_id=1, category=sample_category_update)

        assert f"Category with name '{sample_category_update.name}' already exists" in str(exc_info.value)
        category_service.repository.get_by_id.assert_called_once_with(1)
        category_service.repository.get_by_name.assert_called_once_with(sample_category_update.name)

    @pytest.mark.asyncio
    async def test_update_category_same_name(self, category_service, sample_category_data):
        """Test category update with same name (should not check for name existence)"""
        # Mock repository methods
        category_service.repository.get_by_id = AsyncMock(return_value=sample_category_data)
        update_data = CategoryUpdate(name=sample_category_data["name"])
        category_service.repository.update = AsyncMock(return_value=sample_category_data)

        # Execute
        result = await category_service.update_category(pk_id=1, category=update_data)

        # Assertions
        category_service.repository.get_by_id.assert_called_once_with(1)
        category_service.repository.update.assert_called_once()
        assert result == sample_category_data

    @pytest.mark.asyncio
    async def test_update_category_partial(self, category_service, sample_category_data):
        """Test partial category update"""
        # Mock repository methods
        category_service.repository.get_by_id = AsyncMock(return_value=sample_category_data)
        category_service.repository.update = AsyncMock(return_value=sample_category_data)

        # Execute with partial update (empty update)
        update_data = CategoryUpdate()
        result = await category_service.update_category(pk_id=1, category=update_data)

        # Assertions
        category_service.repository.get_by_id.assert_called_once_with(1)
        category_service.repository.update.assert_called_once()

    # Test delete_category method
    @pytest.mark.asyncio
    async def test_delete_category_success(self, category_service, sample_category_data):
        """Test successful category deletion"""
        # Mock repository methods
        category_service.repository.get_by_id = AsyncMock(return_value=sample_category_data)
        category_service.repository.delete = AsyncMock(return_value=True)

        # Execute
        result = await category_service.delete_category(pk_id=1)

        # Assertions
        category_service.repository.get_by_id.assert_called_once_with(1)
        category_service.repository.delete.assert_called_once_with(1)
        assert result is True

    @pytest.mark.asyncio
    async def test_delete_category_not_found(self, category_service):
        """Test category deletion when not found"""
        # Mock repository method
        category_service.repository.get_by_id = AsyncMock(return_value=None)

        # Execute and assert exception
        with pytest.raises(NotFoundException) as exc_info:
            await category_service.delete_category(pk_id=999)

        assert "Category with id 999 not found" in str(exc_info.value)
        category_service.repository.get_by_id.assert_called_once_with(999)

    @pytest.mark.asyncio
    async def test_delete_category_failure(self, category_service, sample_category_data):
        """Test category deletion failure"""
        # Mock repository methods
        category_service.repository.get_by_id = AsyncMock(return_value=sample_category_data)
        category_service.repository.delete = AsyncMock(return_value=False)

        # Execute
        result = await category_service.delete_category(pk_id=1)

        # Assertions
        category_service.repository.get_by_id.assert_called_once_with(1)
        category_service.repository.delete.assert_called_once_with(1)
        assert result is False

    # Test edge cases and error handling
    @pytest.mark.asyncio
    async def test_create_category_with_none_name(self, category_service):
        """Test category creation with None name (should be handled by Pydantic validation)"""
        # This test assumes Pydantic validation happens before service method
        with pytest.raises(Exception):
            # This would fail in Pydantic validation layer
            invalid_category = CategoryCreate(name=None)
            await category_service.create_category(invalid_category)

    @pytest.mark.asyncio
    async def test_update_category_with_empty_update(self, category_service, sample_category_data):
        """Test update with completely empty update object"""
        # Mock repository methods
        category_service.repository.get_by_id = AsyncMock(return_value=sample_category_data)
        category_service.repository.update = AsyncMock(return_value=sample_category_data)

        # Create empty update
        empty_update = CategoryUpdate()

        # Execute
        result = await category_service.update_category(pk_id=1, category=empty_update)

        # Assertions
        category_service.repository.get_by_id.assert_called_once_with(1)
        category_service.repository.update.assert_called_once()
        assert result == sample_category_data
