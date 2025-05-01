<?php

if($_SESSION["admin"] === false){
    return "You're not welcome. This part is only for canteen workers.";
}


class AdminModel {
    public $filename;
    public $logcontent;

    public function __construct($filename, $content) { // TODO: Magic-Method
        $this->filename = $filename;
        $this->logcontent = $content;
        file_put_contents($filename, $content, FILE_APPEND);
    }

    public function __wakeup() { // TODO: Magic-Method
        // FIXME: RCE through POP-Chain, by appending to another PHP-Script
        new LogFile($this->filename, $this->logcontent);
    }

    public static function read_logs($log) {
        $contents = file_get_contents($log);
        return $contents;
    }
}

class LogFile {
    public function __construct($filename, $content) { // TODO: Magic-Method
        file_put_contents($filename, $content, FILE_APPEND);
    }
}
