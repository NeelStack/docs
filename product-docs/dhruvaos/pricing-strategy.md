# Pricing Strategy — DhruvaOS

## 1. Pricing Model
DhruvaOS adopts a **per-student, per-month SaaS** billing model. This ensures pricing scales with the school's size, lowering the barrier to entry for smaller schools while capturing value from larger institutions.

## 2. Pricing Tiers

### 2.1 Starter Tier
- **Target**: Small schools, primary schools, and newly established tutoring centers.
- **Limit**: Up to 500 active students.
- **Price**: ₹50 / student / month (billed annually).
- **Core Features**: Student profiles, basic attendance, accounts transaction tracking, core reporting, email notifications.
- **Payment Processing**: Standard Razorpay gateway (2% transaction fee).

### 2.2 Growth Tier (Recommended)
- **Target**: Private K-12 schools, CBSE/ICSE colleges, and medium academies.
- **Limit**: Up to 2000 active students.
- **Price**: ₹75 / student / month (billed annually).
- **Features**: Everything in Starter + Examination, Payroll, HR, Library, Hostel, Transportation, Socket.io chat, Capacitor Mobile App, and Parent Portal.
- **AI Add-on**: Base prompt Q&A assistant (500 tokens/student included).

### 2.3 Enterprise Tier
- **Target**: Multi-branch franchises, university networks, and international school chains.
- **Limit**: Unlimited students.
- **Price**: Custom pricing (negotiated contract).
- **Features**: Everything in Growth + Dedicated database instance (silo deployment option), custom subdomain configuration, API gateway rate-limit overrides, custom branding themes, and priority SLA support.
- **AI Add-on**: Custom fine-tuned predictions and dedicated vector space.

## 3. Revenue Projections (Local Market Focus)
- **CBSE Average School Size**: 1,200 students.
- **Annual Contract Value (ACV) per Growth School**: `1200 * ₹75 * 12` = **₹10,80,000** (INR).
- **Cost of Infrastructure (managed RDS/EKS/OpenSearch)**: ~₹1,20,000 annually per 1,200 students.
- **Gross Profit Margin**: **~88%**.
