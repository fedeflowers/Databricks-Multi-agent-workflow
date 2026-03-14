# Deployment Instructions

## Prerequisites
- Databricks CLI installed and configured.
- Permissions to create catalogs and schemas in Unity Catalog.

## Step 1: Initialize Unity Catalog
Run the DDL scripts in `setup/DDL.md`.

## Step 2: Deploy Asset Bundle
```bash
databricks bundle deploy
```

## Step 3: Verify Deployment
- Check Model Serving for agent endpoints.
- Check Databricks Apps for Custom MCP server.
