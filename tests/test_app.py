"""Tests for app.py module."""
import pytest
from src.app import calculate_discount, process_data, ConfigManager


class TestCalculateDiscount:
    """Tests for calculate_discount function."""
    
    def test_valid_discount(self):
        """Test discount calculation with valid inputs."""
        assert calculate_discount(100.0, 10) == 90.0
        assert calculate_discount(100.0, 25) == 75.0
        assert calculate_discount(50.0, 50) == 25.0
    
    def test_zero_discount(self):
        """Test with zero discount."""
        assert calculate_discount(100.0, 0) == 100.0
    
    def test_full_discount(self):
        """Test with 100% discount."""
        assert calculate_discount(100.0, 100) == 0.0
    
    def test_negative_price_raises(self):
        """Test that negative price raises ValueError."""
        with pytest.raises(ValueError, match="Price cannot be negative"):
            calculate_discount(-10.0, 10)
    
    def test_invalid_discount_raises(self):
        """Test that invalid discount percentage raises ValueError."""
        with pytest.raises(ValueError, match="Discount must be between"):
            calculate_discount(100.0, 150)
        with pytest.raises(ValueError, match="Discount must be between"):
            calculate_discount(100.0, -10)
    
    def test_decimal_precision(self):
        """Test decimal precision in results."""
        result = calculate_discount(99.99, 33.33)
        assert isinstance(result, float)
        # Should be rounded to 2 decimal places
        assert result == round(result, 2)


class TestProcessData:
    """Tests for process_data function."""
    
    def test_valid_data(self):
        """Test with valid numeric data."""
        result = process_data([10, 20, 30, 40, 50])
        assert result["sum"] == 150
        assert result["average"] == 30.0
        assert result["min"] == 10
        assert result["max"] == 50
        assert result["count"] == 5
    
    def test_empty_data(self):
        """Test with empty list."""
        result = process_data([])
        assert result["sum"] == 0
        assert result["average"] == 0
        assert result["min"] is None
        assert result["max"] is None
    
    def test_single_element(self):
        """Test with single element."""
        result = process_data([42])
        assert result["sum"] == 42
        assert result["average"] == 42.0
        assert result["min"] == 42
        assert result["max"] == 42
        assert result["count"] == 1
    
    def test_negative_numbers(self):
        """Test with negative numbers."""
        result = process_data([-10, -5, 0, 5, 10])
        assert result["sum"] == 0
        assert result["average"] == 0.0
        assert result["min"] == -10
        assert result["max"] == 10
    
    def test_float_values(self):
        """Test with floating point values."""
        result = process_data([1.5, 2.5, 3.5])
        assert result["sum"] == 7.5
        assert result["average"] == 2.5


class TestConfigManager:
    """Tests for ConfigManager class."""
    
    def test_default_values(self, monkeypatch):
        """Test that defaults are used when env vars not set."""
        # Clear relevant env vars
        monkeypatch.delenv("API_KEY", raising=False)
        monkeypatch.delenv("DB_PASSWORD", raising=False)
        
        config = ConfigManager()
        # Should use default values
        assert config.api_key == ConfigManager.DEFAULT_API_KEY
        assert config.db_password == ConfigManager.DEFAULT_DB_PASSWORD
    
    def test_env_override(self, monkeypatch):
        """Test that environment variables override defaults."""
        monkeypatch.setenv("API_KEY", "custom-api-key")
        monkeypatch.setenv("DB_PASSWORD", "custom-password")
        
        config = ConfigManager()
        assert config.api_key == "custom-api-key"
        assert config.db_password == "custom-password"
    
    def test_database_url_format(self, monkeypatch):
        """Test database URL construction."""
        monkeypatch.setenv("DB_HOST", "testhost")
        monkeypatch.setenv("DB_PORT", "5433")
        monkeypatch.setenv("DB_USER", "testuser")
        monkeypatch.setenv("DB_NAME", "testdb")
        monkeypatch.setenv("DB_PASSWORD", "testpass")
        
        config = ConfigManager()
        url = config.get_database_url()
        
        assert "testhost" in url
        assert "5433" in url
        assert "testuser" in url
        assert "testdb" in url
        assert "testpass" in url
        assert url.startswith("postgresql://")

