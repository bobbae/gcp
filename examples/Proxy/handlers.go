package server

import (
	"fmt"
	"net"
	"net/http"
	"net/http/httputil"
	"net/url"
	"os"
	"strings"

	"github.com/julienschmidt/httprouter"
	"github.com/kahlys/proxy"
	"gitlab.com/bobbae/kuberp/api"
	"gitlab.com/bobbae/q"
	"golang.org/x/net/context"
)

var router *httprouter.Router
var proxyMap = make(map[string]string)

type Server struct{}

func (srv *Server) Echo(ctx context.Context, req *api.EchoRequest) (res *api.EchoResponse, err error) {
	res = &api.EchoResponse{
		Message: req.Message,
	}

	return res, nil
}

func (srv *Server) Proxy(ctx context.Context, req *api.ProxyRequest) (*api.ProxyResponse, error) {
	res := &api.ProxyResponse{
		Message: req.Message,
		Status:  "ok",
	}
	var err error
	switch req.Message {
	case "add":
		if err = addProxy(req); err != nil {
			res.Status = fmt.Sprintf("error, failed to add, %v", err)
		}
	case "delete":
		if err = deleteProxy(req); err != nil {
			res.Status = fmt.Sprintf("error, failed to delete, %v", err)
		}
	case "list":
		res.Status = fmt.Sprintf("list, %v", proxyMap)
	default:
		res.Status = "error, invalid message"
	}
	return res, nil
}

func addProxy(req *api.ProxyRequest) error {
	_, ok := proxyMap[req.Path]
	if ok {
		q.Q("proxy path already exists, will replace", req)
	}
	switch req.Kind {
	case "http":
		return addHTTPProxy(req)
	case "tcp":
		return addTCPProxy(req)
	case "udp":
		return addUDPProxy(req)
	}
	return fmt.Errorf("unsupported type")
}

func addHTTPProxy(req *api.ProxyRequest) error {
	origin, err := url.Parse(req.Origin)
	if err != nil {
		return err
	}
	rp := httputil.NewSingleHostReverseProxy(origin)
	if err != nil {
		return fmt.Errorf("cannot parse origin %s, %v", origin, err)
	}
	if router == nil {
		return fmt.Errorf("no http router")
	}
	rp.Director = func(ireq *http.Request) {
		p, found := proxyMap[req.Path]
		if !found {
			return
		}
		if p == "" {
			return
		}
		if strings.HasPrefix(p, "Deleted-") {
			return
		}
		ireq.Header.Add("X-Forwarded-Host", ireq.Host)
		ireq.Header.Add("X-Origin-Host", origin.Host)
		ireq.URL.Scheme = origin.Scheme
		ireq.URL.Host = origin.Host
		wildcard := strings.Index(req.Path, "*")
		proxyPath := singleJoiningSlash(origin.Path, ireq.URL.Path[wildcard:])
		if strings.HasSuffix(proxyPath, "/") && len(proxyPath) > 1 {
			proxyPath = proxyPath[:len(proxyPath)-1]
		}
		ireq.URL.Path = proxyPath
	}
	_, ok := proxyMap[req.Path]
	if !ok {
		for _, method := range []string{"GET", "POST"} {
			router.Handle(method, req.Path, func(w http.ResponseWriter, r *http.Request, p httprouter.Params) {
				rp.ServeHTTP(w, r)
			})
		}
	}
	proxyMap[req.Path] = req.Origin
	return nil
}

var defaultCert, defaultKey string

func CheckCerts(certDir string) error {
	defaultCert = certDir + "/cert.pem"
	_, err := os.Stat(defaultCert)
	if err != nil {
		return err
	}
	defaultKey = certDir + "/key.pem"
	_, err = os.Stat(defaultKey)
	if err != nil {
		return err
	}
	return nil
}

func addTCPProxy(req *api.ProxyRequest) error {
	laddr, err := net.ResolveTCPAddr("tcp", req.Path)
	if err != nil {
		return err
	}
	raddr, err := net.ResolveTCPAddr("tcp", req.Origin)
	if err != nil {
		return err
	}
	go func() {
		proxy.NewServer(raddr, nil, nil).ListenAndServeTLS(laddr, defaultCert, defaultKey)
	}()
	return nil
}

func addUDPProxy(req *api.ProxyRequest) error {
	return nil
}

func deleteProxy(req *api.ProxyRequest) error {
	proxyMap[req.Path] = "Deleted-" + req.Origin
	//XXX no delete for tcp,udp
	return nil
}

func NewRouter() *httprouter.Router {
	router = httprouter.New()
	return router
}

func singleJoiningSlash(a, b string) string {
	aslash := strings.HasSuffix(a, "/")
	bslash := strings.HasPrefix(b, "/")
	switch {
	case aslash && bslash:
		return a + b[1:]
	case !aslash && !bslash:
		return a + "/" + b
	}
	return a + b
}
