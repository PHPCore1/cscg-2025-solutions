<?php 

session_start();

$_SESSION["admin"] = false;

include_once "controllers/AdminController.php";
include_once "controllers/CanteenController.php";
include_once "models/AdminModel.php";
include_once "models/CanteenModel.php";
include_once "Routing.php";
include_once "Database.php";

$router = new Routing();
$router->new('GET', '/', 'CanteenController@index');
$router->new('GET', '/admin', 'AdminController@admin');

$response = $router->match();

die($response);