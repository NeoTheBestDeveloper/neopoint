.PHONY: clean

clean:
	rm -rf dist

test:
	tox r -e python3.10,python3.11,python3.12

checks:
	tox r -e lint,types
