"""
Sample Python application for security scanning demonstration.
Contains intentional security anti-patterns for testing scanners.
"""
import os
import hashlib
import subprocess
import sqlite3
from typing import Optional


class UserManager:
    """Manages user operations with database."""
    
    def __init__(self, db_path: str = "users.db"):
        self.db_path = db_path
        self.connection: Optional[sqlite3.Connection] = None
    
    def connect(self) -> None:
        """Establish database connection."""
        self.connection = sqlite3.connect(self.db_path)
    
    def close(self) -> None:
        """Close database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    # SECURITY ISSUE: SQL Injection vulnerability (Bandit will catch this)
    def get_user_unsafe(self, username: str) -> Optional[dict]:
        """
        Retrieve user by username - UNSAFE method.
        This demonstrates SQL injection vulnerability.
        """
        if not self.connection:
            self.connect()
        
        cursor = self.connection.cursor()
        # Intentional SQL injection vulnerability for testing
        query = f"SELECT * FROM users WHERE username = '{username}'"  # nosec - intentional for demo
        cursor.execute(query)
        result = cursor.fetchone()
        
        if result:
            return {"id": result[0], "username": result[1], "email": result[2]}
        return None
    
    def get_user_safe(self, username: str) -> Optional[dict]:
        """
        Retrieve user by username - SAFE method using parameterized queries.
        """
        if not self.connection:
            self.connect()
        
        cursor = self.connection.cursor()
        query = "SELECT * FROM users WHERE username = ?"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        
        if result:
            return {"id": result[0], "username": result[1], "email": result[2]}
        return None
    
    def create_user(self, username: str, email: str, password: str) -> bool:
        """Create a new user with hashed password."""
        if not self.connection:
            self.connect()
        
        # Using proper parameterized query
        password_hash = self._hash_password(password)
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                (username, email, password_hash)
            )
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    # SECURITY ISSUE: Weak hashing algorithm (Bandit will catch MD5 usage)
    def _hash_password_weak(self, password: str) -> str:
        """Hash password using MD5 - WEAK and UNSAFE."""
        return hashlib.md5(password.encode()).hexdigest()  # nosec - intentional for demo
    
    def _hash_password(self, password: str) -> str:
        """Hash password using SHA-256 - Better but still not ideal for passwords."""
        # In production, use bcrypt, argon2, or scrypt
        return hashlib.sha256(password.encode()).hexdigest()


class CommandExecutor:
    """Execute system commands - demonstrates command injection risks."""
    
    # SECURITY ISSUE: Command injection vulnerability (Bandit will catch this)
    def run_unsafe(self, user_input: str) -> str:
        """
        Execute command with user input - UNSAFE.
        Demonstrates command injection vulnerability.
        """
        # Intentional command injection vulnerability for testing
        result = subprocess.run(
            f"echo {user_input}",  # nosec - intentional for demo
            shell=True,
            capture_output=True,
            text=True
        )
        return result.stdout
    
    def run_safe(self, args: list) -> str:
        """
        Execute command safely without shell interpolation.
        """
        result = subprocess.run(
            ["echo"] + args,
            shell=False,
            capture_output=True,
            text=True
        )
        return result.stdout


class ConfigManager:
    """Manage application configuration."""
    
    # SECURITY ISSUE: Hardcoded credentials (Bandit will catch this)
    DEFAULT_API_KEY = "sk-1234567890abcdef"  # nosec - intentional for demo
    DEFAULT_DB_PASSWORD = "admin123"  # nosec - intentional for demo
    
    def __init__(self):
        # Better: Load from environment variables
        self.api_key = os.environ.get("API_KEY", self.DEFAULT_API_KEY)
        self.db_password = os.environ.get("DB_PASSWORD", self.DEFAULT_DB_PASSWORD)
    
    def get_api_key(self) -> str:
        """Return configured API key."""
        return self.api_key
    
    def get_database_url(self) -> str:
        """Construct database URL."""
        host = os.environ.get("DB_HOST", "localhost")
        port = os.environ.get("DB_PORT", "5432")
        user = os.environ.get("DB_USER", "admin")
        database = os.environ.get("DB_NAME", "app")
        return f"postgresql://{user}:{self.db_password}@{host}:{port}/{database}"


def calculate_discount(price: float, discount_percent: float) -> float:
    """
    Calculate discounted price.
    
    Args:
        price: Original price
        discount_percent: Discount percentage (0-100)
    
    Returns:
        Discounted price
    """
    if price < 0:
        raise ValueError("Price cannot be negative")
    if not 0 <= discount_percent <= 100:
        raise ValueError("Discount must be between 0 and 100")
    
    discount_amount = price * (discount_percent / 100)
    return round(price - discount_amount, 2)


def process_data(data: list) -> dict:
    """
    Process a list of numbers and return statistics.
    
    Args:
        data: List of numbers to process
    
    Returns:
        Dictionary with sum, average, min, max
    """
    if not data:
        return {"sum": 0, "average": 0, "min": None, "max": None}
    
    total = sum(data)
    average = total / len(data)
    
    return {
        "sum": total,
        "average": round(average, 2),
        "min": min(data),
        "max": max(data),
        "count": len(data)
    }


def main():
    """Main entry point for demonstration."""
    print("Security Pipeline Demo Application")
    print("-" * 40)
    
    # Demo: Process some data
    sample_data = [10, 20, 30, 40, 50]
    stats = process_data(sample_data)
    print(f"Data statistics: {stats}")
    
    # Demo: Calculate discount
    original_price = 100.0
    discount = 15.0
    final_price = calculate_discount(original_price, discount)
    print(f"Price after {discount}% discount: ${final_price}")
    
    # Demo: Config manager (reads from env)
    config = ConfigManager()
    print(f"Database URL configured: {config.get_database_url()[:30]}...")


if __name__ == "__main__":
    main()

