FROM golang:1.16-alpine

RUN apk update && apk add git

ENV GOPATH /go
ADD . /go/src/visit-counter

WORKDIR /go/src/visit-counter

RUN go install visit-counter
RUN ls -al /go/bin/
ENV REDISHOST redis
ENV REDISPORT 6379

ENTRYPOINT /go/bin/visit-counter

EXPOSE 8080
