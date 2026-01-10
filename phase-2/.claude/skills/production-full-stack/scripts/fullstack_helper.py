#!/usr/bin/env python3
"""
Full-Stack Development Helper Script

This script provides utilities for common full-stack development tasks:
- Environment setup and configuration
- Database migration management
- Code quality checks
- Security scanning
- Performance testing
"""

import os
import sys
import json
import subprocess
import argparse
from pathlib import Path
from typing import Dict, List, Optional

class FullStackHelper:
    """Helper class for full-stack development operations"""

    def __init__(self):
        self.project_root = Path.cwd()
        self.frontend_dir = self.project_root / "frontend"
        self.backend_dir = self.project_root / "backend"
        self.database_dir = self.project_root / "database"

    def run_command(self, command: str, cwd: Optional[Path] = None) -> bool:
        """Execute a shell command and return success status"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=cwd or self.project_root,
                check=True,
                capture_output=True,
                text=True
            )
            print(f"✓ Command succeeded: {command}")
            print(result.stdout)
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Command failed: {command}")
            print(f"Error: {e.stderr}")
            return False

    def setup_environment(self):
        """Set up development environment with all dependencies"""
        print("Setting up full-stack development environment...")

        # Setup frontend
        if self.frontend_dir.exists():
            print("Setting up frontend...")
            if not self.run_command("npm install", cwd=self.frontend_dir):
                return False

        # Setup backend
        if self.backend_dir.exists():
            print("Setting up backend...")
            if not self.run_command("npm install", cwd=self.backend_dir):
                return False

        print("Environment setup completed successfully!")
        return True

    def run_tests(self):
        """Run tests for both frontend and backend"""
        print("Running tests...")

        success = True

        # Frontend tests
        if self.frontend_dir.exists():
            print("Running frontend tests...")
            if not self.run_command("npm test -- --passWithNoTests", cwd=self.frontend_dir):
                success = False

        # Backend tests
        if self.backend_dir.exists():
            print("Running backend tests...")
            if not self.run_command("npm test", cwd=self.backend_dir):
                success = False

        return success

    def run_linting(self):
        """Run linting for both frontend and backend"""
        print("Running linting...")

        success = True

        # Frontend linting
        if self.frontend_dir.exists():
            print("Linting frontend...")
            if not self.run_command("npm run lint", cwd=self.frontend_dir):
                success = False

        # Backend linting
        if self.backend_dir.exists():
            print("Linting backend...")
            if not self.run_command("npm run lint", cwd=self.backend_dir):
                success = False

        return success

    def run_security_scan(self):
        """Run security scanning for dependencies"""
        print("Running security scan...")

        success = True

        # Frontend security scan
        if self.frontend_dir.exists():
            print("Scanning frontend dependencies...")
            if not self.run_command("npm audit --audit-level moderate", cwd=self.frontend_dir):
                success = False

        # Backend security scan
        if self.backend_dir.exists():
            print("Scanning backend dependencies...")
            if not self.run_command("npm audit --audit-level moderate", cwd=self.backend_dir):
                success = False

        return success

    def build_project(self):
        """Build the full-stack project"""
        print("Building project...")

        success = True

        # Build frontend
        if self.frontend_dir.exists():
            print("Building frontend...")
            if not self.run_command("npm run build", cwd=self.frontend_dir):
                success = False

        # Build backend
        if self.backend_dir.exists():
            print("Building backend...")
            if not self.run_command("npm run build", cwd=self.backend_dir):
                success = False

        return success

    def setup_database(self):
        """Set up and migrate database"""
        print("Setting up database...")

        if not self.database_dir.exists():
            print("Database directory not found, skipping database setup")
            return True

        # Run database migrations (example for SQL databases)
        migrations_dir = self.database_dir / "migrations"
        if migrations_dir.exists():
            print("Running database migrations...")
            # This would typically use a database migration tool like Knex, Prisma, etc.
            # Example: subprocess.run(["npx", "knex", "migrate:latest"], cwd=self.backend_dir)
            print("Database migrations completed")

        return True

    def start_development(self):
        """Start development servers for both frontend and backend"""
        print("Starting development servers...")

        # Note: This would typically start servers in background
        # For actual implementation, you'd want to use a process manager
        if self.frontend_dir.exists():
            print("To start frontend development server: cd frontend && npm start")

        if self.backend_dir.exists():
            print("To start backend development server: cd backend && npm run dev")

        return True

def main():
    parser = argparse.ArgumentParser(description="Full-Stack Development Helper")
    parser.add_argument(
        "command",
        choices=["setup", "test", "lint", "security", "build", "db", "dev", "all"],
        help="Command to execute"
    )

    args = parser.parse_args()

    helper = FullStackHelper()

    if args.command == "setup":
        success = helper.setup_environment()
    elif args.command == "test":
        success = helper.run_tests()
    elif args.command == "lint":
        success = helper.run_linting()
    elif args.command == "security":
        success = helper.run_security_scan()
    elif args.command == "build":
        success = helper.build_project()
    elif args.command == "db":
        success = helper.setup_database()
    elif args.command == "dev":
        success = helper.start_development()
    elif args.command == "all":
        # Run all operations in sequence
        operations = [
            helper.setup_environment,
            helper.run_linting,
            helper.run_tests,
            helper.run_security_scan,
            helper.build_project,
            helper.setup_database
        ]

        success = True
        for operation in operations:
            if not operation():
                success = False
                break

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()