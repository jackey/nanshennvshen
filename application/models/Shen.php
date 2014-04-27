<?php

class Application_Model_Shen
{	
   const  SHEN_BOY = 1;
   const  SHEN_GIRL = 0;
   
   /**
    *
    * @var Zend_XmlRpc_Client
    */
   protected $rpc_client;


   public function __construct() {
    $this->rpc_client = new Zend_XmlRpc_Client(SHEN_API_URL);
    $this->rpc_client->getHttpClient()->setCookieJar(TRUE);
  }
  
  public function getShenList($gender = 0, $page = 1) {
    $token = $this->getAccessToken();
    $login_res = $this->rpc_client->call("user.login", array(SHEN_API_USER, SHEN_API_PASS));
    
    $shen_list = $this->rpc_client->call("nvshen.index");
    return $shen_list;
	}
  
  public function getAccessToken() {
    $request = new Zend_Http_Client(SHEN_API_TOKEN);
    $res = $request->request();
    $body = $res->getBody();
    return $body;
  }
}

