
go: red_black_set_mod.py red_black_dict_mod.py
	# Strictly speaking, it'd still be nice to analyze this code on 2.x, but 2.7 pylint appears to be having problems.
	./this-pylint \
		--verbose \
		--which-2 None \
		--which-python-3 /usr/local/cpython-3.10/bin/python3 \
		--ignore-message '^.*Similar lines in .* files.*$$' \
		--ignore-message '^.*Too many lines in module.*$$' \
		--to-pylint test-red_black_tree_mod red_black_set_mod.py
	/usr/local/cpython-3.10/bin/python3 ./test-red_black_tree_mod
	/usr/local/pypy3-7.3.9/bin/pypy3 test-red_black_tree_mod
	./print-tree

red_black_set_mod.py: red_black_tree_mod.m4
	m4 -Dm4set=1 -Dm4key=1 red_black_tree_mod.m4 > red_black_set_mod.py

red_black_dict_mod.py: red_black_tree_mod.m4
	m4 -Dm4set=1 -Dm4keyvalue=1 red_black_tree_mod.m4 > red_black_dict_mod.py

clean:
	rm -rf *.pyc __pycache__ *.class red_black_set_mod.py red_black_dict_mod.py MANIFEST dist

# publish: red_black_set_mod.py red_black_dict_mod.py
# 	python3 setup.py sdist upload
# 	./prepare-tarballs

publish: clean red_black_set_mod.py red_black_dict_mod.py
	python3 setup.py sdist
	twine upload dist/*

test-publish: clean red_black_set_mod.py red_black_dict_mod.py
	python3 setup.py sdist bdist_wheel
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

