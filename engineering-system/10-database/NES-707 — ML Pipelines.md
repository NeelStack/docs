---
document_id: NES-707
title: ML Pipelines
subtitle: Enterprise Machine Learning Pipelines, Model Registry & MLOps Standard
version: 1.0.0
status: Draft
classification: Internal
owner: AI & Data Science Board
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-706 BI
next_document: NES-708 Feature Store
---

# NES-707 — ML Pipelines

> **"Machine learning models are software products. We automate training, version models in registries, and deploy predictions via secure pipelines."**

---

# Executive Summary

Deploying Machine Learning (ML) models built on local computers by data scientists without version control, automated training paths, or validation checkpoints leads to unreliable models in production.

We mandate the adoption of standardized **ML Pipelines (MLOps)** across all NeelStack AI products.

This standard establishes our model training flows, version registries (**MLflow**), and containerized inference deployment standards.

---

# Purpose

This standard defines:

- MLOps Core Pipeline Stages
- Automated Training and Validation
- Model Registry Standards (MLflow)
- Deployment and Inference Topologies
- Drift Monitoring and Re-training Rules

---

# MLOps Pipeline Stages

All machine learning models must be developed and updated using structured pipelines:

```text
 Data Prep  ──►  Feature Extraction  ──►  Model Training  ──►  Validation  ──►  Registry
    │                  │                         │                 │             │
 Snowflake          Feature Store            Kubeflow /        Threshold       MLflow
 Queries               (Redis)               SageMaker           Check
```

---

# Model Training & Validation Gates

Model training must be reproducible and sandboxed:

- **Compute Engines**: Run training runs inside Kubernetes compute nodes (Kubeflow) or cloud managed platforms (Amazon SageMaker). Training code must be checked into Git.
- **Validation Threshold**: Prior to model promotion, models must pass automated validation rules comparing accuracy metrics (F1-score, Precision, Recall) against active baseline production models.
- **Safety Checks**: Test models against bias datasets to ensure predictions do not violate safety or compliance standards (NES-226).

---

# Model Registry Standards (MLflow)

All trained models must be registered in the centralized **MLflow Registry**.

- **Version Tracking**: MLflow must log model parameters, hyper-parameters, training datasets, artifact code weights, and environment dependencies.
- **Stage Promotion**: Model stages (e.g. `Staging`, `Production`) are managed inside MLflow and promote via automated pipeline validation runs.

```python
# Reference MLflow logging snippet
import mlflow

mlflow.set_tracking_uri("http://mlflow.data-platform.local")
with mlflow.start_run():
    mlflow.log_param("learning_rate", 0.01)
    mlflow.log_param("epochs", 10)
    mlflow.log_metric("accuracy", 0.95)
    mlflow.log_artifact("model.onnx")
    mlflow.register_model("model_uri", "invoice_ocr_model")
```

---

# Inference Deployment Topologies

Models serve predictions using two deployment models:

- **Online Inference**: Deploy models as containerized microservices running on EKS nodes with auto-scaling active. Services expose low-latency REST/gRPC endpoints.
- **Batch Inference**: Schedule periodic pipelines (using Airflow) to run predictions over large tables (e.g. nightly lead scoring) and write results back to the database.

---

# Model Drift & Retraining

Models decay in predictive performance as real-world data patterns evolve.

- **Data Drift Monitoring**: Track model performance metrics dynamically. Log prediction confidence intervals and input feature distributions.
- **Automated Retraining**: Trigger retraining pipelines automatically when prediction drift metrics deviate from baseline thresholds.

---

# Anti-Patterns

❌ **Manual Weights Copying**: Copying serialized model files (e.g., `.pkl` or `.h5` files) manually to web servers via SFTP, bypassing registries.

❌ **Omitting Training Data Linage**: Registering models in MLflow without saving the hash or link of the specific dataset used for training, making replication impossible.

❌ **Exposing Raw Python Models directly**: Exposing un-optimized raw python scripts directly to heavy web traffic, leading to CPU exhaustion. Models must be compiled (e.g. to ONNX format) for performance.

---

# Production Checklist

- [ ] Model training scripts are checked into Git.
- [ ] MLflow registry captures all parameters and weights.
- [ ] Accuracy validations are automated.
- [ ] Prediction drift metrics dashboards are active.
- [ ] Inference APIs run on auto-scaling EKS nodes.

---

# Success Criteria

The ML pipeline standard is successful when:
- Deploying a new model version is accomplished solely through automated CI/CD pipelines.
- Online prediction latencies remain within SLA limits (e.g. under 100ms).
- Model drift triggers proactive retraining before user experience degrades.

---

# Document Status

**Document:** NES-707 — ML Pipelines
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-708 — Feature Store**
