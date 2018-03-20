<?php 
$servername="localhost";
$username="root";
$password="";
$database="";
$con=new mysqli($servername,$username,$password,$database);
if($con)
{
    echo "<br>";
}
else
{
    echo "not";
}
	
?>
<!DOCTYPE html>
<html>
<head>
<title>FAKE NEWS DETECTOR</title>
<style>
body {
        background-image: url("fakenews.jpg");
		background-size: 100% 100%;
		margin-top:500px;
}
</style>
</head>
<body >
<center>

<h1 style="width:200dp">FAKE NEWS DETECTOR</h1>
      <form action="" method="post"  enctype="multipart/form-data">
	  <b>Enter URL : </b>
	  &nbsp&nbsp&nbsp
	  <input type="text" name="off_name" style="width:400px;height:30px"></td>
	  <br>
	  <br><input type="submit" name="insert_off" value="Insert URL" style="width:120px;height:30px;">
	 
	  </form>
	  </center>
</body>

</html>
<?php    
    
    if(isset($_POST['insert_off'])){
    $o_name=$_POST['off_name'];	
    
        $del="delete from urldata;";
	$del_result=mysqli_query($con,$del);
	$insert="insert into urldata (id,urlname)
      values (null,'$o_name')";
	  
	  $insert_offer=mysqli_query($con,$insert);
	  
	  echo "<script>alert('URL has been inserted...!')</script>";
	  echo "<script>window.open('inserturl.php','_self')</script>";
    	
	}
?>
