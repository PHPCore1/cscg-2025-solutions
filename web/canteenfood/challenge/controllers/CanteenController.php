<?php
class CanteenController
{
    public function index($router)
    {
        $food = new CanteenModel(0);
        if(isset($_GET['price'])) {
            return $router->view('index', ['food' => $food->filterFood($_GET['price'])]);
        }
        return $router->view('index', ['food' => $food->getFood()]);
    }
}