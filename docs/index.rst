SonarQube SDK Documentation
============================

A fully-typed Python SDK for the SonarQube API.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   quickstart
   api/index

Installation
------------

Install with pip:

.. code-block:: bash

   pip install sonarqube-sdk

Or with uv:

.. code-block:: bash

   uv add sonarqube-sdk

Quick Start
-----------

.. code-block:: python

   from sonarqube import SonarQubeClient

   # Initialize client with token authentication
   client = SonarQubeClient(
       base_url="https://sonarqube.example.com",
       token="your-token"
   )

   # Search for projects
   projects = client.projects.search(q="backend")
   for project in projects.components:
       print(f"Project: {project.name}")

   # Get issues
   issues = client.issues.search(
       project_keys=["my-project"],
       severities=["CRITICAL", "BLOCKER"]
   )

API Reference
-------------

.. toctree::
   :maxdepth: 2

   api/client
   api/applications
   api/projects
   api/issues
   api/rules
   api/qualitygates
   api/qualityprofiles

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

