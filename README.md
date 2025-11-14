# sample-python-app-with-lightsail-deploy

Application using reusable deployment workflow

## 🚀 Automated Deployment

This application uses a reusable GitHub Actions workflow for automated deployment to AWS Lightsail.

### Configuration

- **Instance**: sample-python-app
- **Region**: us-east-1
- **Type**: web

### Deployment

Push to `main` branch to trigger automatic deployment:

```bash
git push origin main
```

### Local Development

```bash
npm install
npm start
```

Visit: http://localhost:3000

## 📝 Configuration

Edit `deployment-generic.config.yml` to customize:
- AWS region and instance
- Application dependencies
- Deployment settings

## 🔗 Links

- Reusable Workflow: https://github.com/naveenraj44125-creator/lamp-stack-lightsail
