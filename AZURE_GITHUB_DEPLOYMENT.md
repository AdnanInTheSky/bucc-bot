# Azure App Service Deployment via GitHub

Deploy your BUCC Discord Bot to Azure using direct GitHub integration - **no CLI required!**

## Cost Estimate
- **Azure App Service (Basic B1)**: ~$13/month
- **Your $100 credit lasts**: 7-8 months

## Prerequisites
- Azure account with $100 free credit
- GitHub repository (you already have this!)
- Discord bot token
- Google Sheet ID

## Step-by-Step Deployment

### Step 1: Push Your Code to GitHub

Make sure your latest code is on GitHub:

```bash
git add .
git commit -m "Add Azure deployment files"
git push origin main
```

### Step 2: Create App Service in Azure Portal

1. Go to https://portal.azure.com
2. Click **"Create a resource"** (top left)
3. Search for **"Web App"** and click **Create**

### Step 3: Configure Basic Settings

Fill in the form:

**Basics Tab:**
- **Subscription**: Select your subscription with $100 credit
- **Resource Group**: Click "Create new" → Name it `bucc-discord-bot-rg`
- **Name**: `bucc-discord-bot` (must be globally unique - add numbers if taken)
- **Publish**: `Code`
- **Runtime stack**: `Python 3.11`
- **Operating System**: `Linux`
- **Region**: Choose closest to you (e.g., `East US`, `West Europe`, `Southeast Asia`)

**App Service Plan:**
- Click "Create new"
- **Name**: `bucc-bot-plan`
- **Pricing Plan**: Click "Explore pricing plans"
  - Select **Basic B1** (1.75 GB RAM, 1 vCPU) - ~$13/month
  - Click "Select"

Click **"Next: Deployment >"**

### Step 4: Connect GitHub

**Deployment Tab:**
- **Continuous deployment**: `Enable`
- **GitHub account**: Click "Authorize" and sign in to GitHub
- **Organization**: Select your GitHub username
- **Repository**: Select `BUCC-Discord-BOT`
- **Branch**: Select `main`

Click **"Next: Networking >"** → Keep defaults

Click **"Next: Monitoring >"** → Keep defaults

Click **"Next: Tags >"** → Skip

Click **"Review + Create"**

### Step 5: Review and Create

- Review your settings
- Click **"Create"**
- Wait 2-3 minutes for deployment

### Step 6: Configure Environment Variables

1. After deployment completes, click **"Go to resource"**
2. In the left menu, find **"Settings"** section
3. Click **"Configuration"**
4. Click **"+ New application setting"**

Add these two settings:

**First Setting:**
- **Name**: `DISCORD_BOT_TOKEN`
- **Value**: `your-actual-discord-bot-token`
- Click **OK**

**Second Setting:**
- **Name**: `GOOGLE_SHEET_ID`
- **Value**: `your-google-sheet-id`
- Click **OK**

5. Click **"Save"** at the top
6. Click **"Continue"** when prompted (this will restart the app)

### Step 7: Configure Startup Command

1. Still in **Configuration**
2. Click **"General settings"** tab
3. Find **"Startup Command"**
4. Enter: `python bot.py`
5. Click **"Save"** at the top

### Step 8: Verify Deployment

**Check Logs:**
1. In left menu, go to **"Deployment"** → **"Deployment Center"**
2. Click on the latest deployment to see build logs
3. In left menu, go to **"Monitoring"** → **"Log stream"**
4. You should see your bot starting up

**Check if Bot is Online:**
- Go to your Discord server
- Your bot should appear online!

## Managing Your Bot

### View Logs
1. Go to your App Service in Azure Portal
2. Left menu → **"Log stream"**

### Restart Bot
1. Go to your App Service
2. Click **"Restart"** at the top

### Stop Bot (Save Credits)
1. Go to your App Service
2. Click **"Stop"** at the top

### Update Bot Code
Just push to GitHub - Azure will automatically rebuild and deploy:
```bash
git add .
git commit -m "Update bot"
git push origin main
```

### Monitor Costs
1. Azure Portal → Search "Cost Management"
2. View your spending and remaining credit

## Troubleshooting

### Bot Not Starting?
**Check logs:**
1. Azure Portal → Your App Service
2. **"Log stream"** in left menu

**Common issues:**
- Environment variables not set correctly
- Python version mismatch
- Missing dependencies in requirements.txt

### Deployment Failed?
1. Go to **Deployment Center**
2. Check the build logs
3. Look for errors in the deployment history

### Bot Shows Offline?
1. Check **Log stream** for errors
2. Verify environment variables are set
3. Check Discord bot token is valid

## Alternative: Cheaper Option with Container Instances

If you want to save money (~$10/month instead of $13/month), you can use Azure Container Instances, but it requires Azure CLI or Cloud Shell. See `AZURE_DEPLOYMENT.md` for those instructions.

## Cleanup (When Done)

To delete everything and stop charges:
1. Azure Portal → **Resource groups**
2. Click `bucc-discord-bot-rg`
3. Click **"Delete resource group"** at top
4. Type the resource group name to confirm
5. Click **Delete**

## Support

If you need help:
- Check Azure App Service docs: https://docs.microsoft.com/azure/app-service/
- View bot logs in Azure Portal
- Check GitHub Actions tab for deployment logs
