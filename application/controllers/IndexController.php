<?php

class IndexController extends Zend_Controller_Action
{

    public function init()
    {
        /* Initialize action controller here */
    }

    public function indexAction()
    {
      $mShen = new Application_Model_Shen();
      $shen_list = $mShen->getShenList();
      $this->view->shenlist = $shen_list;
    }


}

