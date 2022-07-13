#Install protobuf compiler on Linux
sudo apt install -y protobuf-compiler
# Alternative method to isntall protobuf compiler on linux
# wget https://github.com/protocolbuffers/protobuf/releases/download/v21.1/protoc-21.1-linux-x86_64.zip
# unzip protoc-21.1-linux-x86_64.zip

#Protobuf compiler on Windows
#wget https://github.com/protocolbuffers/protobuf/releases/download/v21.1/protoc-21.1-win64.zip
#unzip protoc-21.1-win64.zip
#cp protoc.exe $HOME/bin/protoc.exe

go get google.golang.org/protobuf/cmd/protoc-gen-go@v1.27
go get google.golang.org/grpc/cmd/protoc-gen-go-grpc@v1.1
go get github.com/grpc-ecosystem/grpc-gateway/protoc-gen-swagger
go install google.golang.org/protobuf/cmd/protoc-gen-go@v1.27
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@v1.1
go install github.com/grpc-ecosystem/grpc-gateway/protoc-gen-swagger

go get github.com/grpc-ecosystem/grpc-gateway/v2/protoc-gen-grpc-gateway 
go get github.com/grpc-ecosystem/grpc-gateway/v2/protoc-gen-openapiv2 
go get google.golang.org/protobuf/cmd/protoc-gen-go
go get google.golang.org/grpc/cmd/protoc-gen-go-grpc
go install github.com/grpc-ecosystem/grpc-gateway/v2/protoc-gen-grpc-gateway 
go install github.com/grpc-ecosystem/grpc-gateway/v2/protoc-gen-openapiv2 
go install google.golang.org/protobuf/cmd/protoc-gen-go
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc

#install grpcweb on MacOS
#wget https://github.com/grpc/grpc-web/releases/download/1.3.1/protoc-gen-grpc-web-1.3.1-darwin-x86_64
#sudo cp protoc-gen-grpc-web-1.3.1-darwin-x86_64 /usr/local/bin/protoc-gen-grpc-web

# install grpcweb on Linux
wget https://github.com/grpc/grpc-web/releases/download/1.3.1/protoc-gen-grpc-web-1.3.1-linux-x86_64
sudo mv protoc-gen-grpc-web-1.3.1-linux-x86_64 /usr/local/bin/protoc-gen-grpc-web
sudo chmod +x /usr/local/bin/protoc-gen-grpc-web

# Protobuf all for reference
#wget https://github.com/protocolbuffers/protobuf/releases/download/v21.1/protobuf-all-21.1.zip

#googleapi annotations as needed
#mkdir -p google/api
#curl https://raw.githubusercontent.com/googleapis/googleapis/master/google/api/annotations.proto > google/api/annotations.proto
#curl https://raw.githubusercontent.com/googleapis/googleapis/master/google/api/http.proto > google/api/http.proto

#curl https://github.com/protocolbuffers/protobuf/blob/main/src/google/protobuf/descriptor.proto > google/protobuf/descriptor.proto 
#curl https://github.com/protocolbuffers/protobuf/blob/main/src/google/protobuf/descriptor.proto > google/protobuf/struct.proto


