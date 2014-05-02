<?php 

class FrontApiController extends Zend_Controller_Action {
	
	public function init() {
    //TODO::
	}

	public function nextshenAction() {
    $this->_helper->layout->disableLayout();
		$request = $this->getRequest();
    $next_page = $request->getParam("next");
    $gender = $request->getParam("gender", 0);
    $res = $this->getResponse();
    $shen_json = Shen_Json_Response::getInstance($this->getRequest(), $this->getResponse());
    if ($next_page) {
      $mShen = new Application_Model_Shen();
      $shen_list = $mShen->getShenList($gender, $next_page);
      if ($shen_list) {
        $chunks_shen_list = array_chunk($shen_list, count($shen_list) / 2);
        $this->view->chunks_shen_list = $chunks_shen_list;
        
        $this->renderScript("api/nextshen.phtml", array("chunks_shen_list" => $chunks_shen_list));
      }
      else {
        $this->renderScript("api/empty.phtml");
      }
    }
    else {
     $this->renderScript("api/empty.phtml");
    }
	}
}