#~/P/W/aio ❯❯❯ twine upload dist/*                                                                                                                                                                                                                                                                                           ⏎
#~/P/W/aio ❯❯❯ python3 setup.py sdist bdist_wheel                                                                                                                                                                                                                                                                            ⏎
#~/P/W/aio ❯❯❯ rm -rf pywhistle.egg-info build dist

all: pywhistle.egg-info

pywhistle.egg-info:
	python3 setup.py sdist bdist_wheel

clean:
	rm -rf pywhistle.egg-info build dist

push:
	twine upload dist/*
