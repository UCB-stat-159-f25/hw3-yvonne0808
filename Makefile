# Makefile for HW3 LIGO project

# --- Variables ---
ENV_NAME = ligo

# --- Targets ---
# 1. Create or update the conda environment
env:
	@echo "Setting up environment: $(ENV_NAME)"
	@if conda env list | grep -q "$(ENV_NAME)"; then \
		echo "Environment $(ENV_NAME) already exists. Updating..."; \
		conda env update --name $(ENV_NAME) --file environment.yml --prune; \
	else \
		echo "Creating new environment $(ENV_NAME)..."; \
		conda env create --file environment.yml; \
	fi
	@echo "Environment setup complete!"

# 2. Build HTML version of MyST site
html:
	@echo "Building HTML documentation..."
	myst build --html
	@echo "HTML build complete! You can view it locally under _build/html/"

# 3. Clean generated files
clean:
	@echo "Cleaning up generated folders..."
	rm -rf figures audio _build
	@echo "Cleanup complete!"s
