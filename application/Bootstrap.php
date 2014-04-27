<?php

class Bootstrap extends Zend_Application_Bootstrap_Bootstrap
{

  protected function setConstants($constants) {
     foreach ($constants as $name => $contant) {
       if (!defined($name)) {
         define($name, $contant);
       }
     }
  }
}

