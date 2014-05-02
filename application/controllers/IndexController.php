<?php

class IndexController extends Zend_Controller_Action
{

    public function init() {
        /* Initialize action controller here */
    }

    public function indexAction() {
      $mShen = new Application_Model_Shen();
      $shen_list = $mShen->getShenList();
      //$chunks_shen_list = array_chunk($shen_list, count($shen_list) / 2);
      $chunks_shen_list = array($shen_list);
      $this->view->chunks_shen_list = $chunks_shen_list;
    }
}

