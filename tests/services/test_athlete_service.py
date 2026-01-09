import pytest
import uuid
from unittest.mock import AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.athlete import AthleteService
from src.schemas.athlete import AthleteCreate, AthleteUpdate
from src.exceptions.custom_exceptions import NotFoundException, AlreadyExistsException


class TestAthleteService:

    @pytest.fixture
    def mock_db(self):
        return AsyncMock(spec=AsyncSession)

    @pytest.fixture
    def athlete_service(self, mock_db):
        return AthleteService(mock_db)

    @pytest.fixture
    def sample_athlete_data(self):
        return {
            "name": "João Silva",
            "cpf": "12345678901",
            "age": 25,
            "weight": 75.5,
            "height": 1.80,
            "sex": "M",
            "training_center_id": 1,
            "category_id": 2
        }

    @pytest.fixture
    def sample_athlete_response(self, sample_athlete_data):
        athlete_id = uuid.uuid4()
        return {
            **sample_athlete_data,
            "pk_id": 1,
            "id": athlete_id,
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00"
        }

    @pytest.mark.asyncio
    async def test_create_athlete_success(self, athlete_service, sample_athlete_data):
        # Arrange
        athlete_create = AthleteCreate(**sample_athlete_data)
        mock_response = {
            **sample_athlete_data,
            "pk_id": 1,
            "id": uuid.uuid4()
        }

        athlete_service.repository.get_by_cpf = AsyncMock(return_value=None)
        athlete_service.repository.create = AsyncMock(return_value=mock_response)

        # Act
        result = await athlete_service.create_athlete(athlete_create)

        # Assert
        athlete_service.repository.get_by_cpf.assert_called_once_with(athlete_create.cpf)
        athlete_service.repository.create.assert_called_once_with(**athlete_create.model_dump())
        assert result == mock_response

    @pytest.mark.asyncio
    async def test_create_athlete_cpf_already_exists(self, athlete_service, sample_athlete_data):
        # Arrange
        athlete_create = AthleteCreate(**sample_athlete_data)
        existing_athlete = {"id": uuid.uuid4(), "cpf": athlete_create.cpf}

        athlete_service.repository.get_by_cpf = AsyncMock(return_value=existing_athlete)

        # Act & Assert
        with pytest.raises(AlreadyExistsException) as exc_info:
            await athlete_service.create_athlete(athlete_create)

        assert f"Athlete with CPF '{athlete_create.cpf}' already exists" in str(exc_info.value)
        athlete_service.repository.get_by_cpf.assert_called_once_with(athlete_create.cpf)

    @pytest.mark.asyncio
    async def test_get_athlete_success(self, athlete_service, sample_athlete_response):
        # Arrange
        athlete_id = 1
        athlete_service.repository.get_by_id = AsyncMock(return_value=sample_athlete_response)

        # Act
        result = await athlete_service.get_athlete(athlete_id)

        # Assert
        athlete_service.repository.get_by_id.assert_called_once_with(athlete_id)
        assert result == sample_athlete_response

    @pytest.mark.asyncio
    async def test_get_athlete_not_found(self, athlete_service):
        # Arrange
        athlete_id = 999
        athlete_service.repository.get_by_id = AsyncMock(return_value=None)

        # Act & Assert
        with pytest.raises(NotFoundException) as exc_info:
            await athlete_service.get_athlete(athlete_id)

        assert f"Athlete with id {athlete_id} not found" in str(exc_info.value)
        athlete_service.repository.get_by_id.assert_called_once_with(athlete_id)

    @pytest.mark.asyncio
    async def test_get_athlete_by_uuid_success(self, athlete_service, sample_athlete_response):
        # Arrange
        athlete_uuid = str(sample_athlete_response["id"])
        athlete_service.repository.get_by_uuid = AsyncMock(return_value=sample_athlete_response)

        # Act
        result = await athlete_service.get_athlete_by_uuid(athlete_uuid)

        # Assert
        athlete_service.repository.get_by_uuid.assert_called_once_with(athlete_uuid)
        assert result == sample_athlete_response

    @pytest.mark.asyncio
    async def test_get_athlete_by_uuid_not_found(self, athlete_service):
        # Arrange
        athlete_uuid = str(uuid.uuid4())
        athlete_service.repository.get_by_uuid = AsyncMock(return_value=None)

        # Act & Assert
        with pytest.raises(NotFoundException) as exc_info:
            await athlete_service.get_athlete_by_uuid(athlete_uuid)

        assert f"Athlete with uuid {athlete_uuid} not found" in str(exc_info.value)
        athlete_service.repository.get_by_uuid.assert_called_once_with(athlete_uuid)

    @pytest.mark.asyncio
    async def test_get_all_athletes(self, athlete_service, sample_athlete_response):
        # Arrange
        athletes_list = [sample_athlete_response, {**sample_athlete_response, "pk_id": 2}]
        athlete_service.repository.get_all = AsyncMock(return_value=athletes_list)
        skip = 0
        limit = 100

        # Act
        result = await athlete_service.get_all_athletes(skip, limit)

        # Assert
        athlete_service.repository.get_all.assert_called_once_with(skip, limit)
        assert result == athletes_list
        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_get_all_athletes_with_pagination(self, athlete_service, sample_athlete_response):
        # Arrange
        skip = 10
        limit = 20
        athlete_service.repository.get_all = AsyncMock(return_value=[sample_athlete_response])

        # Act
        result = await athlete_service.get_all_athletes(skip=skip, limit=limit)

        # Assert
        athlete_service.repository.get_all.assert_called_once_with(skip, limit)
        assert len(result) == 1

    @pytest.mark.asyncio
    async def test_update_athlete_success(self, athlete_service, sample_athlete_response):
        # Arrange
        athlete_id = 1
        update_data = {"name": "Novo Nome", "age": 26}
        athlete_update = AthleteUpdate(**update_data)

        athlete_service.repository.get_by_id = AsyncMock(return_value=sample_athlete_response)
        athlete_service.repository.get_by_cpf = AsyncMock(return_value=None)

        updated_response = {**sample_athlete_response, **update_data}
        athlete_service.repository.update = AsyncMock(return_value=updated_response)

        # Act
        result = await athlete_service.update_athlete(athlete_id, athlete_update)

        # Assert
        athlete_service.repository.get_by_id.assert_called_once_with(athlete_id)
        athlete_service.repository.update.assert_called_once_with(athlete_id, **update_data)
        assert result == updated_response
        assert result["name"] == "Novo Nome"
        assert result["age"] == 26

    @pytest.mark.asyncio
    async def test_update_athlete_not_found(self, athlete_service):
        # Arrange
        athlete_id = 999
        athlete_update = AthleteUpdate(name="Novo Nome")
        athlete_service.repository.get_by_id = AsyncMock(return_value=None)

        # Act & Assert
        with pytest.raises(NotFoundException) as exc_info:
            await athlete_service.update_athlete(athlete_id, athlete_update)

        assert f"Athlete with id {athlete_id} not found" in str(exc_info.value)
        athlete_service.repository.get_by_id.assert_called_once_with(athlete_id)

    @pytest.mark.asyncio
    async def test_update_athlete_cpf_conflict(self, athlete_service, sample_athlete_response):
        # Arrange
        athlete_id = 1
        new_cpf = "98765432100"
        update_data = {"cpf": new_cpf}
        athlete_update = AthleteUpdate(**update_data)

        existing_athlete_with_new_cpf = {
            **sample_athlete_response,
            "pk_id": 2,
            "cpf": new_cpf
        }

        athlete_service.repository.get_by_id = AsyncMock(return_value=sample_athlete_response)
        athlete_service.repository.get_by_cpf = AsyncMock(return_value=existing_athlete_with_new_cpf)

        # Act & Assert
        with pytest.raises(AlreadyExistsException) as exc_info:
            await athlete_service.update_athlete(athlete_id, athlete_update)

        assert f"Athlete with CPF '{new_cpf}' already exists" in str(exc_info.value)
        athlete_service.repository.get_by_id.assert_called_once_with(athlete_id)
        athlete_service.repository.get_by_cpf.assert_called_once_with(new_cpf)

    @pytest.mark.asyncio
    async def test_update_athlete_same_cpf(self, athlete_service, sample_athlete_response):
        # Arrange
        athlete_id = 1
        update_data = {"name": "Novo Nome", "cpf": sample_athlete_response["cpf"]}
        athlete_update = AthleteUpdate(**update_data)

        athlete_service.repository.get_by_id = AsyncMock(return_value=sample_athlete_response)

        updated_response = {**sample_athlete_response, **update_data}
        athlete_service.repository.update = AsyncMock(return_value=updated_response)

        # Act
        result = await athlete_service.update_athlete(athlete_id, athlete_update)

        # Assert
        athlete_service.repository.get_by_id.assert_called_once_with(athlete_id)
        athlete_service.repository.update.assert_called_once_with(athlete_id, **update_data)
        assert result == updated_response

    @pytest.mark.asyncio
    async def test_delete_athlete_success(self, athlete_service, sample_athlete_response):
        # Arrange
        athlete_id = 1
        athlete_service.repository.get_by_id = AsyncMock(return_value=sample_athlete_response)
        athlete_service.repository.delete = AsyncMock(return_value=True)

        # Act
        result = await athlete_service.delete_athlete(athlete_id)

        # Assert
        athlete_service.repository.get_by_id.assert_called_once_with(athlete_id)
        athlete_service.repository.delete.assert_called_once_with(athlete_id)
        assert result is True

    @pytest.mark.asyncio
    async def test_delete_athlete_not_found(self, athlete_service):
        # Arrange
        athlete_id = 999
        athlete_service.repository.get_by_id = AsyncMock(return_value=None)

        # Act & Assert
        with pytest.raises(NotFoundException) as exc_info:
            await athlete_service.delete_athlete(athlete_id)

        assert f"Athlete with id {athlete_id} not found" in str(exc_info.value)
        athlete_service.repository.get_by_id.assert_called_once_with(athlete_id)

    @pytest.mark.asyncio
    async def test_get_athletes_by_training_center(self, athlete_service, sample_athlete_response):
        # Arrange
        training_center_id = 1
        athletes_list = [sample_athlete_response]
        athlete_service.repository.get_by_training_center = AsyncMock(return_value=athletes_list)

        # Act
        result = await athlete_service.get_athletes_by_training_center(training_center_id)

        # Assert
        athlete_service.repository.get_by_training_center.assert_called_once_with(training_center_id)
        assert result == athletes_list
        assert len(result) == 1

    @pytest.mark.asyncio
    async def test_get_athletes_by_category(self, athlete_service, sample_athlete_response):
        # Arrange
        category_id = 2
        athletes_list = [sample_athlete_response]
        athlete_service.repository.get_by_category = AsyncMock(return_value=athletes_list)

        # Act
        result = await athlete_service.get_athletes_by_category(category_id)

        # Assert
        athlete_service.repository.get_by_category.assert_called_once_with(category_id)
        assert result == athletes_list
        assert len(result) == 1

    @pytest.mark.asyncio
    async def test_get_athletes_by_age_range(self, athlete_service, sample_athlete_response):
        # Arrange
        min_age = 18
        max_age = 30
        athletes_list = [sample_athlete_response]
        athlete_service.repository.get_by_age_range = AsyncMock(return_value=athletes_list)

        # Act
        result = await athlete_service.get_athletes_by_age_range(min_age, max_age)

        # Assert
        athlete_service.repository.get_by_age_range.assert_called_once_with(min_age, max_age)
        assert result == athletes_list
        assert len(result) == 1

    @pytest.mark.asyncio
    async def test_update_athlete_with_partial_data(self, athlete_service, sample_athlete_response):
        # Arrange
        athlete_id = 1
        update_data = {"age": 26}
        athlete_update = AthleteUpdate(**update_data)

        athlete_service.repository.get_by_id = AsyncMock(return_value=sample_athlete_response)
        athlete_service.repository.get_by_cpf = AsyncMock(return_value=None)

        updated_response = {**sample_athlete_response, **update_data}
        athlete_service.repository.update = AsyncMock(return_value=updated_response)

        # Act
        result = await athlete_service.update_athlete(athlete_id, athlete_update)

        # Assert
        athlete_service.repository.update.assert_called_once_with(athlete_id, **update_data)
        assert result["age"] == 26
        assert result["name"] == sample_athlete_response["name"]