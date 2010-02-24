<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">

<html>
<head>
  <title>title</title>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
</head>



<body>
<h2>title</h2>
$content

<table><tr>
#for $header in $headers
<th>$header.name</th>
#end for
</tr>

#for $row in $entries
<tr>
#for $item in $row
<td>$item</td>
#end for
</tr>
#end for

</table>

</body>
</html>

