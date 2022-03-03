# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

VERSION ?= latest
RELEASE_SRC = apisix-python-plugin-runner-${VERSION}-src

.PHONY: setup
setup:
	python3 -m pip install --upgrade pip
	python3 -m pip install -r requirements.txt --ignore-installed


.PHONY: test
test:
	pytest --version || python3 -m pip install pytest-cov
	python3 -m pytest --cov=apisix/runner tests


.PHONY: install
install: clean
	python3 setup.py install --force


.PHONY: lint
lint: clean
	flake8 --version || python3 -m pip install flake8
	flake8 . --count --select=E9,F63,F7,F82 --show-source
	flake8 . --count --max-complexity=15 --max-line-length=120


.PHONY: clean
clean:
	rm -rf apache_apisix.egg-info dist build assets .coverage report.html release
	find . -name "__pycache__" -exec rm -r {} +
	find . -name ".pytest_cache" -exec rm -r {} +
	find . -name "*.pyc" -exec rm -r {} +


.PHONY: dev
dev:
	export PYTHONPATH=$(PWD) && python3 bin/py-runner start


.PHONY: release
release:
	tar -zcvf $(RELEASE_SRC).tgz apisix bin docs tests conf setup.py *.md \
 	LICENSE Makefile NOTICE pytest.ini requirements.txt
	gpg --batch --yes --armor --detach-sig $(RELEASE_SRC).tgz
	shasum -a 512 $(RELEASE_SRC).tgz > $(RELEASE_SRC).tgz.sha512
	mkdir -p release
	mv $(RELEASE_SRC).tgz release/$(RELEASE_SRC).tgz
	mv $(RELEASE_SRC).tgz.asc release/$(RELEASE_SRC).tgz.asc
	mv $(RELEASE_SRC).tgz.sha512 release/$(RELEASE_SRC).tgz.sha512
