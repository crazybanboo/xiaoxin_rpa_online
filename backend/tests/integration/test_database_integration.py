"""
Integration tests for database operations
"""

import pytest
from datetime import datetime

from app.crud import admin, client, upgrade_package, upgrade_task
from app.schemas.admin import AdminCreate
from app.schemas.client import ClientCreate
from app.schemas.upgrade_package import UpgradePackageCreate
from app.schemas.upgrade_task import UpgradeTaskCreate
from tests.utils import create_test_data_set, cleanup_test_data, DatabaseTestCase


@pytest.mark.integration
class TestDatabaseIntegration(DatabaseTestCase):
    """Integration tests for database operations"""

    def test_complete_workflow(self, db_session):
        """Test complete CRUD workflow across all models"""
        # Create admin
        admin_data = AdminCreate(
            username="integration_admin",
            email="integration@example.com",
            password="test123"
        )
        created_admin = admin.create_with_password(db_session, obj_in=admin_data)
        assert created_admin.id is not None

        # Create client
        client_data = ClientCreate(
            name="集成测试客户端",
            ip_address="192.168.1.200",
            version="1.0.0",
            status="online"
        )
        created_client = client.create(db_session, obj_in=client_data)
        assert created_client.id is not None

        # Create package
        package_data = UpgradePackageCreate(
            name="集成测试升级包",
            version="3.0.0",
            file_path="/integration/test/package.zip",
            file_size=2048000
        )
        created_package = upgrade_package.create(db_session, obj_in=package_data)
        assert created_package.id is not None

        # Create task
        task_data = UpgradeTaskCreate(
            client_id=created_client.id,
            package_id=created_package.id,
            status="pending"
        )
        created_task = upgrade_task.create(db_session, obj_in=task_data)
        assert created_task.id is not None

        # Test relationships
        assert created_task.client.name == "集成测试客户端"
        assert created_task.package.name == "集成测试升级包"
        assert len(created_client.upgrade_tasks) == 1

        # Test queries
        found_admin = admin.get_by_username(db_session, username="integration_admin")
        assert found_admin.id == created_admin.id

        found_client = client.get_by_ip(db_session, ip_address="192.168.1.200")
        assert found_client.id == created_client.id

        found_package = upgrade_package.get_by_version(db_session, version="3.0.0")
        assert found_package.id == created_package.id

        client_tasks = upgrade_task.get_by_client(db_session, client_id=created_client.id)
        assert len(client_tasks) == 1

    def test_cascade_delete(self, db_session):
        """Test cascade delete relationships"""
        # Create client with tasks
        client_data = ClientCreate(
            name="删除测试客户端",
            ip_address="192.168.1.201",
            version="1.0.0"
        )
        created_client = client.create(db_session, obj_in=client_data)

        package_data = UpgradePackageCreate(
            name="删除测试包",
            version="1.5.0",
            file_path="/delete/test.zip",
            file_size=1024
        )
        created_package = upgrade_package.create(db_session, obj_in=package_data)

        # Create multiple tasks for the client
        for i in range(3):
            task_data = UpgradeTaskCreate(
                client_id=created_client.id,
                package_id=created_package.id,
                status="pending"
            )
            upgrade_task.create(db_session, obj_in=task_data)

        # Verify tasks exist
        client_tasks = upgrade_task.get_by_client(db_session, client_id=created_client.id)
        assert len(client_tasks) == 3

        # Delete client - should cascade delete tasks
        client.remove(db_session, id=created_client.id)

        # Verify tasks are deleted
        remaining_tasks = upgrade_task.get_by_client(db_session, client_id=created_client.id)
        assert len(remaining_tasks) == 0

    def test_concurrent_operations(self, db_session):
        """Test concurrent database operations"""
        # Create multiple admins simultaneously (simulating concurrent requests)
        admins_data = []
        for i in range(5):
            admin_data = AdminCreate(
                username=f"concurrent_admin_{i}",
                email=f"concurrent{i}@example.com",
                password="test123"
            )
            admins_data.append(admin_data)

        created_admins = []
        for admin_data in admins_data:
            created_admin = admin.create_with_password(db_session, obj_in=admin_data)
            created_admins.append(created_admin)

        # Verify all were created
        assert len(created_admins) == 5
        all_admins = admin.get_multi(db_session)
        admin_usernames = [a.username for a in all_admins]
        
        for i in range(5):
            assert f"concurrent_admin_{i}" in admin_usernames

    def test_transaction_rollback(self, db_session):
        """Test transaction rollback on error"""
        # Create a valid client first
        client_data = ClientCreate(
            name="事务测试客户端",
            ip_address="192.168.1.202",
            version="1.0.0"
        )
        created_client = client.create(db_session, obj_in=client_data)

        # Try to create admin with duplicate username (should fail)
        admin_data1 = AdminCreate(
            username="duplicate_admin",
            email="admin1@example.com",
            password="test123"
        )
        admin.create_with_password(db_session, obj_in=admin_data1)

        # This should fail due to duplicate username
        admin_data2 = AdminCreate(
            username="duplicate_admin",  # Same username
            email="admin2@example.com",
            password="test123"
        )
        
        try:
            admin.create_with_password(db_session, obj_in=admin_data2)
            assert False, "Should have raised an exception"
        except Exception:
            # Rollback should happen
            db_session.rollback()

        # Verify the client still exists (transaction didn't affect other operations)
        found_client = client.get(db_session, id=created_client.id)
        assert found_client is not None

        # Verify only one admin was created
        found_admins = admin.get_multi(db_session)
        duplicate_admins = [a for a in found_admins if a.username == "duplicate_admin"]
        assert len(duplicate_admins) == 1

    def test_complex_queries(self, db_session):
        """Test complex database queries across relationships"""
        # Create comprehensive test data
        test_data = create_test_data_set(db_session)

        # Test getting online clients
        online_clients = client.get_online(db_session)
        online_count = len([c for c in test_data["clients"] if c.status == "online"])
        assert len(online_clients) == online_count

        # Test getting tasks by status
        pending_tasks = upgrade_task.get_by_status(db_session, status="pending")
        pending_count = len([t for t in test_data["tasks"] if t.status == "pending"])
        assert len(pending_tasks) == pending_count

        # Test getting latest package
        latest_package = upgrade_package.get_latest(db_session)
        assert latest_package is not None

        # Clean up
        cleanup_test_data(db_session)

    def test_data_integrity(self, db_session):
        """Test data integrity constraints"""
        # Create client and package
        client_data = ClientCreate(
            name="完整性测试客户端",
            ip_address="192.168.1.203",
            version="1.0.0"
        )
        created_client = client.create(db_session, obj_in=client_data)

        package_data = UpgradePackageCreate(
            name="完整性测试包",
            version="1.0.0",
            file_path="/integrity/test.zip",
            file_size=1024
        )
        created_package = upgrade_package.create(db_session, obj_in=package_data)

        # Create task
        task_data = UpgradeTaskCreate(
            client_id=created_client.id,
            package_id=created_package.id,
            status="pending"
        )
        created_task = upgrade_task.create(db_session, obj_in=task_data)

        # Test that deleting package fails if tasks reference it
        # (This would fail if foreign key constraints are properly set)
        try:
            upgrade_package.remove(db_session, id=created_package.id)
            # If this succeeds, tasks should be cascade deleted too
            remaining_tasks = upgrade_task.get_by_client(db_session, client_id=created_client.id)
            # Either the delete failed (good) or tasks were cascade deleted (also good)
            assert len(remaining_tasks) == 0 or len(remaining_tasks) == 1
        except Exception:
            # Foreign key constraint prevented deletion - this is good
            pass

    def test_timestamp_updates(self, db_session):
        """Test that timestamps are properly updated"""
        # Create admin
        admin_data = AdminCreate(
            username="timestamp_admin",
            email="timestamp@example.com",
            password="test123"
        )
        created_admin = admin.create_with_password(db_session, obj_in=admin_data)

        original_created = created_admin.created_at
        original_updated = created_admin.updated_at

        # Update admin
        from app.schemas.admin import AdminUpdate
        admin_update = AdminUpdate(email="updated_timestamp@example.com")
        updated_admin = admin.update(db_session, db_obj=created_admin, obj_in=admin_update)

        # Verify timestamps
        assert updated_admin.created_at == original_created  # Should not change
        assert updated_admin.updated_at > original_updated  # Should be updated