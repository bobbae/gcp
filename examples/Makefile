.POSIX:
DESTDIR=public

#alias si := system-info

#https://github.com/casey/just#installation

#system-info:
#	@echo from ~/justfile
#	@echo "This is an {{arch()}} machine running {{os()}}".
#	@echo PATH is {{env_var("PATH")}}
#	@echo PATH is $PATH
#	@echo current invocation directory is {{invocation_directory()}}


all:
	@echo make all is all we do


get_repository:
	@echo "🛎 Getting Pages repository"
	#git clone https://github.com/example/examples.git $(DESTDIR)


clean:
	@echo "🧹 Cleaning old build"
	#cd $(DESTDIR) && rm -rf *


get:
	@echo "❓ Checking for make"
	#@if ! [ -x "$$(command -v make)" ]; then\
	#	echo "🤵 Getting make";\
	#	sudo apt install make;\
	#fi


build:
	@echo "🍳 building"
	# do the building
	# @echo "🧂 Optimizing images"
	# do the optimizing



test:
	@echo "🍜 Testing"
	# do the testing
	#docker run -v $(GITHUB_WORKSPACE)/$(DESTDIR)/:/mnt user/examples mnt --disable-external


deploy:
	@echo "🎁 Preparing commit"
	#@cd $(DESTDIR) \
	#	&& git config user.email "user+githubaction@gmail.com" \
	#	&& git config user.name "My Examples via GitHub Actions" \
	#	&& git add . \
	#	&& git status \
	#	&& git commit -m "🤖 CD bot is helping" \
	#	&& git push -f -q https://$(TOKEN)@github.com/user/examples master
	@echo "🚀 deployed!"


run:
	@echo "Run"
	# run
	@echo "Done running"


ssh-host-keys:
	sudo ssh-keygen -b 1024 -t rsa -f /etc/ssh/ssh_host_key
	sudo ssh-keygen -b 1024 -t rsa -f /etc/ssh/ssh_host_rsa_key 
	sudo ssh-keygen -b 1024 -t dsa -f /etc/ssh/ssh_host_dsa_key


sshd-start:
	sudo service ssh start


ngrok-ssh-start:
	ngrok tcp 22


add-sudoers:
	echo "someluckyuser     ALL=(ALL:ALL) NOPASSWD:ALL" | sudo tee -a /etc/sudoers


file-server:
	deno run --allow-net --allow-read https://deno.land/std/http/file_server.ts


asdf-sbcl:
	# asdf list
	# asdf plugin add sbcl
	asdf install sbcl 2.0.4
	# asdf current
	asdf global sbcl 2.0.4


get-rush:
	# gnu parallel alternative
	go get -u github.com/shenwei356/rush/


will-cite-parallel:
	echo 'will cite' | parallel --citation 1> /dev/null 2> /dev/null &


one-click-hugo-run:
	# yarn
	npx yarn start
	# git push origin master


flask-news-update:
	git push heroku master
	# git push origin master


heroku-database:
	export DATABASE_URL=`heroku config:get DATABASE_URL -a abcdefgaaa12w3 -j`


get-starship:
	curl -sS https://starship.rs/install.sh | sh


get-rvm:
	sudo apt-get install -y software-properties-common
	sudo apt-add-repository -y ppa:rael-gc/rvm
	sudo apt-get update
	sudo apt-get install -y rvm
	sudo usermod -a -G rvm `whoami`
	#[ -f /etc/profile.d/rvm.sh ] && source /etc/profile.d/rvm.sh
	# sudo rvm install ruby


get-nvm:
	curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
	# nvm install stable
	# nvm use stable


get-pip:
	sudo apt-get install python3-distutils
	curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
	python3 get-pip.py


get-python-venv:
	sudo apt install python3.8-venv


create-venv:
	sudo apt install -y python3-venv
	python3 -m venv ~/venv-3.x.x


venv-jupyter:
	source ~/venv-3.x.x/bin/activate


create-requirements:
	pip freeze > requirements.txt


clean-requirements:
	pipreqs --force .

#refresh-just-completion-bash:
#	complete -W "$(just --summary)" just


gpg-encrypt:
	gpg -c filename


gpg-decrypt:
	gpg filename


gobox-sym-encrypt:
	gobox sym-encrypt x.tar.gz x.tar.gz.gobox


gobox-sym-decrypt:
	gobox sym-decrypt x.tar.gz.gobox x.tar.gz


gobox-encrypt: 
	gobox encrypt ~/.ssh/gobox_public ~/.ssh/gobox_private x.tar.gz x.tar.gz.gobox


