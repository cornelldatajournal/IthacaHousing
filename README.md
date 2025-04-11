# IthacaInsights.com  
[Visit Here](https://ithacainsights.com/)

Ithaca Insights is a real-time dashboard for housing data in Ithaca, NY. It helps users explore rental trends, compare listings, and understand the local Ithaca housing market.

---

## What It Does

- 📍 Maps available housing listings in Ithaca  
- 🏘️ Clusters neighborhoods by price and location  
- 🧮 Compares predicted vs. listed rents  

Ithaca Insights is designed to serve students and renters looking for a fair deal, as well as researchers and anyone looking to understand Ithaca’s housing landscape without guesswork.

---
## Why It Exists

**Finding housing in Ithaca is a tough cookie. Listings are scattered, and prices vary a ton.
**---

## Stack

- **Frontend**: FastAPI, Vue + TS, deployed via Fly.io  
- **Backend**: PostgreSQL, SQLAlchemy, and REST endpoints  
- **Data**: Parsed live from Ithaca’s rental feeds
- **Model**: Spatial Random Forest Regressor
- **Infra**: Docker app with CI/CD on GitHub Actions  
- **Monitoring**: Prometheus + Grafana metrics available at `/metrics`
  
---
