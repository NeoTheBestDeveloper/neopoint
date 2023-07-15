.PHONY: clean

clean:
	rm -rf dist

test:
	pytest -cov  --cov=neopoint -sv tests
