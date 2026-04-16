## Module 12 Reflection

### 1. What I implemented

- Built user endpoints for registration and login.
- Implemented calculation BREAD endpoints (browse, read, add, edit, delete).
- Integrated SQLAlchemy models and Pydantic schemas with route handlers.
- Added integration tests for both user and calculation flows.
- Configured GitHub Actions to run tests automatically.
- Added Docker image build and push stage for continuous deployment.

### 2. Challenges I faced

- Handling database differences between local development and CI.
- Preventing app import-time DB failures in automated workflows.
- Making route validation and error status codes consistent with tests.
- Ensuring password handling remained secure and testable.

### 3. How I solved them

- Used environment-driven database URLs.
- Moved table initialization to app startup instead of import time.
- Added robust integration tests for positive and negative cases.
- Updated CI workflow to provision PostgreSQL and run tests before Docker push.

### 4. What I learned

- Integration testing catches behavior issues that unit tests often miss.
- CI reliability depends on explicit environment setup (DB, env vars, dependencies).
- API design is clearer when schemas and response models are enforced consistently.
- End-to-end automation (test + build + deploy) improves development confidence.

### 5. Next improvements

- Replace placeholder login token with real JWT authentication and protected routes.
- Add Alembic migrations for production-grade schema evolution.
- Add test coverage for authorization and multi-user data isolation.
