Quick Start
===========

This guide will help you get started with the SonarQube SDK.

Authentication
--------------

Token Authentication (Recommended)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from sonarqube import SonarQubeClient

   client = SonarQubeClient(
       base_url="https://sonarqube.example.com",
       token="your-token"
   )

Basic Authentication
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from sonarqube import SonarQubeClient

   client = SonarQubeClient(
       base_url="https://sonarqube.example.com",
       username="admin",
       password="admin"
   )

Working with Projects
---------------------

Search Projects
^^^^^^^^^^^^^^^

.. code-block:: python

   # Search all projects
   projects = client.projects.search()

   # Search with filter
   projects = client.projects.search(q="backend")

   # Iterate over results
   for project in projects.components:
       print(f"Project: {project.name} ({project.key})")

Create a Project
^^^^^^^^^^^^^^^^

.. code-block:: python

   project = client.projects.create(
       name="My Project",
       project="my-project",
       visibility="private"
   )

Working with Issues
-------------------

Search Issues
^^^^^^^^^^^^^

.. code-block:: python

   # Get all critical issues
   issues = client.issues.search(
       project_keys=["my-project"],
       severities=["CRITICAL", "BLOCKER"]
   )

   for issue in issues.issues:
       print(f"Issue: {issue.message}")

Transition an Issue
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Mark issue as resolved
   client.issues.do_transition(
       issue="AXoN-12345",
       transition="resolve"
   )

Working with Quality Gates
--------------------------

Get Project Status
^^^^^^^^^^^^^^^^^^

.. code-block:: python

   status = client.qualitygates.project_status(
       project_key="my-project"
   )

   if status.project_status.status == "OK":
       print("Quality gate passed!")
   else:
       print("Quality gate failed!")

Error Handling
--------------

.. code-block:: python

   from sonarqube import SonarQubeClient
   from sonarqube.exceptions import (
       SonarQubeAuthenticationError,
       SonarQubeNotFoundError,
       SonarQubePermissionError,
   )

   client = SonarQubeClient(base_url="...", token="...")

   try:
       project = client.projects.search(q="test")
   except SonarQubeAuthenticationError:
       print("Invalid credentials")
   except SonarQubeNotFoundError:
       print("Resource not found")
   except SonarQubePermissionError:
       print("Permission denied")

