# GitHub Copilot Instructions for Sean Girgis' Projects

## Overview
This document provides essential guidance for AI coding agents working within the Sean Girgis codebase. It covers the architecture, workflows, conventions, and integration points necessary for effective contributions.

## Architecture
- **HorizonScale AI**: A predictive capacity pipeline for forecasting resource utilization across 2,000+ nodes using parallel models (Prophet/XGBoost/LSTM). Key files include:
  - [src/HorizonScale/pipeline/06_turbo_prophet.py](src/HorizonScale/pipeline/06_turbo_prophet.py): High-performance forecasting engine.
  - [src/HorizonScale/pipeline/10_risk_dashboard.py](src/HorizonScale/pipeline/10_risk_dashboard.py): Interactive visual interface.

- **AWS Playground**: Contains scripts and YAML configurations for AWS services. Important files:
  - [cli.py](aws_playground/cli.py): Command-line interface for AWS interactions.
  - [requirements.txt](aws_playground/requirements.txt): Lists dependencies for the AWS project.

## Developer Workflows
- **Building and Running**: To initialize the environment and launch the risk dashboard, execute:
  ```bash
  python3 src/HorizonScale/synthetic/00_init_db.py
  python3 src/HorizonScale/pipeline/06_turbo_prophet.py
  streamlit run src/HorizonScale/pipeline/10_risk_dashboard.py
  ```

- **Testing**: Use GitHub Actions for CI/CD. Ensure all tests pass before merging any changes.

## Project-Specific Conventions
- **YAML Configuration**: All configurations are managed through YAML files located in the `data` directory. For example, to edit the resume layout, modify:
  - [data/store.yaml](data/store.yaml): Centralized content store for resumes and CVs.

- **Python Patterns**: Utilize decorators and context managers for clean code practices. Example:
  - Implement a custom context manager for file handling in ETL processes.

## Integration Points
- **Cross-Component Communication**: Components communicate through well-defined APIs. Refer to the [API and Integration Guide](https://github.com/seanlgirgis/HorizonStudy/blob/main/Docs/API_AND_INTEGRATION_GUIDE.md) for details on extending functionalities.

- **External Dependencies**: Ensure all external libraries are listed in the respective `requirements.txt` files. For example, the AWS project requires specific AWS SDKs.

## Conclusion
This document should serve as a foundational guide for AI agents to navigate and contribute effectively to the Sean Girgis codebase. For further details, refer to the project documentation and existing markdown files in the `docs` directory.