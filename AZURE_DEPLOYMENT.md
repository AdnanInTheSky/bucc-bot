# Azure Container Instances Deployment Guide

This guide will help you deploy your BUCC Discord Bot to Azure Container Instances using your $100 free credit.

## Prerequisites

- Azure account with $100 free credit
- Azure CLI installed (or use Azure Cloud Shell)
- Your Discord bot token
- Your Google Sheet ID

## Cost Estimate

**Azure Container Instance (1 vCPU, 1.5 GB RAM)**: ~$10-15/month
- Your $100 credit will last **6-10 months**

## Step 1: Install Azure CLI (Optional - Skip if using Cloud Shell)

### Windows:
Download and install from: https://aka.ms/installazurecliwindows

### macOS:
```bash
brew install azure-cli
```

### Linux:
```bash
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

## Step 2: Login to Azure

```bash
az login
```

This will open a browser window for authentication.

## Step 3: Create a Resource Group

```bash
az group create --name bucc-discord-bot-rg --location eastus
```

**Note**: You can change `eastus` to your preferred region (e.g., `westeurope`, `southeastasia`)

## Step 4: Create Azure Container Registry (ACR)

```bash
az acr create --resource-group bucc-discord-bot-rg --name buccbotregistry --sku Basic
```

**Note**: Registry name must be unique globally. If `buccbotregistry` is taken, try adding numbers like `buccbotregistry123`

## Step 5: Login to Container Registry

```bash
az acr login --name buccbotregistry
```

## Step 6: Build and Push Docker Image

Get your registry login server:
```bash
az acr show --name buccbotregistry --query loginServer --output tsv
```

This will output something like: `buccbotregistry.azurecr.io`

Build and push the image:
```bash
# Navigate to your project directory
cd D:\Projects\BUCC-Discord-BOT

# Build the Docker image
az acr build --registry buccbotregistry --image bucc-discord-bot:latest .
```

## Step 7: Create Container Instance

Replace the placeholders with your actual values:
- `YOUR_DISCORD_BOT_TOKEN` - Your Discord bot token
- `YOUR_GOOGLE_SHEET_ID` - Your Google Sheet ID

```bash
az container create \
  --resource-group bucc-discord-bot-rg \
  --name bucc-discord-bot \
  --image buccbotregistry.azurecr.io/bucc-discord-bot:latest \
  --cpu 1 \
  --memory 1.5 \
  --registry-login-server buccbotregistry.azurecr.io \
  --registry-username buccbotregistry \
  --registry-password $(az acr credential show --name buccbotregistry --query "passwords[0].value" -o tsv) \
  --environment-variables \
    DISCORD_BOT_TOKEN=YOUR_DISCORD_BOT_TOKEN \
    GOOGLE_SHEET_ID=YOUR_GOOGLE_SHEET_ID \
  --restart-policy Always
```

**Important**: For better security, use `--secure-environment-variables` instead of `--environment-variables` for sensitive data:

```bash
az container create \
  --resource-group bucc-discord-bot-rg \
  --name bucc-discord-bot \
  --image buccbotregistry.azurecr.io/bucc-discord-bot:latest \
  --cpu 1 \
  --memory 1.5 \
  --registry-login-server buccbotregistry.azurecr.io \
  --registry-username buccbotregistry \
  --registry-password $(az acr credential show --name buccbotregistry --query "passwords[0].value" -o tsv) \
  --secure-environment-variables \
    DISCORD_BOT_TOKEN=YOUR_DISCORD_BOT_TOKEN \
    GOOGLE_SHEET_ID=YOUR_GOOGLE_SHEET_ID \
  --restart-policy Always
```

## Step 8: Verify Deployment

Check the container status:
```bash
az container show --resource-group bucc-discord-bot-rg --name bucc-discord-bot --query "{Status:instanceView.state, IP:ipAddress.ip}" --output table
```

View logs:
```bash
az container logs --resource-group bucc-discord-bot-rg --name bucc-discord-bot --follow
```

## Updating Your Bot

When you make code changes:

1. Rebuild and push the image:
```bash
az acr build --registry buccbotregistry --image bucc-discord-bot:latest .
```

2. Restart the container:
```bash
az container restart --resource-group bucc-discord-bot-rg --name bucc-discord-bot
```

## Managing Your Bot

### View logs:
```bash
az container logs --resource-group bucc-discord-bot-rg --name bucc-discord-bot --follow
```

### Stop the bot:
```bash
az container stop --resource-group bucc-discord-bot-rg --name bucc-discord-bot
```

### Start the bot:
```bash
az container start --resource-group bucc-discord-bot-rg --name bucc-discord-bot
```

### Delete the bot (to save credits):
```bash
az container delete --resource-group bucc-discord-bot-rg --name bucc-discord-bot --yes
```

## Monitoring Costs

Check your remaining credit:
1. Go to https://portal.azure.com
2. Navigate to "Cost Management + Billing"
3. View "Credits" to see remaining balance

## Alternative: Using Azure Portal (GUI Method)

If you prefer a graphical interface:

1. Go to https://portal.azure.com
2. Search for "Container Instances" and click "Create"
3. Fill in the details:
   - **Resource Group**: Create new "bucc-discord-bot-rg"
   - **Container name**: bucc-discord-bot
   - **Image source**: Azure Container Registry
   - **Registry**: Select your registry
   - **Image**: bucc-discord-bot
   - **OS type**: Linux
   - **Size**: 1 vCPU, 1.5 GB memory
4. In "Advanced" tab, add environment variables:
   - `DISCORD_BOT_TOKEN`
   - `GOOGLE_SHEET_ID`
5. Set **Restart policy** to "Always"
6. Click "Review + Create"

## Troubleshooting

### Bot not starting:
```bash
az container logs --resource-group bucc-discord-bot-rg --name bucc-discord-bot
```

### Check if environment variables are set:
```bash
az container show --resource-group bucc-discord-bot-rg --name bucc-discord-bot --query "containers[0].environmentVariables"
```

### Registry authentication issues:
```bash
az acr credential show --name buccbotregistry
```

## Cleanup (When Done)

To delete everything and stop charges:
```bash
az group delete --name bucc-discord-bot-rg --yes --no-wait
```

## Support

If you encounter issues, check:
- Azure Container Instances documentation: https://docs.microsoft.com/azure/container-instances/
- Your bot logs using the commands above
- Discord bot status in Discord Developer Portal
