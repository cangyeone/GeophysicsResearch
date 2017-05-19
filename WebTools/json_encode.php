<?php
header("Content-type:text/html;charset=utf8");
include("Json.php");
$method = $_POST['method'];
if($method=='SPH')
{exec("/root/anaconda3/bin/python method/damp.py");}
?>