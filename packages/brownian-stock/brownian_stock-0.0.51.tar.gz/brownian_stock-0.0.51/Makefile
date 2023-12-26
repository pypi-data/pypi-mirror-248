

.PHONY: clean
clean:
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf brownian_stock.egg-info
	rm -rf tmp
	rm -rf build
	rm -rf dist
	rm -rf .cache

.PHONY: fmt
fmt:
	pysen run format
	pysen run lint
