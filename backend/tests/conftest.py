"""测试共享夹具"""
import pytest
from app.database import engine, Base


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """所有测试前确保表已创建"""
    Base.metadata.create_all(bind=engine)
    yield
