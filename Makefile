all:
    # install epycocotools locally
	python setup.py build_ext --inplace
	rm -rf build dist epycocotools.egg-info

install:
	# install epycocotools to the Python site-packages
	pip install .
	rm -rf build dist epycocotools.egg-info

uninstall:
	# uninstall epycocotools
	pip uninstall -y epycocotools