gobox-decrypt:
	gobox decrypt ~/.ssh/gobox_public ~/.ssh/gobox_private  x.tar.gz.gobox x.tar.gz


gobox-genkey:
	gobox genkey ~/.ssh/gobox_public ~/.ssh/gobox_private


install-gobox:
	if [ -z `which gobox` ]; then \
		go install github.com/danderson/gobox@latest; \
	fi


xtar: install-gobox
	#mkdir -p ~/.docker && cp .docker/config.json ~/.docker/ 
	#mkdir -p ~/.config && cp .config/starship.toml ~/.config/ 
	-[ -f ~/.bashrc ] && cp ~/.bashrc ~/.bashrc_backup
	-[ -f ~/.bash_profile ] && cp ~/.bash_profile ~/.bash_profile_backup
	tar -C ~  -zcvf  x.tar.gz    .ssh .vimrc  bin/v bin/z.sh .tmux.conf .shextra .gitconfig  .bash_profile_backup .bashrc_backup .env ; 
	gobox sym-encrypt x.tar.gz x.tar.gz.gobox ; 

xuntar: install-gobox
	#cp examples/x.tar.gz.gpg
	#gpg x.tar.gz.gpg
	gobox sym-decrypt x.tar.gz.gobox ../x.tar.gz
	[ -f ~/.bashrc ] && cp ~/.bashrc ~/.bashrc_backup
	[ -f ~/.bash_profile ] && cp ~/.bash_profile ~/.bash_profile_backup
	if [ -d ~/.ssh ]; then \
		cp -r ~/.ssh ~/.ssh.backup; \
	fi
	cd ..; tar xvf x.tar.gz

common-tools: common-1 common-2 get-1
	#brew install htop fd ripgrep bat tree rush exa procs
	wget https://raw.githubusercontent.com/brushtechnology/fabricate/master/fabricate.py


common-1: common-base common-tools-build-essentials common-tools-1


common-2: common-tools-golang common-tools-fzf common-tools-nodejs common-tools-rust


get-1: get-rvm get-nvm get-pip get-python-venv get-starship


common-base:
	sudo apt update
	sudo apt install -y vim tmux openssl miller zip unzip


common-tools-fzf:
	if [ ! -d ~/.fzf ]; then \
		git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf; \
		~/.fzf/install; \
	fi


common-tools-nodejs:
	sudo apt install -y nodejs npm
	sudo npm install -g yarn


common-tools-golang:
	if [ -z `which go`  ] ; then \
		cd /usr/local && sudo wget https://golang.org/dl/go1.18.1.linux-amd64.tar.gz &&  sudo tar -C /usr/local -xzf go1.18.1.linux-amd64.tar.gz; \
		if [ -f /usr/local/bin/go ]; then \
			/usr/local/bin/go version ; \
		else \
			sudo ln -s /usr/local/go/bin/go /usr/local/bin/go; \
		fi \
	else \
		go version; \
	fi


common-tools-1:
	sudo apt install -y  htop   tree  curl wget


common-tools-build-essentials:
	sudo apt install -y build-essential


common-tools-rust: rustup
	. ~/.cargo/env
	#cargo install ripgrep
	sudo apt install ripgrep
	#cargo install cargo-edit


rustup:
	curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh


cargo-edit:
	cargo install cargo-edit


install-docker: docker-engine docker-post-install

docker-engine:
	sudo apt-get update
	sudo apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release
	curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
	echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu  `lsb_release -cs` stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
	sudo apt-get update
	sudo apt-get install docker-ce docker-ce-cli containerd.io


docker-post-install:
	-sudo groupadd docker
	sudo usermod -aG docker `whoami`
	newgrp docker
	#docker run hello-world


minikube-install:
	curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
	sudo install minikube-linux-amd64 ~/bin/minikube
	minikube start
	minikube kubectl -- get po -A
	#minikube  dashboard
	#https://minikube.sigs.k8s.io/docs/start/
	minikube stop


gcloud-install:
	wget https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-359.0.0-linux-x86_64.tar.gz
	tar xf google-cloud-sdk-*.tar.gz
	./google-cloud-sdk/install.sh
	# make sure google-cloud-sdk/bin comes before existing gcloud in /snap/bin or remove /snap/bin/gcloud
	#-sudo mv /snap/bin/gcloud /snap/bin/gcloud-old
	mv google-cloud-sdk ~
	rm google-cloud-sdk-*.tar.gz
	gcloud init
	gcloud components list
	gcloud components install kubectl

sdkman:
	curl -s https://get.sdkman.io | bash

java:
	sdk install java
	sdk install gradle
