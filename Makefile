.PHONY: lint verify-bundle

# Raccourcis : la logique est dans scripts/sandbox/.
lint:
	bash scripts/sandbox/lint.sh

verify-bundle:
	python3 scripts/sandbox/verify_bundle.py $(ARGS)
