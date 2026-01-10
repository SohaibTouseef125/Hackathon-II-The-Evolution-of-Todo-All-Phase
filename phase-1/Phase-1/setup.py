from setuptools import setup, find_packages

setup(
    name="todo-app-phase1",
    version="0.1.0",
    description="Phase 1 Todo In-Memory Python Console App",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "colorama>=0.4.6",
    ],
    entry_points={
        "console_scripts": [
            "todo-app=todo_app.main:main",
        ],
    },
    python_requires=">=3.12",
)