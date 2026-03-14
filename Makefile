# Databricks Multi-agent Workflow - Deployment Automation

# Variables
WORKSPACE_PATH = /Workspace/Users/fioriofederico99@gmail.com/plsa-app
APP_NAME = plsa-app

.PHONY: deploy sync

# Main deployment target
deploy:
	databricks bundle deploy -t dev
	databricks sync . $(WORKSPACE_PATH) --exclude-from .databricksignore --full
	databricks apps deploy $(APP_NAME) --source-code-path $(WORKSPACE_PATH)
