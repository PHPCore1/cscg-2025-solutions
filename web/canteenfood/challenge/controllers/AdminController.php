<?php
class AdminController
{
    public function admin($router)
    {
        if($_SESSION["admin"] === false) {
            return $router->view('admin', ['logs' => "Only access allowed for canteen admin!!!"]);
        } else {
            $admin = new AdminModel("/logs.txt","");
            return $router->view('admin', ['logs' => $admin->read_logs("/logs.txt")]);
        }

    }
}
