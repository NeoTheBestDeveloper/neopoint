.PHONY: clean

clean:
	rm -rf dist

test:
	./scripts/test.sh

checks:
	./scripts/checks.sh
