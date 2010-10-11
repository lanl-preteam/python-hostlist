VERSIONED_FILES = hostlist.py hostlist hostlist.1 \
		  hostgrep hostgrep.1 \
		  dbuck dbuck.1 \
		  pshbak pshbak.1 \
		  setup.py python-hostlist.spec README 
NON_VERSIONED_FILES = test COPYING MANIFEST.in CHANGES Makefile

VERSION = 1.10
RELEASE = 1

all:
	@echo "Do:"
	@echo "  make tar  - build tar.gz source distribution"
	@echo "  make rpms - build RPMs (to standard RPM directories)"
	@echo "  make pypi - upload tar.gz to the Python Package Index"

prepare:
	rm -rf versioned
	mkdir versioned
	cp -pr $(NON_VERSIONED_FILES) versioned
	for f in $(VERSIONED_FILES); do sed -e "s/#VERSION#/$(VERSION)/" -e "s/#RELEASE#/$(RELEASE)/" <$$f >versioned/$$f; done

tar: prepare
	(cd versioned; make tar-versioned)

tar-versioned:
	python setup.py sdist

rpms: tar
	rpmbuild -ta versioned/dist/python-hostlist-$(VERSION).tar.gz

pypi: prepare
	(cd versioned; make pypi-versioned)

pypi-versioned:
	python setup.py sdist upload

clean:
	rm -rf versioned


