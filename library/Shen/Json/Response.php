<?php

class Shen_Json_Response  {
  /**
   * @var Zend_Controller_Request_Abstract
   */
  private $req;
  /**
   *
   * @var Zend_Controller_Response_Abstract
   */
  private $res;
  public function __construct($req, $res) {
    $this->req = $req;
    $this->res = $res;
  }
  
  public static function getInstance($request, $response) {
    $json = new self($request, $response);
    return $json;
  }
  public function json($data, $code = 200, $extra = array()) {
    $output = array(
        "data" => $data,
        "error" => NULL, 
        "code" => $code,
        "extra" => $extra
    );
    
    $this->res->setHeader("Content-Type", "application/json; charset=utf-8");
    $this->res->sendHeaders();
    print json_encode($output);
    die();
  }
  
  public function error() {
    
  }
}