<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">

<html>
<head>
	<title>$page.title</title>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
</head>
<body>


<table width="100%" height="100%" cellspacing="0" cellpadding="0"><tr>

  <td valign="top" width="100">
	NAVIGACE  
	<table>
	#for $child in $site.childs
	<tr>
  <td>
	<a href="$child.get_alternative_path_to($page)">$child.title</a>	
  </td>
  </tr>	
	#end for
</table>
  </td>
<td>
<div>
#for $predecessor in $page.get_predecessors()
<a href="$predecessor.get_alternative_path_to($page)">$predecessor.title</a> -> 
#end for
$page.title
</div>
<div>
$page.content
</div>


<div>
<hr/>
<h3>Subpages</h3>
#for $child in $page.childs
<a href="$child.subpage_path">$child.title</a><br/>
#end for
</div>

<div>
<hr/>
<h3>Comments</h3>
<table>
#for $comment in $page.comments
<tr>
<td>
$comment.author.name, $comment.author.email, $comment.updated.format(), revision: $comment.revision
<p>
$comment.text
</p>
</td>
</tr>
#end for
</table>
<hr/>
author: $page.author.name, $page.author.email<br/>
updated: $page.updated.format()<br/>
revision: $page.revision
</div>
<div>
<hr/>
<h2>Attachments</h3>
<table>
#for $attachment in $page.attachments
<tr>
<td>
$attachment.author.name, $attachment.author.email, $attachment.updated.format(), revision: $attachment.revision
<p>
<a href="$attachment.link">$attachment.name</a>
</p>
</td>
</tr>
#end for
</div>
</td>
</tr>
</table>
</body>
</html>
