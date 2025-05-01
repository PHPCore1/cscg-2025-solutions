<?php
class CanteenModel {


    public function getFood() {
        $log_entry = 'Access at: '. date('Y-m-d H:i:s') . "<br>\n";
        $logger = new AdminModel("/logs.txt", $log_entry);

        $db = Database::getConnection();
        $sql = "SELECT * FROM food";
        if ($result = $db->query($sql)) {
            $result_string = "";
            while($obj = $result->fetch_object()){
                if($obj->name !== '') {
                    $result_string .= $obj->name . ' for ' . $obj->price . '€ <br>';
                    $db->query("UPDATE food SET price = " . (rand(0, 100000) / 100) . " WHERE name = \"" . $obj->name. "\"");
                }

                if($obj->oldvalue !== '') {
                    $dec_result = base64_decode($obj->oldvalue);
                    if (preg_match_all('/O:\d+:"([^"]*)"/', $dec_result, $matches)) { 
                        return 'Not allowed';
                    }
                    $uns_result = unserialize($dec_result); 
                    $result_string .= $uns_result[0] . ' for ' . $uns_result[1] . '€<br>';
                    $new_value = [$uns_result[0], (rand(0, 100000) / 100)];
                    $db->query("UPDATE food SET oldvalue = \"" . base64_encode(serialize($new_value)) . "\" WHERE oldvalue = \"" . $obj->oldvalue . "\"");
                }
            }
            return $result_string;
        }
        return 'No food this week - we\'re closed';
    }

    public function filterFood($price_param) {
        $log_entry = 'Access at: '. date('Y-m-d H:i:s') .   "<br>\n";
        $logger = new AdminModel("../logs.txt", $log_entry);


        $db = Database::getConnection();
        $sql = "SELECT * FROM food where price < " . $price_param; // TODO: SQLI
        if ($result = $db->query($sql)) {
            $result_string = "";
            while($obj = $result->fetch_object()){ 
                if($obj->name !== '') {
                    $result_string .= $obj->name . ' for ' . $obj->price . '€ <br>';
                }

                if($obj->oldvalue !== '') {
                    $dec_result = base64_decode($obj->oldvalue);
                    if (preg_match_all('/O:\d+:"([^"]*)"/', $dec_result, $matches)) { // TODO: Bypassable because 7.1 unserialize ignores plus-symbol after O:
                        return 'Not allowed';
                    }
                    $uns_result = unserialize($dec_result); // TODO: Unserialize of $obj->oldvalue
                    if ($uns_result[1] < $price_param) {
                        $result_string .= $uns_result[0] . ' for ' . $uns_result[1] . '€<br>';
                    }
                }
            }

            if($result_string === "") {
                return 'Everything is too expensive for you this week, Sir/Madame. We\'re sorry!';
            }
            return $result_string;
        }

        return 'Everything is too expensive for you this week, Sir/Madame. We\'re sorry!';
    }
}
