all:
    # install epycocotools locally
	python setup.py build_ext --inplace
	rm -rf build

install:
	# install epycocotools to the Python site-packages
	python setup.py build_ext install
	rm -rf build